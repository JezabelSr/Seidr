"""
SEIÐR — Modo Profesional
Acceso directo a: criaturas + equivalencias reales | ND + recursos | personajes por universo
Sin necesidad de hacer los tests.
"""

import streamlit as st
import pandas as pd


# ── Carga de datos ────────────────────────────────────────────────────────────

def _cargar(ruta: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(ruta)
        if df.empty or len(df.columns) == 0:
            return pd.DataFrame()
        return df
    except Exception:
        return pd.DataFrame()


def _cargar_todos() -> dict:
    try:
        from db import (cargar_tabla, cargar_personajes, cargar_criaturas,
                        cargar_perfiles_nd, cargar_razas, cargar_recursos,
                        cargar_contenido_modulos)
        def _db(fn, fallback):
            try:
                df = fn()
                return df if not df.empty else _cargar(fallback)
            except Exception:
                return _cargar(fallback)
        return {
            "personajes":  _db(cargar_personajes,        "universos/personajes.csv"),
            "criaturas":   _db(cargar_criaturas,         "universos/criaturas.csv"),
            "universos":   _db(lambda: cargar_tabla("universos"), "universos/universos.csv"),
            "nd_clinicos": _db(cargar_perfiles_nd,       "universos/perfiles_nd_clinicos.csv"),
            "razas":       _db(cargar_razas,             "universos/razas_akc_limpio.csv"),
            "recursos":    _db(cargar_recursos,          "universos/recursos_reales/recursos.csv"),
            "contenido":   _db(cargar_contenido_modulos, "universos/contenido_modulos.csv"),
        }
    except Exception:
        return {
            "personajes":  _cargar("universos/personajes.csv"),
            "criaturas":   _cargar("universos/criaturas.csv"),
            "universos":   _cargar("universos/universos.csv"),
            "nd_clinicos": _cargar("universos/perfiles_nd_clinicos.csv"),
            "razas":       _cargar("universos/razas_akc_limpio.csv"),
            "recursos":    _cargar("universos/recursos_reales/recursos.csv"),
            "contenido":   _cargar("universos/contenido_modulos.csv"),
        }


NOMBRES_UNIVERSOS = {
    1: "Harry Potter",
    2: "La Brújula Dorada",
    3: "Pokémon",
    4: "Studio Ghibli",
    5: "Cómo entrenar a tu dragón",
    6: "Disney/Pixar",
}

DIMENSIONES = [
    ("hiperfoco",            "Hiperfoco"),
    ("regulacion_emocional", "Reg. emocional"),
    ("sensorialidad",        "Sensorialidad"),
    ("comunicacion",         "Comunicación"),
    ("aprendizaje",          "Aprendizaje"),
    ("sociabilidad",         "Sociabilidad"),
    ("propiocepcion",        "Propiocepción"),
    ("funcion_ejecutiva",    "F. ejecutiva"),
]

MODULOS_NOMBRES = {3: "Comunicación", 4: "Aprendizaje", 5: "Sociabilidad", 6: "Tu cuerpo", 7: "Clínico"}


# ── Helpers de UI ─────────────────────────────────────────────────────────────

def _titulo_seccion(texto: str):
    st.markdown(
        f"<p style='font-family:\"Cinzel\",serif; color:#c9a84c; "
        f"font-size:0.8rem; letter-spacing:0.1em; margin:1.5rem 0 0.5rem;'>"
        f"{texto}</p>",
        unsafe_allow_html=True
    )


def _card_oscura(contenido_html: str, borde: str = "#c9a84c"):
    st.markdown(
        f"<div style='background:rgba(20,20,30,0.92); border:1px solid rgba(201,168,76,0.2); "
        f"border-left:3px solid {borde}; border-radius:0 8px 8px 0; "
        f"padding:1rem 1.2rem; margin-bottom:0.8rem;'>{contenido_html}</div>",
        unsafe_allow_html=True
    )


def _barra_dimension(nombre: str, valor: float):
    pct = int((valor / 5) * 100)
    return (
        f"<div style='margin-bottom:0.4rem;'>"
        f"<div style='display:flex; justify-content:space-between; margin-bottom:0.1rem;'>"
        f"<span style='color:#9a9080; font-size:0.75rem;'>{nombre}</span>"
        f"<span style='color:#9a9080; font-size:0.75rem;'>{valor:.1f}</span></div>"
        f"<div style='background:#2a2a3a; border-radius:2px; height:4px;'>"
        f"<div style='background:#c9a84c; width:{pct}%; height:4px; border-radius:2px;'></div>"
        f"</div></div>"
    )


def _imagen(url: str, alto: int = 120):
    if not url or str(url).strip() in ("", "nan"):
        return
    try:
        from pathlib import Path
        p = Path(str(url))
        if p.exists():
            st.image(str(p), width=alto)
        else:
            st.image(str(url), width=alto)
    except Exception:
        pass


# ── Tab 1: Por Neurodivergencia ───────────────────────────────────────────────

def _tab_por_nd(datos: dict):
    df_nd        = datos["nd_clinicos"]
    df_criaturas = datos["criaturas"]
    df_razas    = datos["razas"]
    df_recursos = datos["recursos"]
    df_contenido = datos["contenido"]
    df_personajes = datos["personajes"]

    if df_nd.empty:
        st.warning("No se encontró perfiles_nd_clinicos.csv")
        return

    nds_disponibles = sorted(df_nd["nombre"].dropna().unique().tolist())
    nd_elegida = st.selectbox(
        "Selecciona una neurodivergencia",
        nds_disponibles,
        key="prof_nd_selector"
    )

    if not nd_elegida:
        return

    fila_nd = df_nd[df_nd["nombre"] == nd_elegida].iloc[0] if not df_nd[df_nd["nombre"] == nd_elegida].empty else None

    # ── Perfil clínico ──
    _titulo_seccion("PERFIL CLÍNICO")
    if fila_nd is not None:
        explicacion = str(fila_nd.get("explicacion_perfil", ""))
        if explicacion and explicacion != "nan":
            _card_oscura(f"<p style='color:#e8e0d0; font-size:0.9rem; margin:0; line-height:1.6;'>{explicacion}</p>")

        # Rangos de dimensiones
        dims_html = "<div style='display:grid; grid-template-columns:1fr 1fr; gap:0.3rem 1.5rem; margin-top:0.5rem;'>"
        for col_key, col_nombre in [
            ("hiperfoco", "Hiperfoco"), ("reg_emocional", "Reg. emocional"),
            ("sensorialidad", "Sensorialidad"), ("comunicacion", "Comunicación"),
            ("aprendizaje", "Aprendizaje"), ("sociabilidad", "Sociabilidad"),
            ("propiocepcion", "Propiocepción"), ("f_ejecutiva", "F. ejecutiva"),
        ]:
            min_v = fila_nd.get(f"{col_key}_min", "")
            max_v = fila_nd.get(f"{col_key}_max", "")
            medio = fila_nd.get(f"{col_key}_medio", "")
            if str(min_v) != "nan" and str(max_v) != "nan":
                dims_html += (
                    f"<div style='margin-bottom:0.3rem;'>"
                    f"<span style='color:#9a9080; font-size:0.75rem;'>{col_nombre}: </span>"
                    f"<span style='color:#c9a84c; font-size:0.75rem;'>{min_v}–{max_v}</span>"
                    f"<span style='color:#555; font-size:0.72rem;'> (medio: {medio})</span>"
                    f"</div>"
                )
        dims_html += "</div>"
        st.markdown(
            f"<div style='background:rgba(20,20,30,0.88); border:1px solid rgba(201,168,76,0.15); "
            f"border-radius:8px; padding:1rem 1.2rem; margin-bottom:1rem;'>"
            f"<p style='font-family:\"Cinzel\",serif; color:#9a9080; font-size:0.75rem; "
            f"letter-spacing:0.05em; margin:0 0 0.5rem;'>RANGOS POR DIMENSIÓN (0–5)</p>"
            f"{dims_html}</div>",
            unsafe_allow_html=True
        )

    # ── Personajes con esa ND (orientación) ──
    _titulo_seccion("PERSONAJES ASOCIADOS")
    # Buscamos personajes cuya orientación incluye esta ND
    # Como no hay columna de ND en personajes, usamos criaturas del mismo universo como proxy
    # Mostramos los 3 personajes más cercanos al perfil medio de la ND si hay datos
    if fila_nd is not None and not df_personajes.empty:
        try:
            perfil_medio = {
                "hiperfoco":            float(fila_nd.get("hiperfoco_medio", 2.5)),
                "regulacion_emocional": float(fila_nd.get("reg_emocional_medio", 2.5)),
                "sensorialidad":        float(fila_nd.get("sensorialidad_medio", 2.5)),
                "comunicacion":         float(fila_nd.get("comunicacion_medio", 2.5)),
                "aprendizaje":          float(fila_nd.get("aprendizaje_medio", 2.5)),
                "sociabilidad":         float(fila_nd.get("sociabilidad_medio", 2.5)),
                "propiocepcion":        float(fila_nd.get("propiocepcion_medio", 2.5)),
                "funcion_ejecutiva":    float(fila_nd.get("f_ejecutiva_medio", 2.5)),
            }
            import numpy as np
            distancias = []
            for _, p in df_personajes.iterrows():
                try:
                    dist = np.sqrt(sum(
                        (perfil_medio[d] - float(p[d])) ** 2
                        for d in perfil_medio
                    ))
                    distancias.append((dist, p))
                except Exception:
                    continue
            distancias.sort(key=lambda x: x[0])
            top3 = [p for _, p in distancias[:3]]

            cols = st.columns(3)
            for i, p in enumerate(top3):
                with cols[i]:
                    universo_nombre = NOMBRES_UNIVERSOS.get(int(p.get("universo_id", 0)), "")
                    _imagen(p.get("url_imagen", ""), alto=100)
                    st.markdown(
                        f"<p style='color:#c9a84c; font-size:0.85rem; margin:0.3rem 0 0;'>{p['nombre']}</p>"
                        f"<p style='color:#9a9080; font-size:0.75rem; margin:0;'>{universo_nombre}</p>",
                        unsafe_allow_html=True
                    )
        except Exception as e:
            st.caption(f"Personajes no disponibles: {e}")

    # ── Criaturas asociadas ──
    _titulo_seccion("CRIATURAS Y EQUIVALENCIAS REALES")
    if not df_criaturas.empty and not df_razas.empty:
        # Criaturas cuya raza real puede relacionarse con la ND
        # Mostramos una muestra de criaturas de todos los universos con su raza real
        muestra = df_criaturas.dropna(subset=["raza_real_id"]).head(6)
        if not muestra.empty:
            cols = st.columns(3)
            for i, (_, c) in enumerate(muestra.iterrows()):
                with cols[i % 3]:
                    raza_id = c.get("raza_real_id", "")
                    raza_nombre = ""
                    url_raza = ""
                    try:
                        raza_id_int = int(float(str(raza_id))) - 1
                        if 0 <= raza_id_int < len(df_razas):
                            raza_row = df_razas.iloc[raza_id_int]
                            raza_nombre = str(raza_row.get("breed", ""))
                            url_raza = str(raza_row.get("url_imagen", ""))
                    except Exception:
                        raza_nombre = str(raza_id)

                    universo_nombre = NOMBRES_UNIVERSOS.get(int(c.get("universo_id", 0)), "")
                    equiv = str(c.get("explicacion_equivalencia", ""))
                    if equiv == "nan":
                        equiv = ""
                    # Nombre de raza desde el texto de equivalencia
                    if equiv and " — " in equiv:
                        raza_nombre = equiv.split(" — ")[0].strip()
                    elif equiv and " - " in equiv:
                        raza_nombre = equiv.split(" - ")[0].strip()

                    st.markdown(
                        f"<div style='background:rgba(20,20,30,0.88); border:1px solid rgba(201,168,76,0.15); "
                        f"border-radius:8px; padding:0.8rem; margin-bottom:0.5rem;'>"
                        f"<p style='color:#c9a84c; font-size:0.85rem; margin:0 0 0.2rem;'>{c['nombre']}</p>"
                        f"<p style='color:#9a9080; font-size:0.75rem; margin:0 0 0.3rem;'>{universo_nombre}</p>"
                        f"{'<p style=\"color:#4a7fa5; font-size:0.75rem; margin:0 0 0.2rem;\">≈ ' + raza_nombre + '</p>' if raza_nombre else ''}"
                        f"{'<p style=\"color:#9a9080; font-size:0.72rem; margin:0; line-height:1.4;\">' + equiv[:120] + ('…' if len(equiv) > 120 else '') + '</p>' if equiv else ''}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

    # ── Recursos y contenido por módulo ──
    _titulo_seccion("RECURSOS Y GUÍAS POR MÓDULO")

    tabs_modulos = st.tabs(["Comunicación", "Aprendizaje", "Sociabilidad", "Tu cuerpo", "Clínico"])

    for tab_i, (tab, mod_num) in enumerate(zip(tabs_modulos, [3, 4, 5, 6, 7])):
        with tab:
            # Contenido guía (módulos 3-6)
            if mod_num <= 6 and not df_contenido.empty:
                fila_cont = df_contenido[
                    (df_contenido["nd"] == nd_elegida) & (df_contenido["modulo"] == mod_num)
                ]
                if not fila_cont.empty:
                    row = fila_cont.iloc[0]
                    explicacion = str(row.get("explicacion_perfil", ""))
                    if explicacion and explicacion != "nan":
                        st.markdown(
                            f"<p style='color:#e8e0d0; font-size:0.88rem; "
                            f"line-height:1.6; margin-bottom:0.8rem;'>{explicacion}</p>",
                            unsafe_allow_html=True
                        )
                    tecnicas = [t.strip() for t in str(row.get("tecnicas", "")).split("|") if t.strip()]
                    if tecnicas:
                        items = "".join(f"<li style='color:#e8e0d0; font-size:0.85rem; margin-bottom:0.3rem;'>{t}</li>" for t in tecnicas)
                        st.markdown(
                            f"<p style='color:#c9a84c; font-size:0.8rem; margin-bottom:0.3rem;'>✦ Técnicas</p>"
                            f"<ul style='padding-left:1.2rem; margin:0 0 0.8rem;'>{items}</ul>",
                            unsafe_allow_html=True
                        )
                    adaptaciones = [a.strip() for a in str(row.get("adaptaciones", "")).split("|") if a.strip()]
                    if adaptaciones:
                        items = "".join(f"<li style='color:#e8e0d0; font-size:0.85rem; margin-bottom:0.3rem;'>{a}</li>" for a in adaptaciones)
                        st.markdown(
                            f"<p style='color:#4a7fa5; font-size:0.8rem; margin-bottom:0.3rem;'>◈ Adaptaciones</p>"
                            f"<ul style='padding-left:1.2rem; margin:0;'>{items}</ul>",
                            unsafe_allow_html=True
                        )

            # Recursos (todos los módulos)
            if not df_recursos.empty:
                _nd_buscar = nd_elegida  # captura explícita para evitar problemas de closure
                df_rec = df_recursos[
                    (df_recursos["modulo"] == mod_num) &
                    df_recursos["neurodivergencias"].apply(
                        lambda c: False if pd.isna(c)
                        else _nd_buscar in [n.strip() for n in str(c).split(",")]
                    )
                ]
                if not df_rec.empty:
                    st.markdown(
                        "<p style='color:#9a9080; font-size:0.78rem; "
                        "margin: 1rem 0 0.4rem;'>🔗 Recursos</p>",
                        unsafe_allow_html=True
                    )
                    for _, r in df_rec.iterrows():
                        gratuito = str(r.get("gratuito", "")).strip().lower() in ("true","1","sí","si")
                        tag = "🟢" if gratuito else "🔴"
                        url = r.get("url", "")
                        st.markdown(
                            f"<div style='background:rgba(15,15,22,0.8); border:1px solid rgba(201,168,76,0.1); "
                            f"border-radius:6px; padding:0.6rem 0.9rem; margin-bottom:0.4rem;'>"
                            f"<span style='color:#c9a84c; font-size:0.82rem;'>{r.get('nombre','')} {tag}</span>"
                            f"<p style='color:#9a9080; font-size:0.78rem; margin:0.1rem 0 0;'>{r.get('descripcion','')}</p>"
                            f"{'<a href=\"' + url + '\" target=\"_blank\" style=\"color:#4a7fa5; font-size:0.78rem;\">Visitar →</a>' if url else ''}"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                elif mod_num <= 6:
                    st.caption("Sin recursos específicos para esta ND en este módulo.")


# ── Tab 2: Por Universo ───────────────────────────────────────────────────────

def _tab_por_universo(datos: dict):
    df_personajes = datos["personajes"]
    df_criaturas  = datos["criaturas"]
    df_razas      = datos["razas"]

    universo_opciones = list(NOMBRES_UNIVERSOS.values())
    universo_elegido_nombre = st.selectbox(
        "Selecciona un universo",
        universo_opciones,
        key="prof_universo_selector"
    )
    universo_id = {v: k for k, v in NOMBRES_UNIVERSOS.items()}.get(universo_elegido_nombre)

    if not universo_id:
        return

    # ── Personajes ──
    _titulo_seccion("PERSONAJES")
    df_pers_u = df_personajes[df_personajes["universo_id"] == universo_id] if not df_personajes.empty else pd.DataFrame()

    if df_pers_u.empty:
        st.caption("Sin personajes disponibles para este universo.")
    else:
        for _, p in df_pers_u.iterrows():
            with st.expander(f"{p['nombre']}  ·  {p.get('rol', '')}"):
                col_img, col_info = st.columns([1, 3])
                with col_img:
                    _imagen(p.get("url_imagen", ""), alto=100)
                with col_info:
                    desc = str(p.get("descripcion", ""))
                    if desc and desc != "nan":
                        st.markdown(
                            f"<p style='color:#e8e0d0; font-size:0.88rem; "
                            f"line-height:1.5; margin-bottom:0.6rem;'>{desc}</p>",
                            unsafe_allow_html=True
                        )
                    # Perfil de dimensiones
                    barras = ""
                    for col_key, col_nombre in DIMENSIONES:
                        try:
                            valor = float(p.get(col_key, 0))
                            barras += _barra_dimension(col_nombre, valor)
                        except Exception:
                            pass
                    if barras:
                        st.markdown(
                            f"<div style='background:rgba(20,20,30,0.88); "
                            f"border:1px solid rgba(201,168,76,0.12); border-radius:6px; "
                            f"padding:0.8rem;'>{barras}</div>",
                            unsafe_allow_html=True
                        )
                    just = str(p.get("justificacion", ""))
                    if just and just != "nan":
                        st.markdown(
                            f"<p style='color:#9a9080; font-size:0.78rem; "
                            f"margin-top:0.5rem; font-style:italic;'>{just}</p>",
                            unsafe_allow_html=True
                        )

    # ── Criaturas ──
    _titulo_seccion("CRIATURAS Y EQUIVALENCIAS REALES")
    df_crit_u = df_criaturas[df_criaturas["universo_id"] == universo_id] if not df_criaturas.empty else pd.DataFrame()

    if df_crit_u.empty:
        st.caption("Sin criaturas disponibles para este universo.")
    else:
        cols = st.columns(3)
        for i, (_, c) in enumerate(df_crit_u.iterrows()):
            with cols[i % 3]:
                raza_id = c.get("raza_real_id", "")
                raza_nombre = ""
                url_raza = ""
                try:
                    raza_id_int = int(float(str(raza_id))) - 1
                    if 0 <= raza_id_int < len(df_razas) and not df_razas.empty:
                        raza_row = df_razas.iloc[raza_id_int]
                        raza_nombre = str(raza_row.get("breed", ""))
                        url_raza = str(raza_row.get("url_imagen", ""))
                except Exception:
                    raza_nombre = str(raza_id) if str(raza_id) != "nan" else ""

                equiv = str(c.get("explicacion_equivalencia", ""))
                if equiv == "nan":
                    equiv = ""
                desc = str(c.get("descripcion", ""))
                if desc == "nan":
                    desc = ""
                # Nombre de raza desde el texto de equivalencia
                if equiv and " — " in equiv:
                    raza_nombre = equiv.split(" — ")[0].strip()
                elif equiv and " - " in equiv:
                    raza_nombre = equiv.split(" - ")[0].strip()

                st.markdown(
                    f"<div style='background:rgba(20,20,30,0.92); "
                    f"border:1px solid rgba(201,168,76,0.18); border-radius:8px; "
                    f"padding:0.9rem 1rem; margin-bottom:0.6rem;'>",
                    unsafe_allow_html=True
                )
                _imagen(c.get("url_imagen", ""), alto=90)
                st.markdown(
                    f"<p style='color:#c9a84c; font-size:0.88rem; margin:0.4rem 0 0.1rem;'>{c['nombre']}</p>"
                    f"{'<p style=\"color:#4a7fa5; font-size:0.78rem; margin:0 0 0.2rem;\">≈ ' + raza_nombre + '</p>' if raza_nombre else ''}"
                    f"{'<p style=\"color:#9a9080; font-size:0.78rem; margin:0; line-height:1.4;\">' + equiv + '</p>' if equiv else ''}"
                    f"{'<p style=\"color:#9a9080; font-size:0.75rem; margin:0.3rem 0 0; font-style:italic;\">' + desc[:100] + ('…' if len(desc) > 100 else '') + '</p>' if desc else ''}"
                    f"</div>",
                    unsafe_allow_html=True
                )


# ── Página principal ──────────────────────────────────────────────────────────

def pagina_profesional():
    st.markdown("""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <h2 style="font-family:'Cinzel',serif; color:#c9a84c; letter-spacing:0.1em;">
            ⚕ Modo profesional
        </h2>
        <p style="color:#9a9080; font-size:0.9rem;">
            Acceso directo a toda la información del proyecto sin realizar los tests
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(74,127,165,0.1); border:1px solid rgba(74,127,165,0.3);
                border-radius:8px; padding:0.8rem 1.2rem; margin-bottom:1.5rem;">
        <p style="color:#e8e0d0; font-size:0.85rem; margin:0;">
            ℹ️ Este modo es para profesionales (psicólogos, pedagogos, orientadores, TO...)
            que quieran explorar los contenidos de Seiðr sin pasar por el flujo de usuario.
            Toda la información sigue siendo orientativa y no diagnóstica.
        </p>
    </div>
    """, unsafe_allow_html=True)

    datos = _cargar_todos()

    tab_nd, tab_universo = st.tabs(["Por neurodivergencia", "Por universo"])

    with tab_nd:
        _tab_por_nd(datos)

    with tab_universo:
        _tab_por_universo(datos)
