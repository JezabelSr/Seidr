"""
SEIÐR — Generador de PDFs
Genera PDFs descargables para el usuario con su perfil completo y recursos por módulo.
Usa fpdf2 — sin dependencias externas complicadas.
"""

from fpdf import FPDF
from io import BytesIO
import pandas as pd
from pathlib import Path


# ── Paleta de colores ─────────────────────────────────────────────────────────
DORADO  = (201, 168, 76)
BLANCO  = (232, 224, 208)
GRIS    = (154, 144, 128)
OSCURO  = (20, 20, 30)
AZUL    = (74, 127, 165)

# ── Fuente base ───────────────────────────────────────────────────────────────
# fpdf2 incluye fuentes básicas — usamos Helvetica para compatibilidad total
# Las runas se sustituyen por texto equivalente ya que fpdf2 no soporta Unicode completo


class SeidrPDF(FPDF):
    """Clase base con cabecera y pie de página estilo Seiðr."""

    def __init__(self, titulo_pagina: str = "SEIDR"):
        super().__init__()
        self.titulo_pagina = titulo_pagina
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        # Barra dorada superior
        self.set_fill_color(*DORADO)
        self.rect(0, 0, 210, 8, "F")
        # Título
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
                  "Seidr no es una herramienta de diagnostico. Este documento es orientativo. "
                  f"Pagina {self.page_no()}",
                  align="C")

    def seccion(self, titulo: str):
        """Título de sección con línea dorada."""
        self.ln(4)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*DORADO)
        self.cell(0, 8, titulo.upper(), ln=True)
        self.set_draw_color(*DORADO)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def cuerpo(self, texto: str):
        """Párrafo de texto normal."""
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*BLANCO)
        self.multi_cell(0, 6, texto)
        self.ln(2)

    def etiqueta_valor(self, etiqueta: str, valor: str):
        """Par etiqueta: valor en línea."""
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*DORADO)
        self.cell(55, 6, etiqueta + ":", ln=False)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*BLANCO)
        self.cell(0, 6, str(valor), ln=True)

    def barra_dimension(self, nombre: str, valor: float, max_val: float = 5.0):
        """Barra de progreso para una dimensión."""
        pct = min(valor / max_val, 1.0)
        ancho_total = 120
        ancho_barra = int(ancho_total * pct)

        self.set_font("Helvetica", "", 9)
        self.set_text_color(*GRIS)
        self.cell(55, 5, nombre, ln=False)

        # Barra fondo
        x, y = self.get_x(), self.get_y()
        self.set_fill_color(42, 42, 58)
        self.rect(x, y + 1, ancho_total, 3, "F")

        # Barra activa
        self.set_fill_color(*DORADO)
        if ancho_barra > 0:
            self.rect(x, y + 1, ancho_barra, 3, "F")

        # Valor numérico
        self.set_xy(x + ancho_total + 3, y)
        self.set_text_color(*DORADO)
        self.cell(15, 5, f"{valor:.1f}/5", ln=True)

    def fondo_oscuro(self):
        """Fondo oscuro para toda la página."""
        self.set_fill_color(*OSCURO)
        self.rect(0, 0, 210, 297, "F")


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
    """Genera el PDF completo de la saga del usuario."""

    pdf = SeidrPDF("Tu Saga")
    pdf.add_page()
    pdf.fondo_oscuro()

    # ── PORTADA ──
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*DORADO)
    pdf.cell(0, 12, "TU SAGA SEIDR", align="C", ln=True)

    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(*GRIS)
    pdf.cell(0, 8, "Cuando tu saga se convierte en brujula", align="C", ln=True)
    pdf.ln(8)

    # ── UNIVERSO Y PERSONAJE ──
    pdf.seccion("Tu universo y personaje")
    pdf.etiqueta_valor("Universo", universo_nombre)
    pdf.etiqueta_valor("Personaje asignado", personaje_nombre)

    if personaje_data:
        rol = str(personaje_data.get("rol", ""))
        if rol and rol != "nan":
            pdf.etiqueta_valor("Rol", rol)
        justificacion = str(personaje_data.get("justificacion", ""))
        if justificacion and justificacion != "nan":
            pdf.ln(2)
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(*GRIS)
            pdf.multi_cell(0, 5, f'"{justificacion}"')
    pdf.ln(4)

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
        pdf.barra_dimension(nombre, valor)
    pdf.ln(4)

    # ── ORIENTACIÓN ND ──
    if orientacion_nd:
        pdf.seccion("Orientacion neurodivergente")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*GRIS)
        pdf.cell(0, 5,
                 "Perfil orientativo basado en tus puntuaciones. No equivale a un diagnostico.",
                 ln=True)
        pdf.ln(2)
        for nd in orientacion_nd:
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(*DORADO)
            pdf.cell(8, 6, "-", ln=False)
            pdf.cell(0, 6, nd, ln=True)
        pdf.ln(4)

    # ── CRIATURA ──
    pdf.seccion("Tu criatura de asistencia")
    pdf.etiqueta_valor("Criatura asignada", criatura_nombre)
    pdf.etiqueta_valor("Equivalente real", raza_nombre)
    if explicacion_equivalencia and explicacion_equivalencia != "nan":
        pdf.ln(2)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(*GRIS)
        pdf.multi_cell(0, 5, explicacion_equivalencia)
    pdf.ln(6)

    # ── PIE ──
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*GRIS)
    pdf.cell(0, 5,
             "Documento generado de forma privada por Seidr. "
             "Ningun dato ha sido almacenado en servidores externos.",
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
    """Genera el PDF de un módulo de recursos."""

    titulo = MODULO_TITULOS.get(modulo, f"Modulo {modulo}")
    subtitulo = MODULO_SUBTITULOS.get(modulo, "")

    pdf = SeidrPDF(titulo)
    pdf.add_page()
    pdf.fondo_oscuro()

    # Cabecera del módulo
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
        # Usuario NT
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(*GRIS)
        pdf.cell(0, 6,
                 "Tu perfil no muestra rasgos compatibles con ningun patron de neurodivergencia.",
                 ln=True)
        pdf.cell(0, 6, "Aqui tienes recursos generales que pueden ser utiles.", ln=True)
        pdf.ln(4)

    # ── Contenido por ND (módulos 3-6) ──
    if modulo <= 6 and not df_contenido.empty:
        for nd in nds:
            fila = df_contenido[
                (df_contenido["nd"] == nd) & (df_contenido["modulo"] == modulo)
            ]
            if fila.empty:
                continue

            row = fila.iloc[0]
            pdf.seccion(f"Perfil: {nd}")

            # Explicación
            explicacion = str(row.get("explicacion_perfil", ""))
            if explicacion and explicacion != "nan":
                pdf.cuerpo(explicacion)

            # Técnicas
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

            # Adaptaciones
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

    # ── Recursos ──
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
                gratuito = str(r.get("gratuito", "")).lower() in ("true", "1", "si", "sí")
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

    # Aviso módulo 7
    if modulo == 7:
        pdf.ln(4)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(*GRIS)
        pdf.multi_cell(0, 5,
                       "IMPORTANTE: Los tests que aparecen aqui son de cribado orientativo. "
                       "Un diagnostico solo puede darlo un profesional cualificado.")

    return bytes(pdf.output())
