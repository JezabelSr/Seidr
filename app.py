"""
SEIÐR — Cuando tu saga se convierte en brújula
App principal de Streamlit — Estructura base v1.0
"""

import streamlit as st
import base64
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA (debe ser lo primero)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Seiðr",
    page_icon="ᚱ",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# TEXTURA — cargar PNG como base64
# ─────────────────────────────────────────────
def cargar_textura(ruta: str) -> str:
    p = Path(ruta)
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return ""

_b64 = cargar_textura("iconografia/textura_piedra.png")
_textura_css = f"url('data:image/png;base64,{_b64}')" if _b64 else "none"

# ─────────────────────────────────────────────
# TEMA VISUAL — CSS personalizado
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fuentes ── */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&family=Crimson+Pro:ital,wght@0,300;0,400;1,300&display=swap');

/* ── Paleta de colores ── */
:root {
    --bg-oscuro:      #0d0d12;
    --bg-panel:       #14141e;
    --bg-card:        #1a1a28;
    --dorado:         #c9a84c;
    --dorado-claro:   #e8c97a;
    --dorado-suave:   #c9a84c22;
    --texto-principal:#e8e0d0;
    --texto-suave:    #9a9080;
    --runa-glow:      #c9a84c66;
    --acento-frio:    #4a7fa5;
}

/* ── Fondo general ── */
.stApp {
    background-color: var(--bg-oscuro);
    background-image:
        radial-gradient(ellipse at 20% 10%, #1e1a2e 0%, transparent 50%),
        radial-gradient(ellipse at 80% 90%, #1a1510 0%, transparent 50%);
    color: var(--texto-principal);
    font-family: 'Crimson Pro', Georgia, serif;
}
</style>
""", unsafe_allow_html=True)

# Inyectar textura por separado (f-string sin mezclar con el CSS de arriba)
st.markdown(f"""
<style>
.stApp {{
    background-image:
        radial-gradient(ellipse at 20% 10%, #1e1a2e 0%, transparent 50%),
        radial-gradient(ellipse at 80% 90%, #1a1510 0%, transparent 50%),
        {_textura_css};
    background-size: auto, auto, 512px 512px;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--bg-panel);
    border-right: 1px solid #2a2a3a;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Cinzel', serif;
    color: var(--dorado);
    letter-spacing: 0.05em;
}

/* ── Radio buttons de navegación ── */
[data-testid="stSidebar"] .stRadio label {
    color: var(--texto-principal) !important;
    font-family: 'Crimson Pro', serif;
    font-size: 1rem;
    padding: 0.3rem 0;
    cursor: pointer;
    transition: color 0.2s;
}

[data-testid="stSidebar"] .stRadio label:hover {
    color: var(--dorado-claro) !important;
}

/* ── Títulos principales ── */
h1, h2, h3 {
    font-family: 'Cinzel', serif !important;
    color: var(--dorado) !important;
    letter-spacing: 0.04em;
}

/* ── Separador dorado ── */
hr {
    border: none;
    border-top: 1px solid #2a2a3a;
    margin: 1.5rem 0;
}

/* ── Tarjetas de módulo ── */
.seidr-card {
    background: var(--bg-card);
    border: 1px solid #2a2a3a;
    border-left: 3px solid var(--dorado);
    border-radius: 4px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s, background 0.2s;
}

.seidr-card:hover {
    border-left-color: var(--dorado-claro);
    background: #1e1e2e;
}

.seidr-card h4 {
    font-family: 'Cinzel', serif !important;
    color: var(--dorado) !important;
    font-size: 0.95rem;
    margin: 0 0 0.4rem 0;
    letter-spacing: 0.06em;
}

.seidr-card p {
    color: var(--texto-suave);
    font-size: 0.9rem;
    margin: 0;
    line-height: 1.5;
}

/* ── Banner de bienvenida ── */
.seidr-banner {
    text-align: center;
    padding: 3rem 2rem 2rem;
}

.seidr-titulo {
    font-family: 'Cinzel', serif;
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 900;
    color: var(--dorado);
    letter-spacing: 0.15em;
    text-shadow: 0 0 40px var(--runa-glow);
    margin: 0;
    line-height: 1;
}

.seidr-subtitulo {
    font-family: 'Crimson Pro', serif;
    font-style: italic;
    font-size: 1.3rem;
    color: var(--texto-suave);
    margin-top: 0.8rem;
    letter-spacing: 0.05em;
}

.seidr-runa {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: block;
    filter: drop-shadow(0 0 12px var(--runa-glow));
}

/* ── Botón principal ── */
.stButton > button {
    background: transparent;
    border: 1px solid var(--dorado);
    color: var(--dorado);
    font-family: 'Cinzel', serif;
    letter-spacing: 0.1em;
    font-size: 0.9rem;
    padding: 0.6rem 2rem;
    border-radius: 2px;
    transition: all 0.2s;
}

.stButton > button:hover {
    background: var(--dorado-suave);
    border-color: var(--dorado-claro);
    color: var(--dorado-claro);
}

/* ── Aviso en construcción ── */
.en-construccion {
    background: #1a1a10;
    border: 1px dashed #3a3a20;
    border-radius: 4px;
    padding: 2rem;
    text-align: center;
    color: var(--texto-suave);
    font-style: italic;
}

/* ── Info box personalizado ── */
.seidr-info {
    background: #141e28;
    border-left: 3px solid var(--acento-frio);
    padding: 1rem 1.5rem;
    border-radius: 0 4px 4px 0;
    margin: 1rem 0;
    font-size: 0.9rem;
    color: var(--texto-suave);
    line-height: 1.6;
}

/* ── Ocultar elementos de Streamlit ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ESTADO DE SESIÓN
# ─────────────────────────────────────────────
def init_session():
    defaults = {
        "universo_elegido":   None,
        "perfil_usuario":     None,
        "personaje_asignado": None,
        "criatura_asignada":  None,
        "orientacion_nd":     None,
        "test_universo_done": False,
        "test_dim_done":      False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()


# ─────────────────────────────────────────────
# SIDEBAR — Navegación
# ─────────────────────────────────────────────
MODULOS = {
    "ᚱ  Inicio":                 "inicio",
    "ᚦ  Test de universo":       "test_universo",
    "ᚨ  Módulo 1 · Tu perfil":   "modulo_1",
    "ᚢ  Módulo 2 · Tu criatura": "modulo_2",
    "ᚲ  Módulo 3 · Comunicación":"modulo_3",
    "ᚷ  Módulo 4 · Aprendizaje": "modulo_4",
    "ᛉ  Módulo 5 · Sociabilidad":"modulo_5",
    "ᛊ  Módulo 6 · Cuerpo":      "modulo_6",
    "ᛏ  Módulo 7 · Clínico":     "modulo_7",
}

with st.sidebar:
    st.markdown("### ᚱ Seiðr")
    st.markdown("---")

    pagina_actual = st.radio(
        label="Navegación",
        options=list(MODULOS.keys()),
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("---")

    if st.session_state.universo_elegido:
        st.markdown(f"**Universo:** {st.session_state.universo_elegido}")
    if st.session_state.test_dim_done:
        st.markdown("**Perfil:** ᚱ completado")
    if st.session_state.personaje_asignado:
        st.markdown(f"**Personaje:** {st.session_state.personaje_asignado}")

    st.markdown("---")
    st.markdown(
        "<small style='color:#555'>Seiðr v1.0 · AGPL v3<br>"
        "Datos: CC BY-NC-ND 4.0<br>"
        "No es herramienta de diagnóstico</small>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# PÁGINAS
# ─────────────────────────────────────────────

def pagina_inicio():
    st.markdown("""
    <div class="seidr-banner">
        <span class="seidr-runa">ᚱ</span>
        <h1 class="seidr-titulo">SEIÐR</h1>
        <p class="seidr-subtitulo">Cuando tu saga se convierte en brújula</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="seidr-info">
        Seiðr no es una herramienta de diagnóstico. Es un punto de partida:
        usa universos de ficción como puerta de entrada a información clínica
        rigurosa sobre neurodivergencia. La ficción es el vehículo, nunca el contenido.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ¿Cómo funciona?")

    modulos_info = [
        ("ᚦ", "Test de universo", "Elige tu universo de ficción favorito. Será el lenguaje de todo lo que viene."),
        ("ᚨ", "Módulo 1 · Tu perfil", "Responde 24 preguntas en el lenguaje de tu universo. Obtendrás tu perfil de 8 dimensiones y el personaje que más se parece a ti."),
        ("ᚢ", "Módulo 2 · Tu criatura", "Se te asigna una criatura de asistencia basada en tu perfil. Cada criatura tiene un equivalente en razas reales de perros."),
        ("ᚲ", "Módulos 3-7", "Recursos reales organizados por dimensión: comunicación, aprendizaje, sociabilidad, cuerpo y orientación clínica."),
    ]

    col1, col2 = st.columns(2)
    for i, (icono, titulo, desc) in enumerate(modulos_info):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div class="seidr-card">
                <h4>{icono} {titulo}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("ᚦ Comenzar", use_container_width=True):
            st.info("← Selecciona 'Test de universo' en el menú lateral para empezar.")


def pagina_en_construccion(nombre: str, descripcion: str = ""):
    st.title(nombre)
    if descripcion:
        st.markdown(f"*{descripcion}*")
    st.markdown("---")
    st.markdown("""
    <div class="en-construccion">
        <p>ᚲ Este módulo está en construcción.</p>
        <p style="font-size:0.85rem">Vuelve pronto — se está tejiendo.</p>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ENRUTADOR PRINCIPAL
# ─────────────────────────────────────────────
pagina_id = MODULOS[pagina_actual]

if pagina_id == "inicio":
    pagina_inicio()
elif pagina_id == "test_universo":
    pagina_en_construccion("ᚦ Test de universo", "Elige tu universo de ficción. Será el lenguaje de tu viaje.")
elif pagina_id == "modulo_1":
    pagina_en_construccion("ᚨ Módulo 1 · Tu perfil", "24 preguntas → perfil de 8 dimensiones + personaje.")
elif pagina_id == "modulo_2":
    pagina_en_construccion("ᚢ Módulo 2 · Tu criatura de asistencia", "La criatura que mejor encaja con tu perfil y su equivalente en razas reales.")
elif pagina_id == "modulo_3":
    pagina_en_construccion("ᚲ Módulo 3 · Tu forma de comunicarte", "Recursos de logopedia, CAA y comunicación aumentativa.")
elif pagina_id == "modulo_4":
    pagina_en_construccion("ᚷ Módulo 4 · Tu forma de aprender", "Técnicas, adaptaciones y recursos de función ejecutiva.")
elif pagina_id == "modulo_5":
    pagina_en_construccion("ᛉ Módulo 5 · Tu forma de socializar", "Hobbies, comunidades y recursos de sociabilidad.")
elif pagina_id == "modulo_6":
    pagina_en_construccion("ᛊ Módulo 6 · Tu cuerpo", "Autorregulación sensorial, propiocepción y terapia ocupacional.")
elif pagina_id == "modulo_7":
    pagina_en_construccion("ᛏ Módulo 7 · Orientación clínica", "Tests gratuitos, profesionales y recursos clínicos verificados.")
