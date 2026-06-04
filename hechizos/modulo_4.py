"""SEIÐR — Módulo 4: Tu forma de aprender"""

import streamlit as st
from modulo_3 import (
    cargar_contenido, cargar_recursos, obtener_contenido_nd,
    filtrar_recursos_nd, _normalizar_nds,
    _cabecera_modulo, _bloque_explicacion, _bloque_texto,
    _bloque_recursos, _aviso_nt, _nota_pie
)


def mostrar_modulo_4(orientacion_nd=None):
    nds = _normalizar_nds(orientacion_nd)

    _cabecera_modulo("ᚷ", "Tu forma de aprender", "Módulo 4 · Aprendizaje y Función Ejecutiva")

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
        contenido_nt = obtener_contenido_nd(df_contenido, "NT", modulo=4)
        if contenido_nt:
            label_nt = "<p style='font-family:Cinzel,serif; color:#9a9080; font-size:0.8rem; letter-spacing:0.05em; margin-bottom:0.5rem;'>ASÍ FUNCIONA TU APRENDIZAJE</p>"
            st.markdown(label_nt, unsafe_allow_html=True)
            _bloque_explicacion(contenido_nt["explicacion"])
            _bloque_texto("Cómo funciona mejor", "✦", contenido_nt["como_aprende"])
            _bloque_texto("Dificultades frecuentes", "◈", contenido_nt["dificultades"], color_borde="#9a9080")
            _bloque_texto("Tus fortalezas", "✧", contenido_nt["fortalezas"], color_borde="#4a7fa5")
            _bloque_texto("Qué puedes hacer", "⚔", contenido_nt["estrategias"])
            _bloque_texto("Herramientas de IA para ti", "⭐", contenido_nt["herramientas_ia"])
            _bloque_texto("Herramientas y recursos específicos", "🔧", contenido_nt["herramientas_especificas"])
            _bloque_texto("Qué puedes pedir a tu entorno", "◈", contenido_nt["adaptaciones"], color_borde="#4a7fa5")
            _bloque_texto("Kit de supervivencia", "🧭", contenido_nt["kit_supervivencia"], color_borde="#c9a84c")
        else:
            _aviso_nt()
        _bloque_recursos(filtrar_recursos_nd(df_recursos, 4, []))
        _nota_pie()
        return

    for nd in nds:
        if len(nds) > 1:
            st.markdown(
                f"<h3 style='font-family:\"Cinzel\",serif; color:#c9a84c;"
                f"font-size:1rem; margin:1.5rem 0 0.8rem;'>◈ {nd}</h3>",
                unsafe_allow_html=True
            )

        contenido = obtener_contenido_nd(df_contenido, nd, modulo=4)
        if contenido:
            st.markdown(
                "<p style='font-family:\"Cinzel\",serif; color:#9a9080;"
                "font-size:0.8rem; letter-spacing:0.05em; margin-bottom:0.5rem;'>"
                "ASÍ FUNCIONA TU APRENDIZAJE</p>",
                unsafe_allow_html=True
            )
            _bloque_explicacion(contenido["explicacion"])
            _bloque_texto("Cómo funciona mejor", "✦", contenido["como_aprende"])
            _bloque_texto("Dificultades frecuentes", "◈", contenido["dificultades"], color_borde="#9a9080")
            _bloque_texto("Tus fortalezas", "✧", contenido["fortalezas"], color_borde="#4a7fa5")
            _bloque_texto("Qué puedes hacer", "⚔", contenido["estrategias"])
            _bloque_texto("Herramientas de IA para ti", "⭐", contenido["herramientas_ia"])
            _bloque_texto("Herramientas y recursos específicos", "🔧", contenido["herramientas_especificas"])
            _bloque_texto("Qué puedes pedir a tu entorno", "◈", contenido["adaptaciones"], color_borde="#4a7fa5")
            _bloque_texto("Kit de supervivencia", "🧭", contenido["kit_supervivencia"], color_borde="#c9a84c")
        else:
            st.info(f"Contenido para {nd} no disponible aún.")

    df_rec_filtrado = filtrar_recursos_nd(df_recursos, 4, nds)
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
            modulo=4,
            orientacion_nd=nds,
            df_contenido=_df_cont,
            df_recursos=_df_rec,
        )
        st.download_button(
            label="Descargar este modulo en PDF",
            data=_pdf,
            file_name="Seidr_Modulo_4.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="btn_pdf_4",
        )
    except Exception:
        pass

    _nota_pie()
