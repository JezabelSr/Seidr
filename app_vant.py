"""
SEIÐR — Cuando tu saga se convierte en brújula
App principal de Streamlit — Estructura base v1.0
"""

import streamlit as st
import base64
from pathlib import Path
import sys
import pandas as pd

# ─────────────────────────────────────────────
# IMPORTACIONES DE MÓDULOS
# ─────────────────────────────────────────────
sys.path.insert(0, "hechizos")
from test_universo import pagina_test_universo
from modulo_1 import pagina_modulo_1
from modulo_2 import pagina_modulo_2

try:
    from runas.procesamiento_datos import mapear_akc_a_dimensiones_nd
except ImportError:
    def mapear_akc_a_dimensiones_nd(df): return df

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Seiðr",
    page_icon="ᚱ",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CARGA DE RECURSOS (BASE64)
# ─────────────────────────────────────────────
def get_b64(path):
    p = Path(path)
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else None

img_b64 = get_b64("iconografia/portada_seidr.png") or get_b64("iconografia/portada_seidr.jpg")
textura_b64 = get_b64("iconografia/textura_piedra.png")

# ─────────────────────────────────────────────
# CSS FINAL: BANNER INTEGRADO Y DIFUMINADO
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
/* Sidebar visible siempre */
[data-testid="collapsedControl"] {{ display: flex !important; visibility: visible !important; }}
section[data-testid="stSidebar"][aria-expanded="false"] {{ margin-left: 0 !important; min-width: 250px !important; width: 250px !important; }}

/* Fondo global con textura */
.stApp {{ 
    background-color: #0d0d12; 
    background-image: url('data:image/png;base64,{textura_b64}');
    background-repeat: repeat;
    color: #e8e0d0; 
    font-family: 'Crimson Pro', serif; 
}}

/* PORTADA: Altura fija + Degradado suave hacia abajo */
.portada-container {{
    width: 100%;
    height: 280px;
    overflow: hidden;
    border-radius: 8px;
    margin-bottom: 2rem;
    
    /* Degradado suave que funde la imagen con el fondo */
    -webkit-mask-image: linear-gradient(to bottom, black 75%, transparent 100%);
    mask-image: linear-gradient(to bottom, black 75%, transparent 100%);
}}

.portada-img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: 50% 10%; /* Ajuste para que se vea el título */
    display: block;
}}

/* Tarjetas */
.seidr-card {{ background: #1a1a28; border: 1px solid #2a2a3a; border-left: 3px solid #c9a84c; padding: 1.2rem; margin-bottom: 1rem; }}
.seidr-card h4 {{ font-family: 'Cinzel', serif; color: #c9a84c; margin: 0 0 0.4rem 0; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
MODULOS = {
    "ᚱ  Inicio": "inicio",
    "ᚦ  Test de universo": "test_universo",
    "ᚨ  Módulo 1 · Tu perfil": "modulo_1",
    "ᚢ  Módulo 2 · Tu criatura": "modulo_2",
    "ᚲ  Módulo 3 · Comunicación": "modulo_3",
    "ᚷ  Módulo 4 · Aprendizaje": "modulo_4",
    "ᛉ  Módulo 5 · Sociabilidad": "modulo_5",
    "ᛊ  Módulo 6 · Cuerpo": "modulo_6",
    "ᛏ  Módulo 7 · Clínico": "modulo_7",
}

with st.sidebar:
    st.markdown("### ᚱ Seiðr")
    pagina_actual = st.radio("Navegación", list(MODULOS.keys()), label_visibility="collapsed")

# ─────────────────────────────────────────────
# PÁGINA INICIO
# ─────────────────────────────────────────────
def pagina_inicio():
    if img_b64:
        st.markdown(f'''
            <div class="portada-container">
                <img src="data:image/png;base64,{img_b64}" class="portada-img">
            </div>
        ''', unsafe_allow_html=True)

    st.write("### ¿Cómo funciona?")
    
    col1, col2 = st.columns(2)
    modulos_info = [
        ("ᚦ", "Test de universo", "Elige tu universo de ficción favorito."),
        ("ᚨ", "Módulo 1 · Tu perfil", "Responde 24 preguntas y obtén tu perfil."),
        ("ᚢ", "Módulo 2 · Tu criatura", "Tu criatura de asistencia personalizada."),
        ("ᚲ", "Módulos 3-7", "Recursos organizados por dimensiones.")
    ]
    
    for i, (icono, titulo, desc) in enumerate(modulos_info):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f'<div class="seidr-card"><h4>{icono} {titulo}</h4><p>{desc}</p></div>', unsafe_allow_html=True)

    if st.button("ᚦ Comenzar"):
        st.session_state.pagina_actual = "test_universo"
        st.rerun()

# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
pagina_id = MODULOS[pagina_actual]

if pagina_id == "inicio":
    pagina_inicio()
elif pagina_id == "test_universo":
    pagina_test_universo()
elif pagina_id == "modulo_1":
    pagina_modulo_1()
elif pagina_id == "modulo_2":
    pagina_modulo_2()
else:
    st.title(pagina_actual)
    st.info("Este módulo está en desarrollo.")