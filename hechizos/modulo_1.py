"""
SEIÐR — Módulo 1: Tu perfil
24 preguntas en el lenguaje del universo → perfil de 8 dimensiones → personaje más cercano
"""

import streamlit as st
import pandas as pd
import numpy as np

DIMENSIONES = [
    "hiperfoco", "regulacion_emocional", "sensorialidad", "comunicacion",
    "aprendizaje", "sociabilidad", "propiocepcion", "funcion_ejecutiva"
]

NOMBRES_DIMENSIONES = {
    "hiperfoco":            "Hiperfoco",
    "regulacion_emocional": "Regulación emocional",
    "sensorialidad":        "Sensorialidad",
    "comunicacion":         "Comunicación",
    "aprendizaje":          "Aprendizaje",
    "sociabilidad":         "Sociabilidad",
    "propiocepcion":        "Propiocepción",
    "funcion_ejecutiva":    "Función ejecutiva",
}

DESCRIPCIONES_DIMENSIONES = {
    "hiperfoco":            "Intensidad y concentración en intereses específicos",
    "regulacion_emocional": "Cómo gestionas y expresas tus emociones",
    "sensorialidad":        "Cómo procesas el entorno sensorial",
    "comunicacion":         "Tu estilo y forma de expresarte",
    "aprendizaje":          "Cómo absorbes y procesas la información",
    "sociabilidad":         "Cómo te relacionas con los demás",
    "propiocepcion":        "Conciencia y necesidades de tu propio cuerpo",
    "funcion_ejecutiva":    "Planificación, organización e inicio de tareas",
}


@st.cache_data
def cargar_preguntas_modulo1(universo_id: int):
    try:
        df = pd.read_csv("universos/preguntas.csv", engine="python")
        return df[(df["universo_id"] == universo_id) & (df["modulo"] == 1)].reset_index(drop=True)
    except Exception:
        return pd.DataFrame()


@st.cache_data
def cargar_personajes(universo_id: int):
    try:
        df = pd.read_csv("universos/personajes.csv", engine="python")
        return df[df["universo_id"] == universo_id].reset_index(drop=True)
    except Exception:
        return pd.DataFrame()


def get_opciones(row):
    opciones = []
    for letra in ["a", "b", "c", "d", "e"]:
        txt = row.get(f"opcion_{letra}", "")
        pun = row.get(f"puntuacion_{letra}", "")
        if pd.notna(txt) and str(txt).strip() and pd.notna(pun) and str(pun).strip():
            try:
                opciones.append({"texto": str(txt).strip(), "puntuacion": float(pun)})
            except ValueError:
                pass
    return opciones


def calcular_perfil(respuestas: dict) -> dict:
    """Calcula la puntuación media por dimensión."""
    perfil = {}
    for dim in DIMENSIONES:
        valores = respuestas.get(dim, [])
        perfil[dim] = round(np.mean(valores), 2) if valores else 0.0
    return perfil


def encontrar_personaje(perfil: dict, personajes: pd.DataFrame) -> pd.Series:
    """Encuentra el personaje con perfil más cercano usando distancia euclidiana."""
    min_dist = float("inf")
    mejor = None
    for _, row in personajes.iterrows():
        try:
            dist = np.sqrt(sum(
                (float(perfil[d]) - float(row[d])) ** 2
                for d in DIMENSIONES
            ))
            if dist < min_dist:
                min_dist = dist
                mejor = row
        except Exception:
            continue
    return mejor


def cargar_imagen(url: str, nombre: str = ""):
    """Muestra una imagen desde ruta local o URL."""
    if not url or str(url).strip() in ("", "nan"):
        st.markdown(
            f"<div style='background:#1a1a28;border:1px solid #2a2a3a;"
            f"border-radius:4px;padding:2rem;text-align:center;color:#9a9080;'>"
            f"ᚱ</div>",
            unsafe_allow_html=True
        )
        return
    try:
        from pathlib import Path
        p = Path(url)
        if p.exists():
            st.image(str(p), use_container_width=True)
        else:
            st.image(url, use_container_width=True)
    except Exception:
        pass




def _raiz_progreso(idx_actual: int, total: int):
    """Barra de progreso con forma de raíz nórdica."""
    progreso = idx_actual / total if total > 0 else 0
    x_ini, x_fin, yt = 40, 620, 72
    ancho = x_fin - x_ini
    x_actual = x_ini + int(ancho * progreso)
    n = 6
    lineas = []
    mid = x_ini + ancho // 2
    lineas.append(
        f'<path d="M {x_ini} {yt} Q {x_ini+ancho//4} {yt-3} {mid} {yt} ' +
        f'Q {x_ini+3*ancho//4} {yt+3} {x_fin} {yt}" ' +
        'stroke="#2a2a3a" stroke-width="2" fill="none" stroke-linecap="round"/>' 
    )
    if x_actual > x_ini + 4:
        xm = (x_ini + x_actual) // 2
        lineas.append(
            f'<path d="M {x_ini} {yt} Q {xm} {yt-3} {x_actual} {yt}" ' +
            'stroke="#c9a84c" stroke-width="3" fill="none" stroke-linecap="round"/>' 
        )
    for i in range(n):
        xr = x_ini + int(ancho * (i + 1) / (n + 1))
        arriba = (i % 2 == 0)
        activa = xr <= x_actual
        color_d = "#c9a84c88" if activa else "#1e1e2e"
        s1 = -1 if arriba else 1
        yr1 = yt + s1 * 30
        yr2 = yt + s1 * 50
        lineas.append(
            f'<path d="M {xr} {yt} Q {xr+4} {yt+s1*15} {xr+5} {yr1}" ' +
            f'stroke="{color_d}" stroke-width="1.5" fill="none" stroke-linecap="round"/>' 
        )
        lineas.append(
            f'<path d="M {xr+5} {yr1} Q {xr+14} {yr1+s1*10} {xr+20} {yr2}" ' +
            f'stroke="{color_d}" stroke-width="1" fill="none" stroke-linecap="round"/>' 
        )
        lineas.append(
            f'<path d="M {xr+5} {yr1} Q {xr-6} {yr1+s1*8} {xr-10} {yr2-s1*5}" ' +
            f'stroke="{color_d}" stroke-width="1" fill="none" stroke-linecap="round"/>' 
        )
        if activa:
            lineas.append(f'<circle cx="{xr+20}" cy="{yr2}" r="2.5" fill="#c9a84c"/>')
            lineas.append(f'<circle cx="{xr-10}" cy="{yr2-s1*5}" r="2" fill="#c9a84c"/>')
        if activa:
            lineas.append(f'<circle cx="{xr}" cy="{yt}" r="4" fill="#c9a84c"/>')
        else:
            lineas.append(f'<circle cx="{xr}" cy="{yt}" r="4" fill="#1a1a28" stroke="#2a2a3a" stroke-width="1"/>')
    lineas.append(f'<circle cx="{x_ini}" cy="{yt}" r="4" fill="#c9a84c"/>')
    if x_actual > x_ini + 12:
        lineas.append(f'<circle cx="{x_actual}" cy="{yt}" r="7" fill="#c9a84c"/>')
        lineas.append(f'<circle cx="{x_actual}" cy="{yt}" r="3.5" fill="#0d0d12"/>')
    lineas.append(
        f'<text x="330" y="16" text-anchor="middle" ' +
        f"font-family=\'Cinzel\',serif font-size=\'12\' fill=\'#9a9080\'>" +
        f'{idx_actual} / {total}</text>'
    )
    svg = (
        '<svg width="100%" viewBox="0 0 660 130" xmlns="http://www.w3.org/2000/svg" ' +
        'style="margin:0.5rem 0 1.2rem">' +
        "".join(lineas) + '</svg>'
    )
    st.markdown(svg, unsafe_allow_html=True)

def init_modulo1():
    defaults = {
        "m1_fase":          "test",
        "m1_idx":           0,
        "m1_respuestas":    {d: [] for d in DIMENSIONES},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def resetear_modulo1():
    """Limpia el estado del módulo 1 para empezar de cero."""
    st.session_state["m1_fase"]       = "test"
    st.session_state["m1_idx"]        = 0
    st.session_state["m1_respuestas"] = {d: [] for d in DIMENSIONES}
    st.session_state.pop("perfil_usuario", None)
    st.session_state.pop("personaje_asignado", None)
    st.session_state.pop("personaje_data", None)


def pagina_modulo_1():
    init_modulo1()

    universo_id = st.session_state.get("universo_elegido")
    universo_nombre = st.session_state.get("universo_nombre", "tu universo")

    if not universo_id:
        st.warning("Primero completa el test de universo.")
        return

    preguntas = cargar_preguntas_modulo1(universo_id)
    if preguntas.empty:
        st.error(f"No hay preguntas para el universo {universo_id}.")
        return

    fase = st.session_state.m1_fase

    # Cabecera
    st.markdown(
        f"<div style='text-align:center;padding:1.5rem 0 1rem'>"
        f"<h1 style=\"font-family:'Cinzel',serif;color:#c9a84c;"
        f"letter-spacing:0.1em;font-size:1.8rem\">ᚨ Tu perfil</h1>"
        f"<p style='color:#9a9080;font-style:italic'>"
        f"Universo: {universo_nombre}</p></div>",
        unsafe_allow_html=True
    )

    # ─── TEST ───
    if fase == "test":
        total = len(preguntas)
        idx = st.session_state.m1_idx

        if idx >= total:
            # Test completado — calcular perfil
            perfil = calcular_perfil(st.session_state.m1_respuestas)
            st.session_state.perfil_usuario = perfil
            personajes = cargar_personajes(universo_id)
            personaje = encontrar_personaje(perfil, personajes)
            if personaje is not None:
                st.session_state.personaje_asignado = personaje["nombre"]
                st.session_state.personaje_data = personaje.to_dict()
            st.session_state.test_dim_done = True
            st.session_state.m1_fase = "resultado"
            st.rerun()
            return

        row = preguntas.iloc[idx]
        dimension = str(row["dimension"]).strip().lower()
        opciones = get_opciones(row)

        # ── Contenedor oscuro para legibilidad ──
        st.markdown("""
        <div style="background:rgba(13,13,18,0.88);border:1px solid rgba(201,168,76,0.22);
        border-radius:12px;padding:1.8rem 2rem 1.2rem;margin:0.5rem 0;">
        """, unsafe_allow_html=True)

        _raiz_progreso(idx + 1, total)

        # Pregunta
        st.markdown(
            f"<div style='background:#1a1a28;border-left:3px solid #c9a84c;"
            f"padding:1.5rem;border-radius:0 4px 4px 0;margin:1rem 0 1.5rem'>"
            f"<p style=\"font-family:'Cinzel',serif;color:#e8e0d0;font-size:1rem;"
            f"margin:0;line-height:1.5\">{row['texto']}</p></div>",
            unsafe_allow_html=True
        )

        for i, op in enumerate(opciones):
            if st.button(op["texto"], key=f"m1_q{idx}_op{i}", use_container_width=True):
                dim_key = dimension.strip().lower()
                if dim_key in st.session_state.m1_respuestas:
                    st.session_state.m1_respuestas[dim_key].append(op["puntuacion"])
                st.session_state.m1_idx += 1
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # ─── RESULTADO ───
    elif fase == "resultado":
        perfil = st.session_state.get("perfil_usuario", {})
        personaje_nombre = st.session_state.get("personaje_asignado", "")
        personaje_data = st.session_state.get("personaje_data", {})

        # ── Personaje asignado ──
        st.markdown("---")
        st.markdown(
            f"<h2 style=\"font-family:'Cinzel',serif;color:#c9a84c;"
            f"font-size:1.2rem;text-align:center\">Tu personaje</h2>",
            unsafe_allow_html=True
        )

        col_img, col_desc = st.columns([1, 2])
        with col_img:
            cargar_imagen(personaje_data.get("url_imagen", ""), personaje_nombre)
            # Copyright
            universos_copyright = {
                1: "© Warner Bros. / J.K. Rowling",
                2: "© New Line Cinema / Philip Pullman",
                3: "© Nintendo / The Pokémon Company",
                4: "© Studio Ghibli",
                5: "© DreamWorks Animation",
                6: "© The Walt Disney Company / Pixar",
            }
            copyright_txt = universos_copyright.get(universo_id, "")
            if copyright_txt:
                st.markdown(
                    f"<p style='color:#555;font-size:0.7rem;text-align:center;"
                    f"margin-top:0.3rem'>{copyright_txt}. Uso educativo no comercial.</p>",
                    unsafe_allow_html=True
                )

        with col_desc:
            st.markdown(
                f"<p style=\"font-family:'Cinzel',serif;color:#c9a84c;"
                f"font-size:1.1rem;margin-bottom:0.5rem\">{personaje_nombre}</p>",
                unsafe_allow_html=True
            )
            descripcion = personaje_data.get("descripcion", "")
            if descripcion and str(descripcion) not in ("", "nan"):
                st.markdown(
                    f"<p style='color:#e8e0d0;font-size:0.9rem;line-height:1.6'>"
                    f"{descripcion}</p>",
                    unsafe_allow_html=True
                )

        # ── Perfil de 8 dimensiones ──
        st.markdown("---")
        st.markdown(
            f"<h2 style=\"font-family:'Cinzel',serif;color:#c9a84c;"
            f"font-size:1.2rem;text-align:center\">Tu perfil de dimensiones</h2>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)
        for i, dim in enumerate(DIMENSIONES):
            col = col1 if i % 2 == 0 else col2
            with col:
                valor = perfil.get(dim, 0)
                pct = int((valor / 5) * 100)
                st.markdown(
                    f"<div style='margin-bottom:1rem'>"
                    f"<p style=\"font-family:'Cinzel',serif;color:#c9a84c;"
                    f"font-size:0.85rem;margin:0 0 0.2rem\">"
                    f"{NOMBRES_DIMENSIONES[dim]}</p>"
                    f"<p style='color:#9a9080;font-size:0.75rem;margin:0 0 0.3rem'>"
                    f"{DESCRIPCIONES_DIMENSIONES[dim]}</p>"
                    f"<div style='background:#2a2a3a;border-radius:2px;height:6px'>"
                    f"<div style='background:#c9a84c;width:{pct}%;height:6px;"
                    f"border-radius:2px'></div></div>"
                    f"<p style='color:#9a9080;font-size:0.75rem;text-align:right;"
                    f"margin:0.2rem 0 0'>{valor:.1f} / 5</p>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        # ── Orientación ND ──
        st.markdown("---")
        _mostrar_orientacion_nd(perfil)

        # ── Botón continuar ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="
            background: rgba(74,127,165,0.12);
            border: 1px solid rgba(74,127,165,0.4);
            border-left: 4px solid #4a7fa5;
            border-radius: 0 8px 8px 0;
            padding: 1rem 1.5rem;
            margin: 1.5rem 0 1rem;
        ">
            <p style="color:#e8e0d0; font-size:0.9rem; margin:0; line-height:1.6;">
                ⚠️ <strong>Este perfil es orientativo y no equivale a un diagnóstico clínico.</strong>
                Solo un profesional cualificado puede realizar un diagnóstico. Seiðr es un punto de partida, no un resultado definitivo.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ── Narrador contextual ──
        try:
            from narrador import get_narrador
            universo_id = st.session_state.get("universo_elegido")
            texto_narrador = get_narrador(universo_id, "perfil_completado")
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

        col_btn = st.columns([1, 2, 1])[1]
        with col_btn:
            if st.button("ᚢ Continuar a Tu criatura →", use_container_width=True, key="btn_m1_siguiente"):
                st.session_state["_pagina_activa"] = "ᚢ  Tu criatura"
                st.rerun()


def _mostrar_orientacion_nd(perfil: dict):
    """Ejecuta el algoritmo de orientación ND y muestra el resultado."""
    try:
        try:
            from db import cargar_perfiles_nd
            df_nd = cargar_perfiles_nd()
            if df_nd.empty:
                raise Exception("BD vacía")
        except Exception:
            df_nd = pd.read_csv("universos/perfiles_nd_clinicos.csv", engine="python")
        from orientacion_nd import orientar_nd

        # El algoritmo usa nombres distintos — adaptamos el perfil
        perfil_nd = {
            "hiperfoco":      perfil.get("hiperfoco", 0),
            "reg_emocional":  perfil.get("regulacion_emocional", 0),
            "sensorialidad":  perfil.get("sensorialidad", 0),
            "comunicacion":   perfil.get("comunicacion", 0),
            "aprendizaje":    perfil.get("aprendizaje", 0),
            "sociabilidad":   perfil.get("sociabilidad", 0),
            "propiocepcion":  perfil.get("propiocepcion", 0),
            "f_ejecutiva":    perfil.get("funcion_ejecutiva", 0),
        }

        df_resultado = orientar_nd(perfil_nd, df_nd, umbral=8)

        # ── Guardar orientacion_nd en session_state para módulos 3-7 ──
        nds_encontradas = [
            str(row["nombre"])
            for _, row in df_resultado.iterrows()
            if str(row.get("nombre", "")) != "Perfil Neurotípico"
        ]
        st.session_state["orientacion_nd"] = nds_encontradas if nds_encontradas else []

        st.markdown(
            "<h2 style=\"font-family:'Cinzel',serif;color:#c9a84c;"
            "font-size:1.2rem;text-align:center\">Orientación</h2>",
            unsafe_allow_html=True
        )

        for _, row in df_resultado.iterrows():
            nombre_nd = row.get("nombre", "")
            etiqueta  = row.get("etiqueta", "")
            coincidencia = row.get("coincidencia", "")

            if nombre_nd == "Perfil Neurotípico":
                # Buscar explicación NT en el CSV si existe
                fila_nt = df_nd[df_nd["nombre"] == "Neurotípico"] if "Neurotípico" in df_nd["nombre"].values else None
                explicacion = "Tu perfil no muestra rasgos que encajen con ningún patrón de neurodivergencia de manera significativa. Eso no significa que no tengas particularidades — simplemente que están dentro del rango considerado típico en todas las dimensiones."
                st.markdown(
                    "<div style='background:#1a1a28;border-left:3px solid #4a7fa5;"
                    "padding:1.2rem;border-radius:0 4px 4px 0;margin-bottom:0.8rem'>"
                    "<p style=\"font-family:'Cinzel',serif;color:#4a7fa5;"
                    "font-size:0.95rem;margin:0 0 0.5rem\">⬜ Perfil Neurotípico</p>"
                    f"<p style='color:#9a9080;font-size:0.85rem;line-height:1.6;margin:0'>{explicacion}</p>"
                    "</div>",
                    unsafe_allow_html=True
                )
            else:
                icono = "✅" if coincidencia == "100%" else "🔶"
                # Buscar explicación en el CSV
                fila = df_nd[df_nd["nombre"] == nombre_nd]
                explicacion = ""
                if not fila.empty and "explicacion_perfil" in fila.columns:
                    explicacion = str(fila.iloc[0]["explicacion_perfil"])
                    if explicacion == "nan":
                        explicacion = ""

                st.markdown(
                    f"<div style='background:#1a1a28;border-left:3px solid #c9a84c;"
                    f"padding:1.2rem;border-radius:0 4px 4px 0;margin-bottom:0.8rem'>"
                    f"<p style=\"font-family:'Cinzel',serif;color:#c9a84c;"
                    f"font-size:0.95rem;margin:0 0 0.3rem\">"
                    f"{icono} {nombre_nd} "
                    f"<span style='color:#9a9080;font-size:0.8rem'>({etiqueta} · {coincidencia})</span></p>"
                    f"<p style='color:#9a9080;font-size:0.85rem;line-height:1.6;margin:0'>{explicacion}</p>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        

    except Exception as e:
        st.markdown(
            f"<p style='color:#555;font-size:0.8rem;text-align:center'>"
            f"Orientación ND no disponible: {e}</p>",
            unsafe_allow_html=True
        )
