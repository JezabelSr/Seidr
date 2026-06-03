"""SEIÐR — Módulo 5: Tu forma de socializar"""

import streamlit as st
from modulo_3 import (
    cargar_contenido, cargar_recursos, obtener_contenido_nd,
    filtrar_recursos_nd, _normalizar_nds,
    _cabecera_modulo, _bloque_explicacion, _bloque_lista,
    _bloque_recursos, _aviso_nt, _nota_pie
)


def mostrar_modulo_5(orientacion_nd=None):
    nds = _normalizar_nds(orientacion_nd)

    _cabecera_modulo("ᛉ", "Tu forma de socializar", "Módulo 5 · Sociabilidad")
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


    df_contenido = cargar_contenido()
    df_recursos  = cargar_recursos()

    if not nds:
        _aviso_nt()
        _bloque_recursos(filtrar_recursos_nd(df_recursos, 5, []))
        _nota_pie()
        return

    for nd in nds:
        if len(nds) > 1:
            st.markdown(
                f"<h3 style='font-family:\"Cinzel\",serif; color:#c9a84c;"
                f"font-size:1rem; margin:1.5rem 0 0.8rem;'>◈ {nd}</h3>",
                unsafe_allow_html=True
            )

        contenido = obtener_contenido_nd(df_contenido, nd, modulo=5)
        if contenido:
            st.markdown(
                "<p style='font-family:\"Cinzel\",serif; color:#9a9080;"
                "font-size:0.8rem; letter-spacing:0.05em; margin-bottom:0.5rem;'>"
                "ASÍ FUNCIONA TU SOCIALIZACIÓN</p>",
                unsafe_allow_html=True
            )
            _bloque_explicacion(contenido["explicacion"])

            if contenido["tecnicas"]:
                _bloque_lista("Qué puedes hacer", "✦", contenido["tecnicas"])

            if contenido["adaptaciones"]:
                _bloque_lista("Qué puedes pedir a tu entorno social y familiar", "◈", contenido["adaptaciones"], color_borde="#4a7fa5")
        else:
            st.info(f"Contenido para {nd} no disponible aún.")

    df_rec_filtrado = filtrar_recursos_nd(df_recursos, 5, nds)
    if not df_rec_filtrado.empty:
        st.markdown("<hr style='border-color:#2a2a3a; margin:1.5rem 0;'>", unsafe_allow_html=True)
        _bloque_recursos(df_rec_filtrado)


    # ── Descarga PDF del módulo ──
    try:
        from generador_pdf import generar_pdf_modulo
        from modulo_3 import cargar_contenido as _cc, cargar_recursos as _cr
        _df_cont = _cc()
        _df_rec = _cr()
        _pdf = generar_pdf_modulo(
            modulo=5,
            orientacion_nd=nds,
            df_contenido=_df_cont,
            df_recursos=_df_rec,
        )
        st.download_button(
            label="Descargar este modulo en PDF",
            data=_pdf,
            file_name="Seidr_Modulo_5.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="btn_pdf_5",
        )
    except Exception:
        pass

        _nota_pie()
