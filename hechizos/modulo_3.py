"""
SEIÐR — Módulo 3: Tu forma de comunicarte
Lee contenido de universos/contenido_modulos.csv
Los enlaces del CSV de recursos van al final como "si quieres profundizar"
"""

import streamlit as st
import pandas as pd


# ── Helpers compartidos (importados por módulos 4-6) ──────────────────────────

def cargar_contenido(ruta: str = "universos/contenido_modulos.csv") -> pd.DataFrame:
    """Lee contenido_modulos desde SQLite (con fallback a CSV)."""
    try:
        from db import cargar_contenido_modulos
        df = cargar_contenido_modulos()
        if not df.empty:
            return df
    except Exception:
        pass
    # Fallback a CSV
    try:
        df = pd.read_csv(ruta, encoding="utf-8-sig")
        df.columns = [c.strip().lstrip("\ufeff") for c in df.columns]
        return df
    except Exception:
        return pd.DataFrame()


def cargar_recursos(ruta: str = "universos/recursos_reales/recursos.csv") -> pd.DataFrame:
    """Lee recursos desde SQLite (con fallback a CSV)."""
    try:
        from db import cargar_recursos as _cargar_recursos_db
        df = _cargar_recursos_db()
        if not df.empty:
            return df
    except Exception:
        pass
    # Fallback a CSV
    try:
        return pd.read_csv(ruta)
    except Exception:
        return pd.DataFrame()


def obtener_contenido_nd(df: pd.DataFrame, nd: str, modulo: int) -> dict | None:
    """Devuelve el dict de contenido para una ND y módulo concretos."""
    fila = df[(df["nd"] == nd) & (df["modulo"] == modulo)]
    if fila.empty:
        return None
    row = fila.iloc[0]
    return {
        "explicacion": str(row.get("explicacion_perfil", "")),
        "tecnicas":    [t.strip() for t in str(row.get("tecnicas", "")).split("|") if t.strip()],
        "adaptaciones":[a.strip() for a in str(row.get("adaptaciones", "")).split("|") if a.strip()],
    }


def filtrar_recursos_nd(df: pd.DataFrame, modulo: int, nds: list[str]) -> pd.DataFrame:
    """Filtra recursos por módulo y lista de NDs."""
    df_mod = df[df["modulo"] == modulo].copy()
    if not nds:
        return df_mod
    def coincide(celda):
        if pd.isna(celda):
            return False
        return any(nd in [n.strip() for n in str(celda).split(",")] for nd in nds)
    return df_mod[df_mod["neurodivergencias"].apply(coincide)]


def _normalizar_nds(orientacion_nd) -> list[str]:
    if orientacion_nd is None:
        return []
    if isinstance(orientacion_nd, str):
        return [orientacion_nd.strip()] if orientacion_nd.strip() else []
    if isinstance(orientacion_nd, list):
        return [nd for nd in orientacion_nd if nd and str(nd).strip()]
    return []


# ── Bloques de UI ─────────────────────────────────────────────────────────────

def _bloque_explicacion(texto: str):
    st.markdown(f"""
    <div style="
        background: rgba(20,20,30,0.92);
        border-left: 3px solid #c9a84c;
        border-radius: 0 8px 8px 0;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.2rem;
    ">
        <p style="color:#e8e0d0; font-size:0.95rem; line-height:1.7; margin:0;">{texto}</p>
    </div>
    """, unsafe_allow_html=True)


def _bloque_lista(titulo: str, icono: str, items: list[str], color_borde: str = "#c9a84c"):
    items_html = "".join(
        f"<li style='color:#e8e0d0; font-size:0.9rem; line-height:1.6; margin-bottom:0.5rem;'>{it}</li>"
        for it in items
    )
    st.markdown(f"""
    <div style="
        background: rgba(20,20,30,0.88);
        border: 1px solid rgba(201,168,76,0.2);
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    ">
        <p style="font-family:'Cinzel',serif; color:{color_borde};
                  font-size:0.95rem; margin:0 0 0.8rem; letter-spacing:0.05em;">
            {icono} {titulo}
        </p>
        <ul style="margin:0; padding-left:1.2rem;">{items_html}</ul>
    </div>
    """, unsafe_allow_html=True)


def _bloque_recursos(df_recursos: pd.DataFrame):
    if df_recursos.empty:
        return
    st.markdown("""
    <p style="font-family:'Cinzel',serif; color:#9a9080;
              font-size:0.85rem; margin: 1.5rem 0 0.5rem; letter-spacing:0.05em;">
        🔗 Si quieres profundizar
    </p>
    """, unsafe_allow_html=True)
    for _, row in df_recursos.iterrows():
        nombre = row.get("nombre", "")
        desc   = row.get("descripcion", "")
        url    = row.get("url", "")
        gratuito = str(row.get("gratuito", "")).strip().lower() in ("true", "1", "sí", "si")
        tag    = "🟢" if gratuito else "🔴"
        st.markdown(f"""
        <div style="
            background: rgba(15,15,22,0.7);
            border: 1px solid rgba(201,168,76,0.12);
            border-radius: 6px;
            padding: 0.7rem 1rem;
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div>
                <span style="color:#c9a84c; font-size:0.85rem;">{nombre}</span>
                <span style="color:#9a9080; font-size:0.78rem; margin-left:0.5rem;">{tag}</span>
                <p style="color:#9a9080; font-size:0.8rem; margin:0.2rem 0 0;">{desc}</p>
            </div>
            {"<a href='" + url + "' target='_blank' style='color:#4a7fa5; font-size:0.8rem; white-space:nowrap; margin-left:1rem;'>Visitar →</a>" if url else ""}
        </div>
        """, unsafe_allow_html=True)


def _cabecera_modulo(runa: str, titulo: str, subtitulo: str):
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <h2 style="font-family:'Cinzel',serif; color:#c9a84c; letter-spacing:0.1em;">
            {runa} {titulo}
        </h2>
        <p style="color:#9a9080; font-size:0.9rem;">{subtitulo}</p>
    </div>
    """, unsafe_allow_html=True)


def _aviso_nt():
    st.markdown("""
    <div style="
        background: rgba(74,127,165,0.1);
        border: 1px solid rgba(74,127,165,0.3);
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 1.5rem;
    ">
        <p style="color:#e8e0d0; font-size:0.9rem; margin:0;">
            Tu perfil no muestra rasgos compatibles con ningún patrón de neurodivergencia de forma significativa.
            Aun así, aquí tienes recursos generales que pueden ser útiles.
        </p>
    </div>
    """, unsafe_allow_html=True)


def _nota_pie():
    st.markdown("""
    <p style="color:#555; font-size:0.75rem; text-align:center; margin-top:2rem;">
        ⚠️ Este contenido es orientativo y no sustituye la valoración de un profesional.
    </p>
    """, unsafe_allow_html=True)


# ── Función principal módulo 3 ────────────────────────────────────────────────

def mostrar_modulo_3(orientacion_nd=None):
    nds = _normalizar_nds(orientacion_nd)

    _cabecera_modulo("ᚲ", "Tu forma de comunicarte", "Módulo 3 · Comunicación")
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
        _bloque_recursos(filtrar_recursos_nd(df_recursos, 3, []))
        _nota_pie()
        return

    for nd in nds:
        if len(nds) > 1:
            st.markdown(
                f"<h3 style='font-family:\"Cinzel\",serif; color:#c9a84c;"
                f"font-size:1rem; margin:1.5rem 0 0.8rem;'>◈ {nd}</h3>",
                unsafe_allow_html=True
            )

        contenido = obtener_contenido_nd(df_contenido, nd, modulo=3)
        if contenido:
            st.markdown(
                "<p style='font-family:\"Cinzel\",serif; color:#9a9080;"
                "font-size:0.8rem; letter-spacing:0.05em; margin-bottom:0.5rem;'>"
                "ASÍ FUNCIONA TU COMUNICACIÓN</p>",
                unsafe_allow_html=True
            )
            _bloque_explicacion(contenido["explicacion"])

            if contenido["tecnicas"]:
                _bloque_lista("Qué puedes hacer", "✦", contenido["tecnicas"])

            if contenido["adaptaciones"]:
                _bloque_lista("Qué puedes pedir a tu entorno", "◈", contenido["adaptaciones"], color_borde="#4a7fa5")
        else:
            st.info(f"Contenido para {nd} no disponible aún.")

    # Recursos al final, discretos
    df_rec_filtrado = filtrar_recursos_nd(df_recursos, 3, nds)
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
            modulo=3,
            orientacion_nd=nds,
            df_contenido=_df_cont,
            df_recursos=_df_rec,
        )
        st.download_button(
            label="Descargar este modulo en PDF",
            data=_pdf,
            file_name="Seidr_Modulo_3.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="btn_pdf_3",
        )
    except Exception:
        pass

        _nota_pie()
