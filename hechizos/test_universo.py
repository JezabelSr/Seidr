"""
SEIÐR — Test de universo
Flujo: elección directa O test (3 preguntas generales → grupo → 4 preguntas finas → universo)
"""

import streamlit as st
import pandas as pd
from collections import Counter

UNIVERSOS_POR_GRUPO = {
    "A": [
        {"id": 1, "nombre": "Harry Potter",              "desc": "El mundo mágico de Hogwarts"},
        {"id": 2, "nombre": "La Brújula Dorada",         "desc": "Mundos paralelos y daimonions"},
    ],
    "B": [
        {"id": 3, "nombre": "Pokémon",                   "desc": "Entrenadores y criaturas"},
        {"id": 5, "nombre": "Cómo entrenar a tu dragón", "desc": "Vikingos y dragones"},
    ],
    "C": [
        {"id": 4, "nombre": "Studio Ghibli",             "desc": "Mundos animados y espíritus"},
        {"id": 6, "nombre": "Disney/Pixar",              "desc": "Magia y emociones"},
    ],
    "D": [],
    "E": [],
}

TODOS_UNIVERSOS = [u for g in UNIVERSOS_POR_GRUPO.values() for u in g]

PREGUNTAS_POR_GRUPO = {
    "A": [4, 5, 6, 7],
    "B": [8, 9, 10, 11],
    "C": [12, 13, 14],
    "D": [15, 16, 17, 18],
    "E": [19, 20, 21, 22],
}

NOMBRES_UNIVERSOS = {
    1: "Harry Potter",
    2: "La Brújula Dorada",
    3: "Pokémon",
    4: "Studio Ghibli",
    5: "Cómo entrenar a tu dragón",
    6: "Disney/Pixar",
}


@st.cache_data
def cargar_preguntas():
    try:
        df = pd.read_csv("universos/preguntas.csv", engine="python")
        return df[df["universo_id"] == 0].reset_index(drop=True)
    except Exception:
        return pd.DataFrame()


def get_opciones(row):
    opciones = []
    for letra in ["a", "b", "c", "d", "e"]:
        txt = row.get(f"opcion_{letra}", "")
        pun = row.get(f"puntuacion_{letra}", "")
        if pd.notna(txt) and str(txt).strip() and pd.notna(pun) and str(pun).strip():
            opciones.append({"texto": str(txt).strip(), "puntuacion": str(pun).strip()})
    return opciones


def init_test():
    defaults = {
        "test_fase":        "inicio",
        "test_idx":         0,
        "test_resp_b1":     [],
        "test_grupo":       None,
        "test_resp_b2":     [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def calcular_grupo(respuestas):
    if not respuestas:
        return "A"
    return Counter(respuestas).most_common(1)[0][0]


def calcular_universo(grupo, respuestas_b2):
    universos = UNIVERSOS_POR_GRUPO.get(grupo, [])
    if not universos:
        return None
    if len(universos) == 1:
        return universos[0]["id"]
    conteo = Counter(respuestas_b2)
    if conteo.get("1", 0) >= conteo.get("2", 0):
        return universos[0]["id"]
    return universos[1]["id"]


def _card_universo(u, key):
    st.markdown(f"""
    <div style="background:#1a1a28;border:1px solid #2a2a3a;
                border-left:3px solid #c9a84c;padding:1rem 1.2rem;
                border-radius:4px;margin-bottom:0.4rem;text-align:center">
        <p style="font-family:'Cinzel',serif;color:#c9a84c;
                   font-size:0.9rem;margin:0 0 0.3rem">{u['nombre']}</p>
        <p style="color:#9a9080;font-size:0.8rem;margin:0">{u['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    return st.button("Elegir", key=key, use_container_width=True)


def _mostrar_pregunta(numero, total, texto, opciones):
    st.progress(numero / total)
    st.markdown(
        f"<p style='color:#9a9080;font-size:0.8rem;text-align:right;margin-top:-0.5rem'>"
        f"{numero} / {total}</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='background:#1a1a28;border-left:3px solid #c9a84c;"
        f"padding:1.5rem;border-radius:0 4px 4px 0;margin:1rem 0 1.5rem'>"
        f"<p style=\"font-family:'Cinzel',serif;color:#e8e0d0;font-size:1rem;"
        f"margin:0;line-height:1.5\">{texto}</p></div>",
        unsafe_allow_html=True
    )
    for i, op in enumerate(opciones):
        if st.button(op["texto"], key=f"q{numero}_op{i}", use_container_width=True):
            return op["puntuacion"]
    return None


def _finalizar(universo_id):
    st.session_state.universo_elegido = universo_id
    st.session_state.universo_nombre = NOMBRES_UNIVERSOS.get(universo_id, "")
    st.session_state.test_universo_done = True
    st.session_state.test_fase = "completado"
    st.rerun()


def pagina_test_universo():
    init_test()

    preguntas = cargar_preguntas()

    # Cabecera
    st.markdown(
        "<div style='text-align:center;padding:2rem 0 1rem'>"
        "<h1 style=\"font-family:'Cinzel',serif;color:#c9a84c;"
        "letter-spacing:0.1em;font-size:1.8rem\">ᚦ Test de universo</h1>"
        "<p style='color:#9a9080;font-style:italic'>"
        "El universo que elijas será el lenguaje de todo lo que viene.</p></div>",
        unsafe_allow_html=True
    )

    fase = st.session_state.test_fase

    # ─── INICIO — elegir entre test o elección directa ───
    if fase == "inicio":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background:#1a1a28;border:1px solid #2a2a3a;
                        border-left:3px solid #c9a84c;padding:1.5rem;
                        border-radius:4px;text-align:center">
                <p style="font-family:'Cinzel',serif;color:#c9a84c;font-size:0.95rem;margin:0 0 0.5rem">
                    ᚦ Hacer el test
                </p>
                <p style="color:#9a9080;font-size:0.85rem;margin:0">
                    Responde 7 preguntas y descubre qué universo encaja con tu forma de ser
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Empezar el test", use_container_width=True):
                st.session_state.test_fase = "bloque1"
                st.rerun()

        with col2:
            st.markdown("""
            <div style="background:#1a1a28;border:1px solid #2a2a3a;
                        border-left:3px solid #c9a84c;padding:1.5rem;
                        border-radius:4px;text-align:center">
                <p style="font-family:'Cinzel',serif;color:#c9a84c;font-size:0.95rem;margin:0 0 0.5rem">
                    ᚱ Elegir directamente
                </p>
                <p style="color:#9a9080;font-size:0.85rem;margin:0">
                    Ya sé qué universo quiero
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Ver universos", use_container_width=True):
                st.session_state.test_fase = "eleccion_directa"
                st.rerun()

    # ─── ELECCIÓN DIRECTA ───
    elif fase == "eleccion_directa":
        st.markdown(
            "<p style='color:#9a9080;text-align:center;margin-bottom:1.5rem'>"
            "¿Cuál es tu universo?</p>",
            unsafe_allow_html=True
        )
        cols = st.columns(3)
        for i, u in enumerate(TODOS_UNIVERSOS):
            with cols[i % 3]:
                if _card_universo(u, key=f"dir_{u['id']}"):
                    _finalizar(u["id"])

    # ─── BLOQUE 1 ───
    elif fase == "bloque1":
        bloque1 = preguntas[preguntas["pregunta_id"].isin([1, 2, 3])].reset_index(drop=True)
        idx = st.session_state.test_idx

        if idx >= len(bloque1):
            grupo = calcular_grupo(st.session_state.test_resp_b1)
            st.session_state.test_grupo = grupo
            st.session_state.test_idx = 0
            if not UNIVERSOS_POR_GRUPO.get(grupo):
                st.session_state.test_fase = "no_disponible"
            else:
                st.session_state.test_fase = "bloque2"
            st.rerun()
            return

        row = bloque1.iloc[idx]
        respuesta = _mostrar_pregunta(idx + 1, 7, str(row["texto"]), get_opciones(row))
        if respuesta is not None:
            st.session_state.test_resp_b1.append(respuesta)
            st.session_state.test_idx += 1
            st.rerun()

    # ─── BLOQUE 2 ───
    elif fase == "bloque2":
        grupo = st.session_state.test_grupo
        ids_grupo = PREGUNTAS_POR_GRUPO.get(grupo, [])
        preguntas_b2 = preguntas[preguntas["pregunta_id"].isin(ids_grupo)].reset_index(drop=True)
        total_b2 = len(preguntas_b2)
        idx = st.session_state.test_idx

        if idx >= total_b2:
            universo_id = calcular_universo(grupo, st.session_state.test_resp_b2)
            _finalizar(universo_id)
            return

        row = preguntas_b2.iloc[idx]
        respuesta = _mostrar_pregunta(3 + idx + 1, 3 + total_b2, str(row["texto"]), get_opciones(row))
        if respuesta is not None:
            st.session_state.test_resp_b2.append(respuesta)
            st.session_state.test_idx += 1
            st.rerun()

    # ─── GRUPO NO DISPONIBLE ───
    elif fase == "no_disponible":
        st.markdown(
            "<div style='background:#14141e;border:1px dashed #3a3a20;"
            "border-radius:4px;padding:2rem;text-align:center;margin:2rem auto;max-width:600px'>"
            "<p style=\"color:#c9a84c;font-family:'Cinzel',serif;font-size:1rem\">"
            "Tu universo llega en la siguiente fase</p>"
            "<p style='color:#9a9080;font-size:0.9rem;margin-top:0.5rem'>"
            "Los universos que encajan con tu perfil aún no están disponibles. "
            "Elige uno de los actuales para continuar.</p></div>",
            unsafe_allow_html=True
        )
        cols = st.columns(3)
        for i, u in enumerate(TODOS_UNIVERSOS):
            with cols[i % 3]:
                if _card_universo(u, key=f"nd_{u['id']}"):
                    _finalizar(u["id"])

    # ─── COMPLETADO ───
    elif fase == "completado":
        nombre = st.session_state.get("universo_nombre", "tu universo")
        st.markdown(
            f"<div style='text-align:center;padding:2rem'>"
            f"<p style=\"font-family:'Cinzel',serif;color:#c9a84c;font-size:1.4rem\">"
            f"Tu universo es {nombre}</p>"
            f"<p style='color:#9a9080;font-style:italic'>"
            f"Ahora descubriremos qué personaje se parece más a ti.</p></div>",
            unsafe_allow_html=True
        )
        try:
            from narrador import get_narrador
            universo_id = st.session_state.get("universo_elegido")
            texto_narrador = get_narrador(universo_id, "universo_elegido")
            if texto_narrador:
                st.markdown(
                    f"<div style='background:rgba(201,168,76,0.06);border-left:3px solid #c9a84c;"
                    f"border-radius:0 8px 8px 0;padding:1rem 1.5rem;margin:1rem 0 1.5rem;text-align:center;'>"
                    f"<p style='color:#c9a84c;font-size:0.9rem;font-style:italic;margin:0;line-height:1.7;'>{texto_narrador}</p></div>",
                    unsafe_allow_html=True
                )
        except Exception:
            pass

        col_btn = st.columns([1, 2, 1])[1]
        with col_btn:
            if st.button("ᚨ Continuar a Tu perfil →", use_container_width=True, key="btn_tu_completado"):
                st.session_state["_pagina_activa"] = "ᚨ  Tu perfil"
                st.rerun()
