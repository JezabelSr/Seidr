"""
SEIÐR — Generador de PDFs
Genera PDFs descargables para el usuario con su perfil completo y recursos por módulo.
Usa fpdf2 — sin dependencias externas complicadas.
"""

from fpdf import FPDF
from io import BytesIO
import pandas as pd
from pathlib import Path
import re

# ── Paleta de colores ─────────────────────────────────────────────────────────
DORADO  = (201, 168, 76)
BLANCO  = (232, 224, 208)
GRIS    = (154, 144, 128)
OSCURO  = (20, 20, 30)
AZUL    = (74, 127, 165)
GRIS_OSCURO = (42, 42, 58)

# ── Descripciones de dimensiones ─────────────────────────────────────────────
DESC_DIMENSIONES = {
    "hiperfoco":            "Intensidad y concentracion en intereses especificos. Puntuaciones altas indican capacidad de enfoque profundo y prolongado.",
    "regulacion_emocional": "Como se gestionan y expresan las emociones. Puntuaciones bajas pueden indicar mayor intensidad emocional o dificultad para regularla.",
    "sensorialidad":        "Como se procesa el entorno sensorial. Puntuaciones altas indican mayor sensibilidad o procesamiento intenso de estimulos.",
    "comunicacion":         "Estilo y forma de expresarse. Refleja preferencias de comunicacion oral, escrita, directa o indirecta.",
    "aprendizaje":          "Como se absorbe y procesa la informacion. Incluye preferencias de canal, ritmo y estilo de aprendizaje.",
    "sociabilidad":         "Como se relaciona con los demas. Puntuaciones bajas no indican aislamiento sino preferencia por interacciones selectivas.",
    "propiocepcion":        "Conciencia y necesidades del propio cuerpo. Incluye la necesidad de movimiento, estimulacion tactil y conciencia espacial.",
    "funcion_ejecutiva":    "Planificacion, organizacion, inicio de tareas y flexibilidad cognitiva. Area central en muchos perfiles neurodivergentes.",
}

DESC_ND = {
    "Dislexia":                   "Dificultad especifica en la decodificacion lectora y escritura, no relacionada con la inteligencia. Fortalezas en pensamiento visual y narrativo.",
    "TDAH":                       "Patron de inatención, hiperactividad e impulsividad que interfiere en el funcionamiento. Sistema de motivacion y atencion diferente al tipico.",
    "TEA":                        "Diferencias en comunicacion social y patrones de comportamiento. Pensamiento sistematico, honestidad y profundidad en intereses.",
    "AACC":                       "Capacidad de aprendizaje y procesamiento significativamente por encima de la media. Necesidad de profundidad, complejidad y estimulacion.",
    "Discalculia":                "Dificultad especifica en el procesamiento numerico. No afecta a la inteligencia general ni a otras areas del aprendizaje.",
    "Dispraxia/TDC":              "Dificultad en la planificacion y ejecucion motora. Afecta a la coordinacion y al aprendizaje de habilidades motrices nuevas.",
    "Sindrome de Tourette":       "Presencia de tics motores y vocales involuntarios. No afecta a la inteligencia ni a las capacidades comunicativas.",
    "SPD":                        "Procesamiento sensorial atipico: hipo o hipersensibilidad en distintas modalidades. El entorno puede ser agotador o insuficiente.",
    "Tartamudez":                 "Disfluencia del habla que afecta al flujo y ritmo de la comunicacion oral. Capacidad comunicativa completamente intacta.",
    "Discapacidad Intelectual":   "Limitaciones en el funcionamiento intelectual y en la conducta adaptativa. Mayor tiempo y apoyos para el aprendizaje.",
    "TOC":                        "Presencia de obsesiones y compulsiones que generan malestar significativo. Pensamiento detallista y orientado a la precision.",
    "Mutismo Selectivo":          "Incapacidad para hablar en determinados contextos sociales, de base ansiosa. En entornos seguros la comunicacion es fluida.",
    "Trastorno de Ansiedad Social":"Miedo intenso y persistente a situaciones de evaluacion social. Capacidades sociales intactas pero inhibidas por la ansiedad.",
    "TANV":                       "Dificultad en el procesamiento visual-espacial y no verbal. Fortalezas en lenguaje verbal, memoria verbal y habilidades academicas.",
}

# ── Mapeo breed → archivo de imagen ──────────────────────────────────────────
def _breed_a_archivo(breed: str) -> str | None:
    """Convierte el nombre del breed del CSV al nombre del archivo en iconografia/razas/."""
    if not breed or str(breed) == "nan":
        return None
    # Normalizar: minúsculas, espacios → guión bajo, quitar caracteres especiales
    nombre = breed.lower().strip()
    nombre = re.sub(r'[áàä]', 'a', nombre)
    nombre = re.sub(r'[éèë]', 'e', nombre)
    nombre = re.sub(r'[íìï]', 'i', nombre)
    nombre = re.sub(r'[óòö]', 'o', nombre)
    nombre = re.sub(r'[úùü]', 'u', nombre)
    nombre = re.sub(r'[^\w\s]', '', nombre)
    nombre = re.sub(r'\s+', '_', nombre)
    
    # Buscar en la carpeta
    carpeta = Path("iconografia/razas")
    for ext in [".jpg", ".jpeg", ".png", ".gif", ".avif"]:
        ruta = carpeta / f"{nombre}{ext}"
        if ruta.exists():
            return str(ruta)
    
    # Búsqueda parcial por si el nombre no coincide exactamente
    if carpeta.exists():
        for archivo in carpeta.iterdir():
            if nombre.split("_")[0] in archivo.stem.lower():
                return str(archivo)
    
    return None


# ── Limpieza de texto para compatibilidad latin-1 ───────────────────────────
def _limpiar(texto: str) -> str:
    """Sustituye caracteres Unicode no soportados por Helvetica."""
    if not texto:
        return ""
    return (str(texto)
        .replace("—", "-").replace("–", "-")
        .replace("‘", "'").replace("’", "'")
        .replace("“", '"').replace("”", '"')
        .replace("á", "a").replace("é", "e")
        .replace("í", "i").replace("ó", "o")
        .replace("ú", "u").replace("ñ", "n")
        .replace("Á", "A").replace("É", "E")
        .replace("Í", "I").replace("Ó", "O")
        .replace("Ú", "U").replace("Ñ", "N")
        .replace("ü", "u").replace("à", "a")
        .replace("è", "e").replace("ò", "o")
        .replace("ù", "u").replace("ì", "i")
        .replace("¿", "?").replace("¡", "!")
        .replace("·", "*").replace("…", "...")
    )


# ── Clase PDF base ────────────────────────────────────────────────────────────

class SeidrPDF(FPDF):
    def __init__(self, titulo_pagina: str = "SEIDR"):
        super().__init__()
        self.titulo_pagina = titulo_pagina
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_fill_color(*DORADO)
        self.rect(0, 0, 210, 8, "F")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*OSCURO)
        self.set_xy(10, 1)
        self.cell(0, 6, f"SEIDR  *  {self.titulo_pagina.upper()}", align="L")
        self.set_xy(0, 1)
        self.cell(200, 6, "seidr-app.streamlit.app", align="R")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*GRIS)
        self.cell(0, 10,
                  "Seidr no es una herramienta de diagnostico. Este documento es orientativo.  "
                  f"Pagina {self.page_no()}",
                  align="C")

    def fondo_oscuro(self):
        self.set_fill_color(*OSCURO)
        self.rect(0, 0, 210, 297, "F")

    def seccion(self, titulo: str):
        self.ln(5)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*DORADO)
        self.cell(0, 8, titulo.upper(), ln=True)
        self.set_draw_color(*DORADO)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def cuerpo(self, texto: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*BLANCO)
        self.multi_cell(0, 6, _limpiar(texto))
        self.ln(2)

    def cuerpo_gris(self, texto: str):
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*GRIS)
        self.multi_cell(0, 5, _limpiar(texto))
        self.ln(1)

    def etiqueta_valor(self, etiqueta: str, valor: str):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DORADO)
        self.cell(55, 6, _limpiar(etiqueta) + ":", new_x="RIGHT", new_y="TOP")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*BLANCO)
        self.multi_cell(130, 6, _limpiar(str(valor)))

    def barra_dimension(self, nombre: str, valor: float, descripcion: str = "", max_val: float = 5.0):
        pct = min(valor / max_val, 1.0)
        ancho_total = 80
        ancho_barra = int(ancho_total * pct)

        y_ini = self.get_y()

        # Nombre dimensión
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*DORADO)
        self.cell(58, 5, nombre, ln=False)

        # Barra fondo
        x, y = self.get_x(), self.get_y()
        self.set_fill_color(*GRIS_OSCURO)
        self.rect(x, y + 1, ancho_total, 3, "F")
        # Barra activa
        self.set_fill_color(*DORADO)
        if ancho_barra > 0:
            self.rect(x, y + 1, ancho_barra, 3, "F")
        # Valor
        self.set_xy(x + ancho_total + 3, y)
        self.set_text_color(*DORADO)
        self.set_font("Helvetica", "B", 9)
        self.cell(15, 5, f"{valor:.1f}/5", ln=True)

        # Descripción de la dimensión
        if descripcion:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(*GRIS)
            self.set_x(58 + 10)
            self.multi_cell(ancho_total + 18, 4, descripcion)
        self.ln(1)


# ── PDF 1: Tu Saga Completa ───────────────────────────────────────────────────

def generar_pdf_saga(
    universo_nombre: str,
    personaje_nombre: str,
    personaje_data: dict,
    perfil_usuario: dict,
    orientacion_nd: list,
    criatura_nombre: str,
    raza_nombre: str,
    explicacion_equivalencia: str,
) -> bytes:

    # Limpiar todos los textos de entrada
    universo_nombre = _limpiar(universo_nombre)
    personaje_nombre = _limpiar(personaje_nombre)
    criatura_nombre = _limpiar(criatura_nombre)
    raza_nombre = _limpiar(raza_nombre)
    explicacion_equivalencia = _limpiar(explicacion_equivalencia)

    pdf = SeidrPDF("Tu Saga")
    pdf.add_page()
    pdf.fondo_oscuro()

    # ── PORTADA ──
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*DORADO)
    pdf.cell(0, 12, "TU SAGA SEIDR", align="C", ln=True)
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(*GRIS)
    pdf.cell(0, 7, "Cuando tu saga se convierte en brujula", align="C", ln=True)
    pdf.ln(6)

    # Línea decorativa
    pdf.set_draw_color(*DORADO)
    pdf.set_line_width(0.3)
    pdf.line(50, pdf.get_y(), 160, pdf.get_y())
    pdf.ln(8)

    # ── UNIVERSO Y PERSONAJE ──
    pdf.seccion("Tu universo y personaje")
    pdf.etiqueta_valor("Universo", universo_nombre)
    pdf.etiqueta_valor("Personaje asignado", personaje_nombre)

    if personaje_data:
        rol = str(personaje_data.get("rol", ""))
        if rol and rol != "nan":
            pdf.etiqueta_valor("Rol en el universo", rol)
        descripcion = str(personaje_data.get("descripcion", ""))
        if descripcion and descripcion != "nan":
            pdf.ln(2)
            pdf.cuerpo_gris(descripcion)
        justificacion = str(personaje_data.get("justificacion", ""))
        if justificacion and justificacion != "nan":
            pdf.ln(1)
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(*GRIS)
            pdf.multi_cell(0, 5, f'Por que este personaje: "{justificacion}"')
    pdf.ln(3)

    # ── PERFIL DE 8 DIMENSIONES ──
    pdf.seccion("Tu perfil de 8 dimensiones")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*GRIS)
    pdf.cell(0, 5, "Puntuaciones de 0 a 5 obtenidas en el test de perfil.", ln=True)
    pdf.ln(3)

    DIMS = [
        ("hiperfoco",            "Hiperfoco"),
        ("regulacion_emocional", "Regulacion emocional"),
        ("sensorialidad",        "Sensorialidad"),
        ("comunicacion",         "Comunicacion"),
        ("aprendizaje",          "Aprendizaje"),
        ("sociabilidad",         "Sociabilidad"),
        ("propiocepcion",        "Propiocepcion"),
        ("funcion_ejecutiva",    "Funcion ejecutiva"),
    ]
    for key, nombre in DIMS:
        valor = float(perfil_usuario.get(key, 0))
        desc = DESC_DIMENSIONES.get(key, "")
        pdf.barra_dimension(nombre, valor, desc)
    pdf.ln(3)

    # ── ORIENTACIÓN ND ──
    if orientacion_nd:
        pdf.seccion("Orientacion neurodivergente")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*GRIS)
        pdf.cell(0, 5,
                 "Perfil orientativo basado en tus puntuaciones. No equivale a un diagnostico clinico.",
                 ln=True)
        pdf.ln(3)
        for nd in orientacion_nd:
            # Nombre ND
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(*DORADO)
            pdf.cell(0, 6, nd, ln=True)
            # Descripción
            desc_nd = DESC_ND.get(nd, "")
            if desc_nd:
                pdf.set_font("Helvetica", "", 9)
                pdf.set_text_color(*BLANCO)
                pdf.set_x(15)
                pdf.multi_cell(0, 5, desc_nd)
            pdf.ln(2)

    # ── CRIATURA ──
    pdf.seccion("Tu criatura de asistencia")

    # Intentar añadir imagen de la raza
    ruta_img = _breed_a_archivo(raza_nombre)

    # Intentar añadir imagen de la raza
    ruta_img = _breed_a_archivo(raza_nombre)
    if ruta_img:
        try:
            y_ini = pdf.get_y()
            pdf.image(ruta_img, x=10, y=y_ini, w=45, h=45)
            pdf.set_xy(60, y_ini)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(*DORADO)
            pdf.multi_cell(140, 7, _limpiar(criatura_nombre))
            pdf.set_x(60)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(*BLANCO)
            pdf.multi_cell(140, 6, _limpiar(f"Equivalente real: {raza_nombre}"))
            if explicacion_equivalencia and explicacion_equivalencia != "nan":
                pdf.set_x(60)
                pdf.set_font("Helvetica", "I", 9)
                pdf.set_text_color(*GRIS)
                pdf.multi_cell(140, 5, _limpiar(explicacion_equivalencia))
            if pdf.get_y() < y_ini + 48:
                pdf.set_y(y_ini + 48)
        except Exception:
            pdf.etiqueta_valor("Criatura asignada", criatura_nombre)
            pdf.etiqueta_valor("Equivalente real", raza_nombre)
            if explicacion_equivalencia and explicacion_equivalencia != "nan":
                pdf.cuerpo_gris(explicacion_equivalencia)
    else:
        pdf.etiqueta_valor("Criatura asignada", criatura_nombre)
        pdf.etiqueta_valor("Equivalente real", raza_nombre)
        if explicacion_equivalencia and explicacion_equivalencia != "nan":
            pdf.cuerpo_gris(explicacion_equivalencia)

    pdf.ln(6)

    # ── PIE ──
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*GRIS)
    pdf.cell(0, 5,
             "Documento generado de forma privada por Seidr. Ningun dato ha sido almacenado en servidores externos.",
             align="C", ln=True)

    return bytes(pdf.output())


# ── PDF Módulos 3-7 ───────────────────────────────────────────────────────────

MODULO_TITULOS = {
    3: "Tu forma de comunicarte",
    4: "Tu forma de aprender",
    5: "Tu forma de socializar",
    6: "Tu cuerpo",
    7: "Orientacion clinica",
}

MODULO_SUBTITULOS = {
    3: "Comunicacion",
    4: "Aprendizaje y Funcion Ejecutiva",
    5: "Sociabilidad",
    6: "Propiocepcion y Sensorialidad",
    7: "Tests, profesionales y recursos clinicos",
}


def generar_pdf_modulo(
    modulo: int,
    orientacion_nd: list,
    df_contenido: pd.DataFrame,
    df_recursos: pd.DataFrame,
) -> bytes:

    titulo = MODULO_TITULOS.get(modulo, f"Modulo {modulo}")
    subtitulo = MODULO_SUBTITULOS.get(modulo, "")

    pdf = SeidrPDF(titulo)
    pdf.add_page()
    pdf.fondo_oscuro()

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*DORADO)
    pdf.cell(0, 10, titulo.upper(), align="C", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*GRIS)
    pdf.cell(0, 6, subtitulo, align="C", ln=True)
    pdf.ln(6)

    nds = orientacion_nd if orientacion_nd else []

    if not nds:
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(*GRIS)
        pdf.multi_cell(0, 6, "Tu perfil no muestra rasgos compatibles con ningun patron de neurodivergencia. Aqui tienes recursos generales.")
        pdf.ln(4)

    # Contenido por ND (módulos 3-6)
    if modulo <= 6 and not df_contenido.empty:
        for nd in nds:
            fila = df_contenido[
                (df_contenido["nd"] == nd) & (df_contenido["modulo"] == modulo)
            ]
            if fila.empty:
                continue
            row = fila.iloc[0]
            pdf.seccion(f"Perfil: {nd}")

            explicacion = str(row.get("explicacion_perfil", ""))
            if explicacion and explicacion != "nan":
                pdf.cuerpo(explicacion)

            tecnicas = [t.strip() for t in str(row.get("tecnicas", "")).split("|") if t.strip()]
            if tecnicas:
                pdf.ln(2)
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(*DORADO)
                pdf.cell(0, 6, "Que puedes hacer:", ln=True)
                for t in tecnicas:
                    pdf.set_font("Helvetica", "", 9)
                    pdf.set_text_color(*BLANCO)
                    pdf.cell(8, 5, "-", ln=False)
                    pdf.multi_cell(0, 5, t)

            adaptaciones = [a.strip() for a in str(row.get("adaptaciones", "")).split("|") if a.strip()]
            if adaptaciones:
                pdf.ln(2)
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(*AZUL)
                pdf.cell(0, 6, "Que puedes pedir a tu entorno:", ln=True)
                for a in adaptaciones:
                    pdf.set_font("Helvetica", "", 9)
                    pdf.set_text_color(*BLANCO)
                    pdf.cell(8, 5, "-", ln=False)
                    pdf.multi_cell(0, 5, a)
            pdf.ln(4)

    # Recursos
    if not df_recursos.empty:
        df_mod = df_recursos[df_recursos["modulo"] == modulo]
        if nds:
            def coincide(celda):
                if pd.isna(celda):
                    return False
                return any(nd in [n.strip() for n in str(celda).split(",")] for nd in nds)
            df_rec = df_mod[df_mod["neurodivergencias"].apply(coincide)]
            if df_rec.empty:
                df_rec = df_mod
        else:
            df_rec = df_mod

        if not df_rec.empty:
            pdf.seccion("Si quieres profundizar")
            for _, r in df_rec.iterrows():
                nombre = str(r.get("nombre", ""))
                desc = str(r.get("descripcion", ""))
                url = str(r.get("url", ""))
                gratuito = str(r.get("gratuito", "")).lower() in ("true", "1", "si", "si")
                tag = "[Gratuito]" if gratuito else "[De pago]"

                pdf.set_font("Helvetica", "B", 9)
                pdf.set_text_color(*DORADO)
                pdf.cell(0, 5, f"{nombre}  {tag}", ln=True)
                if desc and desc != "nan":
                    pdf.set_font("Helvetica", "", 8)
                    pdf.set_text_color(*GRIS)
                    pdf.multi_cell(0, 4, desc)
                if url and url != "nan":
                    pdf.set_font("Helvetica", "I", 8)
                    pdf.set_text_color(*AZUL)
                    pdf.cell(0, 4, url, ln=True)
                pdf.ln(2)

    if modulo == 7:
        pdf.ln(4)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(*GRIS)
        pdf.multi_cell(0, 5,
                       "IMPORTANTE: Los tests que aparecen aqui son de cribado orientativo. "
                       "Un diagnostico solo puede darlo un profesional cualificado.")

    return bytes(pdf.output())
