"""
SEIÐR — Módulo de Regreso
Permite al usuario recuperar su perfil completo con su código Seiðr.
"""

import streamlit as st
import pandas as pd
from pathlib import Path


def _cargar_personaje(personaje_id: int) -> dict:
    """Carga los datos de un personaje por su ID."""
    try:
        from db import cargar_personajes
        df = cargar_personajes()
    except Exception:
        try:
            df = pd.read_csv("universos/personajes.csv", encoding="utf-8-sig")
        except Exception:
            return {}

    if df.empty:
        return {}

    fila = df[df["personaje_id"] == personaje_id]
    if fila.empty:
        return {}
    return fila.iloc[0].to_dict()


def _cargar_criatura(universo_id: int, perfil: dict) -> dict:
    """Asigna la criatura compensada para el perfil dado."""
    try:
        import numpy as np
        from db import cargar_criaturas
        criaturas = cargar_criaturas(universo_id)
    except Exception:
        try:
            import numpy as np
            df = pd.read_csv("universos/criaturas.csv", encoding="utf-8-sig")
            criaturas = df[df["universo_id"] == universo_id]
        except Exception:
            return {}

    if criaturas.empty:
        return {}

    MAPA = {
        "calma":         "regulacion_emocional",
        "vinculo":       "sociabilidad",
        "estimulacion":  "hiperfoco",
        "independencia": "funcion_ejecutiva",
    }
    perfil_ideal = {
        "calma":         6.0 - float(perfil.get("regulacion_emocional", 3.0)),
        "vinculo":       6.0 - float(perfil.get("sociabilidad", 3.0)),
        "estimulacion":  float(perfil.get("hiperfoco", 3.0)),
        "independencia": 6.0 - float(perfil.get("funcion_ejecutiva", 3.0)),
    }

    import numpy as np
    min_dist = float("inf")
    mejor = None
    for _, row in criaturas.iterrows():
        try:
            dist = sum(
                (perfil_ideal[d] - float(row[d])) ** 2
                for d in MAPA if d in row and pd.notna(row[d])
            ) ** 0.5
            if dist < min_dist:
                min_dist = dist
                mejor = row
        except Exception:
            continue
    return mejor.to_dict() if mejor is not None else {}


def pagina_regreso():
    st.markdown("""
    <div style='text-align:center;padding:1rem 0 0.5rem'>
        <h2 style="font-family:'Cinzel',serif;color:#c9a84c;letter-spacing:0.1em;">
            ᚺ Ya estuve aquí
        </h2>
        <p style='color:#9a9080;font-style:italic;font-size:0.9rem;'>
            Introduce tu código Seiðr para recuperar tu saga
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Instrucciones ──
    st.markdown("""
    <div style="background:rgba(74,127,165,0.1);border:1px solid rgba(74,127,165,0.3);
                border-radius:8px;padding:1rem 1.5rem;margin-bottom:1.5rem;">
        <p style="color:#e8e0d0;font-size:0.9rem;margin:0;line-height:1.7;">
            Tu código Seiðr aparece en el PDF descargable de tu saga.<br>
            Tiene este formato: <strong style="color:#c9a84c;">SEIDR-1-051-TOC.AACC-54505005</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Input del código ──
    codigo_input = st.text_input(
        "Tu código Seiðr",
        placeholder="SEIDR-1-051-TOC.AACC-54505005",
        label_visibility="collapsed",
    )

    col = st.columns([1, 2, 1])[1]
    with col:
        btn = st.button("ᚺ Recuperar mi saga", use_container_width=True, key="btn_regreso")

    if btn and codigo_input:
        from codigo_seidr import decodificar_codigo

        datos = decodificar_codigo(codigo_input.strip())

        if datos is None:
            st.markdown("""
            <div style="background:rgba(180,50,50,0.15);border:1px solid rgba(180,50,50,0.4);
                        border-radius:8px;padding:1rem 1.5rem;margin-top:1rem;">
                <p style="color:#e8a0a0;font-size:0.9rem;margin:0;">
                    ⚠️ Código no reconocido. Comprueba que lo has copiado correctamente del PDF.
                </p>
            </div>
            """, unsafe_allow_html=True)
            return

        # ── Cargar perfil en session_state ──
        universo_id    = datos["universo_id"]
        universo_nombre = datos["universo_nombre"]
        personaje_id   = datos["personaje_id"]
        orientacion_nd = datos["orientacion_nd"]
        perfil         = datos["perfil_usuario"]

        personaje_data = _cargar_personaje(personaje_id)
        personaje_nombre = personaje_data.get("nombre", f"Personaje #{personaje_id}")

        criatura_data = _cargar_criatura(universo_id, perfil)
        criatura_nombre = criatura_data.get("nombre", "")

        # Guardar en session_state
        st.session_state["universo_elegido"]   = universo_id
        st.session_state["universo_nombre"]    = universo_nombre
        st.session_state["perfil_usuario"]     = perfil
        st.session_state["personaje_asignado"] = personaje_nombre
        st.session_state["personaje_data"]     = personaje_data
        st.session_state["criatura_asignada"]  = criatura_nombre
        st.session_state["orientacion_nd"]     = orientacion_nd
        st.session_state["test_universo_done"] = True
        st.session_state["test_dim_done"]      = True

        # ── Confirmación ──
        st.markdown(f"""
        <div style="background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.3);
                    border-radius:10px;padding:1.5rem;margin-top:1rem;text-align:center;">
            <p style="font-family:'Cinzel',serif;color:#c9a84c;font-size:1.1rem;margin:0 0 0.5rem;">
                ✦ Saga recuperada
            </p>
            <p style="color:#e8e0d0;font-size:0.9rem;margin:0 0 0.3rem;">
                Universo: <strong>{universo_nombre}</strong>
            </p>
            <p style="color:#e8e0d0;font-size:0.9rem;margin:0 0 0.3rem;">
                Personaje: <strong>{personaje_nombre}</strong>
            </p>
            <p style="color:#e8e0d0;font-size:0.9rem;margin:0 0 0.3rem;">
                Criatura: <strong>{criatura_nombre}</strong>
            </p>
            {"<p style='color:#e8e0d0;font-size:0.9rem;margin:0;'>Orientación: <strong>" + " · ".join(orientacion_nd) + "</strong></p>" if orientacion_nd else "<p style='color:#9a9080;font-size:0.9rem;margin:0;'>Perfil neurotípico</p>"}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col2 = st.columns([1, 2, 1])[1]
        with col2:
            if st.button("ᚲ Ir a mis recursos →", use_container_width=True, key="btn_regreso_recursos"):
                st.session_state["_pagina_activa"] = "ᚲ  Comunicación"
                st.rerun()
