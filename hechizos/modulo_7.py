"""SEIÐR — Módulo 7: Orientación clínica"""

import streamlit as st
import pandas as pd

from modulo_3 import (
    cargar_recursos, filtrar_recursos_nd, _normalizar_nds,
    _bloque_recursos, _nota_pie
)


def mostrar_modulo_7(orientacion_nd=None):
    nds = _normalizar_nds(orientacion_nd)

    st.markdown("""
    <div style="text-align:center; margin-bottom:2rem;">
        <h2 style="font-family:'Cinzel',serif; color:#c9a84c; letter-spacing:0.1em;">
            ᛏ Orientación clínica
        </h2>
        <p style="color:#9a9080; font-size:0.95rem;">
            Módulo 7 · Tests, profesionales y recursos clínicos
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: rgba(74,127,165,0.1);
        border: 1px solid rgba(74,127,165,0.35);
        border-radius:10px;
        padding:1rem 1.2rem;
        margin-bottom:1.5rem;
    ">
        <p style="color:#e8e0d0; margin:0; font-size:0.9rem;">
            ℹ️ <strong>Seiðr no es una herramienta de diagnóstico.</strong>
            Los tests que aparecen aquí son de cribado orientativo.
            Un diagnóstico solo puede darlo un profesional cualificado.
        </p>
    </div>
    """, unsafe_allow_html=True)


    # ── Narrador contextual ──
    try:
        from narrador import get_narrador
        _universo_id = st.session_state.get("universo_elegido")
        _texto_narrador = get_narrador(_universo_id, "modulo_recursos")
        if _texto_narrador:
            st.markdown(
                f"<div style='background:rgba(201,168,76,0.06);border-left:3px solid #c9a84c;"
                f"border-radius:0 8px 8px 0;padding:1rem 1.5rem;margin:0 0 1.5rem;'>"
                f"<p style='color:#c9a84c;font-size:0.9rem;font-style:italic;margin:0;"
                f"line-height:1.7;'>{_texto_narrador}</p></div>",
                unsafe_allow_html=True
            )
    except Exception:
        pass
    if not nds:
        st.markdown("""
        <p style="color:#e8e0d0; text-align:center; margin-bottom:1.5rem;">
            Recursos clínicos generales disponibles para todos los perfiles.
        </p>
        """, unsafe_allow_html=True)
    else:
        nd_texto = " y ".join(f"**{nd}**" for nd in nds)
        st.markdown(
            f"<p style='color:#e8e0d0; text-align:center; margin-bottom:1.5rem;'>"
            f"Tests y recursos clínicos para tu perfil: {nd_texto}.</p>",
            unsafe_allow_html=True
        )

    df_recursos = cargar_recursos()
    if df_recursos.empty:
        st.info("No se encontraron recursos clínicos.")
        return

    df_filtrado = filtrar_recursos_nd(df_recursos, modulo=7, nds=nds)

    if df_filtrado.empty:
        df_filtrado = df_recursos[df_recursos["modulo"] == 7]

    # Tests primero en módulo 7
    tipos_orden = ["test", "asociacion", "herramienta", "tecnica", "recurso_material"]
    etiquetas = {
        "test":             "📋 Tests de cribado",
        "asociacion":       "🏛️ Asociaciones y profesionales",
        "herramienta":      "🛠️ Referencias clínicas",
        "tecnica":          "✨ Técnicas",
        "recurso_material": "📦 Recursos materiales",
    }

    for tipo in tipos_orden:
        subset = df_filtrado[df_filtrado["tipo"] == tipo] if "tipo" in df_filtrado.columns else pd.DataFrame()
        if subset.empty:
            continue
        st.markdown(
            f"<h4 style='font-family:\"Cinzel\",serif; color:#c9a84c; "
            f"margin-top:1.5rem; margin-bottom:0.5rem;'>{etiquetas[tipo]}</h4>",
            unsafe_allow_html=True
        )
        _bloque_recursos(subset)


    # ── Descarga PDF del módulo ──
    try:
        from generador_pdf import generar_pdf_modulo
        from modulo_3 import cargar_contenido as _cc, cargar_recursos as _cr
        _df_cont = _cc()
        _df_rec = _cr()
        _pdf = generar_pdf_modulo(
            modulo=7,
            orientacion_nd=nds,
            df_contenido=_df_cont,
            df_recursos=_df_rec,
        )
        st.download_button(
            label="📥 Descargar este módulo en PDF",
            data=_pdf,
            file_name=f"Seidr_Modulo_7.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="btn_pdf_7",
        )
    except Exception as e:
        pass

    _nota_pie()
