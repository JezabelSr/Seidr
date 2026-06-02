"""
SEIÐR — Módulo 2: Tu criatura de asistencia
Asigna la criatura más afín al perfil del usuario aplicando el principio clínico de compensación
y permite descargar el Pacto de Acompañamiento de forma 100% privada.
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# Mapa clínico de interdependencia (Lógica de compensación)
MAPA_DIMS_CRIATURA = {
    "calma":        "regulacion_emocional",  # Poca regulación necesita MUCHA calma
    "vinculo":      "sociabilidad",           # Poca sociabilidad necesita un vínculo MUY proactivo
    "estimulacion": "hiperfoco",              # Mucho hiperfoco agradece estímulos de desconexión alternativos
    "independencia": "funcion_ejecutiva",      # Poca función ejecutiva requiere una criatura autónoma/independiente
}

UNIVERSOS_COPYRIGHT = {
    1: "© Warner Bros. / J.K. Rowling",
    2: "© New Line Cinema / Philip Pullman",
    3: "© Nintendo / The Pokémon Company",
    4: "© Studio Ghibli",
    5: "© DreamWorks Animation",
    6: "© The Walt Disney Company / Pixar",
}


@st.cache_data
def cargar_criaturas(universo_id: int):
    try:
        from db import cargar_criaturas as _db_criaturas
        df = _db_criaturas()
        if not df.empty:
            return df[df["universo_id"] == universo_id].reset_index(drop=True)
        raise Exception("BD vacía")
    except Exception:
        pass
    try:
        df = pd.read_csv("universos/criaturas.csv", engine="python")
        return df[df["universo_id"] == universo_id].reset_index(drop=True)
    except Exception:
        return pd.DataFrame()


def cargar_razas():
    try:
        from db import cargar_razas as _db_razas
        df = _db_razas()
        if not df.empty:
            return df
        raise Exception("BD vacía")
    except Exception:
        pass
    try:
        return pd.read_csv("universos/razas_akc_limpio.csv", engine="python")
    except Exception:
        return pd.DataFrame()


def encontrar_criatura_compensada(perfil_usuario: dict, criaturas: pd.DataFrame) -> pd.Series:
    """
    Algoritmo Clínico: Invierte las necesidades de soporte del usuario para calcular 
    el perfil matemático exacto de la criatura de asistencia ideal.
    """
    min_dist = float("inf")
    mejor = None
    
    # 1. Creamos las necesidades espejo ideales para el usuario (Fórmula Base 6.0)
    perfil_ideal = {}
    try:
        perfil_ideal["calma"] = 6.0 - float(perfil_usuario.get("regulacion_emocional", 3.0))
        perfil_ideal["vinculo"] = 6.0 - float(perfil_usuario.get("sociabilidad", 3.0))
        perfil_ideal["estimulacion"] = float(perfil_usuario.get("hiperfoco", 3.0))
        perfil_ideal["independencia"] = 6.0 - float(perfil_usuario.get("funcion_ejecutiva", 3.0))
    except Exception:
        # Fallback seguro en caso de valores nulos o incidencias
        perfil_ideal = {"calma": 3.0, "vinculo": 3.0, "estimulacion": 3.0, "independencia": 3.0}

    # 2. Buscamos qué criatura del CSV real se aproxima más a ese ideal compensatorio
    for _, row in criaturas.iterrows():
        try:
            dist_acumulada = 0.0
            for dim_criatura in MAPA_DIMS_CRIATURA.keys():
                if dim_criatura in row and pd.notna(row[dim_criatura]):
                    val_criatura = float(row[dim_criatura])
                    val_ideal = float(perfil_ideal[dim_criatura])
                    dist_acumulada += (val_ideal - val_criatura) ** 2
            
            dist = np.sqrt(dist_acumulada)
            if dist < min_dist:
                min_dist = dist
                mejor = row
        except Exception:
            continue
            
    return mejor


def cargar_imagen(url: str):
    if not url or str(url).strip() in ("", "nan"):
        st.markdown(
            "<div style='background:#1a1a28;border:1px solid #2a2a3a;"
            "border-radius:4px;padding:3rem;text-align:center;color:#555'>ᚱ</div>",
            unsafe_allow_html=True
        )
        return
    try:
        p = Path(str(url))
        if p.exists():
            st.image(str(p), use_container_width=True)
        else:
            st.image(str(url), use_container_width=True)
    except Exception:
        pass


def pagina_modulo_2():
    universo_id = st.session_state.get("universo_elegido")
    universo_nombre = st.session_state.get("universo_nombre", "tu universo")
    perfil = st.session_state.get("perfil_usuario")

    # Cabecera Rúnica
    st.markdown(
        "<div style='text-align:center;padding:1.5rem 0 1rem'>"
        "<h1 style=\"font-family:'Cinzel',serif;color:#c9a84c;"
        "letter-spacing:0.1em;font-size:1.8rem\">ᚢ Tu criatura de asistencia</h1>"
        "<p style='color:#9a9080;font-style:italic'>"
        f"Universo: {universo_nombre}</p></div>",
        unsafe_allow_html=True
    )

    if not universo_id:
        st.warning("Primero completa el test de universo.")
        return

    if not perfil:
        st.warning("Primero completa el test de perfil en el Módulo 1.")
        return

    criaturas = cargar_criaturas(universo_id)
    razas = cargar_razas()

    if criaturas.empty:
        st.error(f"No hay criaturas para el universo {universo_id}.")
        return

    # Ejecución del algoritmo compensado
    criatura = encontrar_criatura_compensada(perfil, criaturas)
    if criatura is None:
        st.error("No se pudo asignar una criatura.")
        return

    st.session_state.criatura_asignada = criatura["nombre"]

    # ── CRIATURA ──
    st.markdown("---")
    st.markdown(
        "<h2 style=\"font-family:'Cinzel',serif;color:#c9a84c;"
        "font-size:1.2rem;text-align:center\">Tu criatura</h2>",
        unsafe_allow_html=True
    )

    col_img, col_desc = st.columns([1, 2])
    with col_img:
        cargar_imagen(criatura.get("url_imagen", ""))
        copyright_txt = UNIVERSOS_COPYRIGHT.get(universo_id, "")
        if copyright_txt:
            st.markdown(
                f"<p style='color:#555;font-size:0.7rem;text-align:center;margin-top:0.3rem'>"
                f"{copyright_txt}. Uso educativo no comercial.</p>",
                unsafe_allow_html=True
            )

    with col_desc:
        st.markdown(
            f"<p style=\"font-family:'Cinzel',serif;color:#c9a84c;"
            f"font-size:1.1rem;margin-bottom:0.5rem\">{criatura['nombre']}</p>",
            unsafe_allow_html=True
        )
        descripcion = str(criatura.get("descripcion", ""))
        if descripcion and descripcion != "nan":
            st.markdown(
                f"<p style='color:#e8e0d0;font-size:0.9rem;line-height:1.6'>"
                f"{descripcion}</p>",
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='color:#9a9080;font-size:0.85rem;font-style:italic;'>Rasgos analíticos de esta criatura:</p>", unsafe_allow_html=True)
        
        # Guardamos las dimensiones locales para usarlas tanto en barras como en el TXT descargable
        dims_criatura = {
            "Calma":         float(criatura.get("calma", 3.0)),
            "Vínculo":       float(criatura.get("vinculo", 3.0)),
            "Estimulación":  float(criatura.get("estimulacion", 3.0)),
            "Independencia": float(criatura.get("independencia", 3.0)),
        }
        
        col_b1, col_b2 = st.columns(2)
        for idx, (nombre_dim, valor) in enumerate(dims_criatura.items()):
            col_actual = col_b1 if idx < 2 else col_b2
            pct = int((valor / 5) * 100)
            
            with col_actual:
                st.markdown(
                    f"<div style='margin-bottom:0.6rem'>"
                    f"<p style=\"font-family:'Cinzel',serif;color:#c9a84c;"
                    f"font-size:0.75rem;margin:0 0 0.2rem\">{nombre_dim}</p>"
                    f"<div style='background:#2a2a3a;border-radius:2px;height:5px'>"
                    f"<div style='background:#c9a84c;width:{pct}%;height:5px;"
                    f"border-radius:2px'></div></div></div>",
                    unsafe_allow_html=True
                )

    # ── SU EQUIVALENTE REAL (Búsqueda elástica por Texto) ──
    raza_id = criatura.get("raza_real_id")
    raza = None
    explicacion = str(criatura.get("explicacion_equivalencia", ""))
    
    if pd.notna(raza_id) and not razas.empty:
        st.markdown("---")
        st.markdown(
            "<h2 style=\"font-family:'Cinzel',serif;color:#c9a84c;"
            "font-size:1.2rem;text-align:center\">Su equivalente real</h2>",
            unsafe_allow_html=True
        )



        try:
            from razas_helper import buscar_raza
            raza, nombre_raza_display = buscar_raza(raza_id, explicacion, razas)
        except Exception:
            raza, nombre_raza_display = None, ""

        if raza is not None:
            col_raza_img, col_raza_info = st.columns([1, 2])
            with col_raza_img:
                cargar_imagen(raza.get("url_imagen", ""))

            with col_raza_info:
                st.markdown(
                    f"<p style=\"font-family:'Cinzel',serif;color:#c9a84c;"
                    f"font-size:1.1rem;margin-bottom:0.8rem\">{nombre_raza_display}</p>",
                    unsafe_allow_html=True
                )

                caracter = str(raza.get("caracter", ""))
                if caracter and caracter != "nan":
                    st.markdown(
                        f"<p style='color:#e8e0d0;font-size:0.9rem;line-height:1.6;"
                        f"margin-bottom:1rem'>{caracter}</p>",
                        unsafe_allow_html=True
                    )

                datos = []
                if pd.notna(raza.get("min_height")) and pd.notna(raza.get("max_height")):
                    datos.append(f"📏 Altura: {int(raza['min_height'])}-{int(raza['max_height'])} cm")
                if pd.notna(raza.get("min_weight")) and pd.notna(raza.get("max_weight")):
                    datos.append(f"⚖️ Peso: {int(raza['min_weight'])}-{int(raza['max_weight'])} kg")
                if pd.notna(raza.get("min_expectancy")) and pd.notna(raza.get("max_expectancy")):
                    datos.append(f"🕰️ Esperanza de vida: {int(raza['min_expectancy'])}-{int(raza['max_expectancy'])} años")
                if raza.get("group"):
                    datos.append(f"🏷️ Grupo: {raza['group']}")

                for dato in datos:
                    st.markdown(
                        f"<p style='color:#9a9080;font-size:0.85rem;margin:0.2rem 0'>{dato}</p>",
                        unsafe_allow_html=True
                    )

    # ── PERGAMINO DE ASISTENCIA (DESCARGABLE ANÓNIMO) ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='background:#1c1c2d; border: 1px dashed #c9a84c; padding: 1.5rem; border-radius: 8px; text-align: center; margin-bottom: 2rem;'>"
        "<h3 style=\"font-family:'Cinzel',serif; color:#c9a84c; font-size:1.1rem; margin-top:0;\">📜 Sella tu Pacto de Acompañamiento</h3>"
        "<p style='color:#9a9080; font-size:0.85rem; max-width: 500px; margin: 0 auto 1rem;'>"
        "Descarga tu guía de ruta personalizada en un pergamino digital. Procesado al vuelo en tu navegador: privacidad absoluta sin almacenamiento de datos.</p>",
        unsafe_allow_html=True
    )

    nombre_criatura = criatura["nombre"]
    nombre_raza_txt = nombre_raza_display if nombre_raza_display else (raza.get("breed", "Raza por definir") if raza is not None else "Raza por definir")
    
    # Generación de la plantilla de texto plano estético (.txt)
    texto_pergamino = f"""╔═══════════════════════════════════════════════════════════╗
  SEIÐR — PACTO DE ACOMPAÑAMIENTO Y SOPORTE CLÍNICO
╚═══════════════════════════════════════════════════════════╝

[ UNIVERSO DE CONEXIÓN ]: {universo_nombre.upper()}

Tu espectro y perfil neurodivergente manifiestan una afinidad
terapéutica de compensación con el siguiente guardián:

PROTECTOR ASIGNADO : {nombre_criatura.upper()}
EQUIVALENTE REAL   : {nombre_raza_txt.upper()}

─────────────────────────────────────────────────────────────
▶ RASGOS ANALÍTICOS DE LA CRIATURA (PERFIL DE COMPENSACIÓN):
─────────────────────────────────────────────────────────────
• CALMA (Frente a desregulación emocional):   {int((dims_criatura['Calma']/5)*100)}% 
• VÍNCULO (Frente a necesidades sociales):    {int((dims_criatura['Vínculo']/5)*100)}% 
• ESTIMULACIÓN (Frente a bucles de hiperfoco): {int((dims_criatura['Estimulación']/5)*100)}% 
• INDEPENDENCIA (Soporte en función ejecutiva): {int((dims_criatura['Independencia']/5)*100)}%

─────────────────────────────────────────────────────────────
▶ EXPLICACIÓN DE LA EQUIVALENCIA CLÍNICA:
─────────────────────────────────────────────────────────────
{explicacion if (explicacion and explicacion != 'nan') else 'Soporte adaptado minuciosamente a los picos de demanda del entorno del usuario.'}

─────────────────────────────────────────────────────────────
▶ GUÍA DE RUTA INMEDIATA (¿Por dónde tirar?):
─────────────────────────────────────────────────────────────
1. REGULACIÓN CONSCIENTE: Emplea la simbología o imágenes de {nombre_criatura}
   como un anclaje externo/foco primario en momentos de sobrecarga cognitiva.
2. ADAPTACIÓN DE ENTORNOS: La raza {nombre_raza_txt} refleja tu mapa ideal de 
   soporte. Diseña tus rutinas buscando un balance idéntico entre sus niveles de 
   calma e iniciativa autónoma.
3. PRÓXIMO PASO: Avanza al Módulo 3 en la aplicación para configurar tus 
   estrategias de comunicación personalizada y gestión del cansancio social.

─────────────────────────────────────────────────────────────
Documento generado de forma 100% privada por el motor SEIÐR.
Ningún dato clínico ha sido registrado en servidores externos.
─────────────────────────────────────────────────────────────"""

    st.download_button(
        label="📥 Descargar mi Pergamino de Asistencia (.txt)",
        data=texto_pergamino,
        file_name=f"Seidr_Pacto_{nombre_criatura}.txt",
        mime="text/plain"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Narrador contextual ──
    try:
        from narrador import get_narrador
        universo_id = st.session_state.get("universo_elegido")
        texto_narrador = get_narrador(universo_id, "criatura_asignada")
        if texto_narrador:
            st.markdown(
                f"<div style='background:rgba(201,168,76,0.06);border-left:3px solid #c9a84c;"
                f"border-radius:0 8px 8px 0;padding:1rem 1.5rem;margin:1rem 0 1.5rem;'>"
                f"<p style='color:#c9a84c;font-size:0.9rem;font-style:italic;margin:0;"
                f"line-height:1.7;'>{texto_narrador}</p></div>",
                unsafe_allow_html=True
            )
    except Exception:
        pass

    # Botón para avanzar al módulo 3
    st.markdown("---")
    col_btn = st.columns([1, 2, 1])[1]
    with col_btn:
        if st.button("ᚲ Continuar a Comunicación →", use_container_width=True, key="btn_m2_siguiente"):
            for etiqueta, key in {
                "ᚱ  Inicio": "inicio",
                "ᚦ  Test de universo": "test_universo",
                "ᚨ  Tu perfil": "modulo_1",
                "ᚢ  Tu criatura": "modulo_2",
                "ᚲ  Comunicación": "modulo_3",
                "ᚷ  Aprendizaje": "modulo_4",
                "ᛉ  Sociabilidad": "modulo_5",
                "ᛊ  Tu cuerpo": "modulo_6",
                "ᛏ  Orientación clínica": "modulo_7",
                "⚕  Modo profesional": "profesional",
            }.items():
                if key == "modulo_3":
                    st.session_state["_pagina_activa"] = etiqueta
                    st.rerun()