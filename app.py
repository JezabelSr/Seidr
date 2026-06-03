import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path
import sys

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
sys.path.insert(0, "hechizos")

# ── Crear BD SQLite desde CSVs si no existe ──
try:
    from crear_bd import crear_bd
    crear_bd(forzar=False)
except Exception as e:
    pass  # Si falla, los módulos usarán CSVs como fallback

try:
    from test_universo import pagina_test_universo
except ImportError:
    def pagina_test_universo(): st.warning("Módulo test_universo no encontrado en hechizos/")

try:
    from modulo_1 import pagina_modulo_1
except ImportError:
    def pagina_modulo_1(): st.warning("Módulo modulo_1 no encontrado en hechizos/")

try:
    from modulo_2 import pagina_modulo_2
except ImportError:
    def pagina_modulo_2(): st.warning("Módulo modulo_2 no encontrado en hechizos/")

try:
    from modulo_3 import mostrar_modulo_3
except ImportError:
    def mostrar_modulo_3(orientacion_nd=None): st.warning("Módulo modulo_3 no encontrado en hechizos/")

try:
    from modulo_4 import mostrar_modulo_4
except ImportError:
    def mostrar_modulo_4(orientacion_nd=None): st.warning("Módulo modulo_4 no encontrado en hechizos/")

try:
    from modulo_5 import mostrar_modulo_5
except ImportError:
    def mostrar_modulo_5(orientacion_nd=None): st.warning("Módulo modulo_5 no encontrado en hechizos/")

try:
    from modulo_6 import mostrar_modulo_6
except ImportError:
    def mostrar_modulo_6(orientacion_nd=None): st.warning("Módulo modulo_6 no encontrado en hechizos/")

try:
    from modulo_7 import mostrar_modulo_7
except ImportError:
    def mostrar_modulo_7(orientacion_nd=None): st.warning("Módulo modulo_7 no encontrado en hechizos/")

st.set_page_config(
    page_title="Seiðr",
    page_icon="iconografia/favicon_seidr.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CARGA DE IMÁGENES
# ─────────────────────────────────────────────
def get_b64(path: str) -> str | None:
    p = Path(path)
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else None

img_portada  = get_b64("iconografia/portada_seidr.png") or get_b64("iconografia/portada_seidr.jpg")
textura_b64  = get_b64("iconografia/textura_piedra.png")
textura_css  = f"url('data:image/png;base64,{textura_b64}')" if textura_b64 else "none"

# Música por universo
MUSICA_UNIVERSO = {
    1: "iconografia/musica/harry_potter.mp3",
    2: "iconografia/musica/la_brujula_dorada.mp3",
    3: "iconografia/musica/pokemon.mp3",
    4: "iconografia/musica/ghibli.mp3",
    5: "iconografia/musica/como_entrenar_a_tu_dragon.mp3",
    6: "iconografia/musica/disney.mp3",
}

# Fondos por universo
FONDOS_UNIVERSO = {
    1: "iconografia/fondos/fondo_harrypotter.webp",
    2: "iconografia/fondos/fondo_labrujuladorada.webp",
    3: "iconografia/fondos/fondo_pokemon.webp",
    4: "iconografia/fondos/fondo_ghibli.webp",
    5: "iconografia/fondos/fondo_comoentrenaratudragon.webp",
    6: "iconografia/fondos/fondo_disney.webp",
}

def get_fondo_universo() -> str:
    """Devuelve el CSS de fondo según el universo elegido en session_state."""
    universo_id = st.session_state.get("universo_elegido")
    if universo_id and universo_id in FONDOS_UNIVERSO:
        b64 = get_b64(FONDOS_UNIVERSO[universo_id])
        if b64:
            return f"url('data:image/webp;base64,{b64}')"
    return textura_css  # fallback a la textura de piedra

# ─────────────────────────────────────────────
# CSS COMPLETO
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;900&family=Crimson+Pro:ital,wght@0,300;0,400;1,300&display=swap');

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

.stApp {
    background-color: var(--bg-oscuro);
    color: var(--texto-principal);
    font-family: 'Crimson Pro', Georgia, serif;
}

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

[data-testid="stSidebar"] .stRadio label {
    color: var(--texto-principal) !important;
    font-family: 'Crimson Pro', serif;
    font-size: 1rem;
    padding: 0.3rem 0;
}

[data-testid="stSidebar"] .stRadio label:hover {
    color: var(--dorado-claro) !important;
}

h1, h2, h3 {
    font-family: 'Cinzel', serif !important;
    color: var(--dorado) !important;
    letter-spacing: 0.04em;
}

hr {
    border: none;
    border-top: 1px solid #2a2a3a;
    margin: 1.5rem 0;
}

.seidr-card {
    background: var(--bg-card);
    border: 1px solid #2a2a3a;
    border-left: 3px solid var(--dorado);
    border-radius: 4px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}

.seidr-card:hover { border-left-color: var(--dorado-claro); background: #1e1e2e; }

.seidr-card h4 {
    font-family: 'Cinzel', serif !important;
    color: var(--dorado) !important;
    font-size: 0.95rem;
    margin: 0 0 0.4rem 0;
    letter-spacing: 0.06em;
}

.seidr-card p { color: var(--texto-suave); font-size: 0.9rem; margin: 0; line-height: 1.5; }

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

.en-construccion {
    background: #1a1a10;
    border: 1px dashed #3a3a20;
    border-radius: 4px;
    padding: 2rem;
    text-align: center;
    color: var(--texto-suave);
    font-style: italic;
}

.stButton > button {
    background: rgba(20, 20, 30, 0.95) !important;
    border: 1px solid var(--dorado);
    color: var(--dorado);
    font-family: 'Cinzel', serif;
    letter-spacing: 0.1em;
    font-size: 0.9rem;
    padding: 0.6rem 2rem;
    border-radius: 2px;
    transition: all 0.2s;
    backdrop-filter: blur(4px);
}

.stButton > button:hover {
    background: rgba(201, 168, 76, 0.15) !important;
    border-color: var(--dorado-claro);
    color: var(--dorado-claro);
}

/* Barra de progreso también legible */
[data-testid="stProgressBar"] > div {
    background: rgba(20, 20, 30, 0.7) !important;
    border-radius: 4px;
}

/* Contenedor principal — overlay más oscuro sobre fondos de universo */
section[data-testid="stMain"] .stMainBlockContainer {
    background: rgba(10, 10, 15, 0.82);
    backdrop-filter: blur(3px);
}

.portada-box {
    width: 100%;
    max-height: 220px;
    overflow: hidden;
    border-radius: 6px;
    margin-bottom: 1.5rem;
}

.portada-img {
    width: 100%;
    height: 220px;
    object-fit: cover;
    object-position: 50% 20%;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* Reducir padding superior del contenido principal */
.stMainBlockContainer {
    padding-top: 1rem !important;
}
[data-testid="stMain"] > div {
    padding-top: 0.5rem !important;
}
</style>
""", unsafe_allow_html=True)

# Fondo dinámico según universo elegido (o textura por defecto)
fondo_actual = get_fondo_universo()
# Si hay fondo de universo, añadir overlay oscuro encima para reducir saturación
tiene_fondo_universo = st.session_state.get("universo_elegido") is not None
overlay_css = "rgba(8,8,14,0.55)" if tiene_fondo_universo else "rgba(0,0,0,0)"

st.markdown(f"""
<style>
.stApp {{
    background-image: linear-gradient({overlay_css}, {overlay_css}), {fondo_actual};
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ESTADO DE SESIÓN
# ─────────────────────────────────────────────
def init_session():
    defaults = {
        "universo_elegido":    None,
        "universo_nombre":     None,
        "perfil_usuario":      None,
        "personaje_asignado":  None,
        "personaje_data":      None,
        "criatura_asignada":   None,
        "orientacion_nd":      None,
        "test_universo_done":  False,
        "test_dim_done":       False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
MODULOS = {
    "ᚱ  Inicio":                  "inicio",
    "ᚦ  Test de universo":        "test_universo",
    "ᚨ  Tu perfil":               "modulo_1",
    "ᚢ  Tu criatura":             "modulo_2",
    "ᚲ  Comunicación":            "modulo_3",
    "ᚷ  Aprendizaje":             "modulo_4",
    "ᛉ  Sociabilidad":            "modulo_5",
    "ᛊ  Tu cuerpo":               "modulo_6",
    "ᛏ  Orientación clínica":     "modulo_7",
    "⚕  Modo profesional":        "profesional",
}

with st.sidebar:
    st.markdown("### ᚱ Seiðr")
    st.markdown("---")

    # Índice activo: viene de _pagina_activa si se navegó desde una tarjeta
    opciones = list(MODULOS.keys())
    idx_defecto = 0
    if "_pagina_activa" in st.session_state:
        try:
            idx_defecto = opciones.index(st.session_state["_pagina_activa"])
        except ValueError:
            idx_defecto = 0

    # El radio usa su propio valor en session_state como índice
    # Así sobrevive a los reruns internos de cada módulo
    if "_pagina_activa" not in st.session_state:
        st.session_state["_pagina_activa"] = opciones[0]

    pagina_actual = st.radio(
        label="Navegación",
        options=opciones,
        index=opciones.index(st.session_state.get("_pagina_activa", opciones[0])),
        label_visibility="collapsed",
    )
    st.session_state["_pagina_activa"] = pagina_actual

    st.markdown("---")

    if st.session_state.universo_nombre:
        st.markdown(f"**Universo:** {st.session_state.universo_nombre}")
    if st.session_state.test_dim_done:
        st.markdown("**Perfil:** ᚱ completado")
    if st.session_state.personaje_asignado:
        st.markdown(f"**Personaje:** {st.session_state.personaje_asignado}")
    if st.session_state.criatura_asignada:
        st.markdown(f"**Criatura:** {st.session_state.criatura_asignada}")

    st.markdown("---")

    # ── Botón RESET ──
    if st.button("↺  Reiniciar todo", use_container_width=True, key="btn_reset"):
        claves_a_limpiar = [
            "universo_elegido", "universo_nombre", "perfil_usuario",
            "personaje_asignado", "personaje_data", "criatura_asignada",
            "orientacion_nd", "test_universo_done", "test_dim_done",
            "test_fase", "test_idx", "test_resp_b1", "test_grupo", "test_resp_b2",
            "m1_fase", "m1_idx", "m1_respuestas",
            "m2_fase",
        ]
        for k in claves_a_limpiar:
            st.session_state.pop(k, None)
        st.rerun()

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
def _navegar_a(pagina_key: str):
    """Cambia la página activa actualizando session_state y haciendo rerun."""
    for etiqueta, key in MODULOS.items():
        if key == pagina_key:
            st.session_state["_pagina_activa"] = etiqueta
            st.session_state["_navegar_desde_boton"] = True
            st.rerun()


def pagina_inicio():
    # ── Banner ──
    if img_portada:
        st.markdown(
            f'<div class="portada-box">'
            f'<img src="data:image/png;base64,{img_portada}" class="portada-img">'
            f'</div>',
            unsafe_allow_html=True
        )

    # ── Texto Seiðr ──
    _html_texto = (
        "<div style='max-width:720px;margin:0.5rem auto 0.8rem;text-align:center;padding:0 1rem;'>"
        "<p style='font-family:Cinzel,serif;color:#c9a84c;font-size:0.85rem;"
        "letter-spacing:0.2em;margin-bottom:1rem;'>"
        "ᚱ SEIÐR &nbsp;·&nbsp; <em style='font-family:Crimson Pro,serif;font-style:italic;'>"
        "pronunciado &#34;say-thr&#34;</em></p>"
        "<p style='color:#e8e0d0;font-size:1.05rem;line-height:1.85;margin-bottom:1.2rem;'>"
        "En la tradición nórdica, el <strong style='color:#c9a84c;'>seiðr</strong> "
        "era la magia de los videntes: el arte de leer los hilos invisibles del destino "
        "y encontrar el camino propio.</p>"
        "<p style='color:#9a9080;font-size:0.95rem;line-height:1.8;margin-bottom:1.2rem;'>"
        "Esta app usa universos de ficción como puerta de entrada a información clínica "
        "rigurosa sobre neurodivergencia. Elige tu saga favorita, descubre qué personaje "
        "se parece a ti, y encuentra recursos reales adaptados a cómo funciona tu mente.</p>"
        "<p style='font-family:Crimson Pro,serif;color:#c9a84c;font-size:1rem;"
        "font-style:italic;letter-spacing:0.05em;'>"
        "La ficción es el vehículo. El conocimiento, el destino.</p>"
        "</div>"
    )
    st.markdown(_html_texto, unsafe_allow_html=True)

    # ── Botón único ──
    col = st.columns([1, 3, 1])[1]
    with col:
        if st.button("ᚦ  Comienza tu aventura", use_container_width=True, key="btn_inicio_aventura"):
            _navegar_a("test_universo")


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
# SCROLL AL TOP AL CAMBIAR DE PÁGINA
# ─────────────────────────────────────────────
if "pagina_anterior" not in st.session_state:
    st.session_state["pagina_anterior"] = pagina_actual

if st.session_state["pagina_anterior"] != pagina_actual:
    st.session_state["pagina_anterior"] = pagina_actual
    # Scroll al top — probamos múltiples selectores para compatibilidad
    components.html(
        """<script>
        var selectors = [
            'section.main',
            '[data-testid="stMain"]',
            '.main',
            'div.block-container',
        ];
        for (var s of selectors) {
            var el = window.parent.document.querySelector(s);
            if (el) { el.scrollTop = 0; break; }
        }
        window.parent.scrollTo(0, 0);
        </script>""",
        height=0
    )

def reproducir_musica_universo():
    """Reproduce música ambiental según el universo elegido."""
    universo_id = st.session_state.get("universo_elegido")
    if not universo_id or universo_id not in MUSICA_UNIVERSO:
        return
    ruta = Path(MUSICA_UNIVERSO[universo_id])
    if not ruta.exists():
        return
    # Leer audio y reproducir con autoplay
    audio_bytes = ruta.read_bytes()
    # Usar HTML para autoplay con loop y volumen bajo
    import base64
    b64 = base64.b64encode(audio_bytes).decode()
    st.markdown(
        f"""
        <audio id="seidr-audio" autoplay loop
               style="display:none">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        <script>
            var audio = document.getElementById('seidr-audio');
            if (audio) {{ audio.volume = 0.3; }}
        </script>
        """,
        unsafe_allow_html=True
    )


def pagina_sellada(nombre: str, runa: str,
                   mensaje: str = "Completa tu perfil para desvelarlo.",
                   destino_key: str = "ᚦ  Test de universo",
                   destino_label: str = "ᚦ Ir al test de universo"):
    """Módulo bloqueado — estética de piedra sellada con botón al test."""
    st.markdown(
        f"""
        <div style='max-width:600px;margin:4rem auto;text-align:center;'>
            <div style='background:linear-gradient(135deg,#1a1a1e 0%,#12121a 60%,#1e1a14 100%);
                        border:1px solid #3a3428;border-radius:8px;padding:3rem 2rem;
                        box-shadow:inset 0 0 40px rgba(0,0,0,0.6);
                        position:relative;overflow:hidden;'>
                <div style='font-size:4rem;color:#3a3428;margin-bottom:1.5rem;
                            filter:blur(0.5px);'>{runa}</div>
                <p style='font-family:Cinzel,serif;color:#5a5040;font-size:1.1rem;
                          letter-spacing:0.15em;margin:0 0 0.5rem;'>{nombre.upper()}</p>
                <p style='color:#4a4030;font-size:0.85rem;font-style:italic;
                          margin:0 0 2rem;line-height:1.6;'>
                    Este camino permanece sellado.<br>{mensaje}
                </p>
                <div style='border-top:1px solid #3a3428;margin:0 auto 1.5rem;width:60%;'></div>
                <p style='color:#6a5a40;font-size:0.8rem;margin:0;letter-spacing:0.05em;'>
                    ᚱ Para continuar, completa el test de perfil
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col = st.columns([1, 2, 1])[1]
    with col:
        if st.button(destino_label, use_container_width=True, key=f"btn_sellado_{runa}"):
            st.session_state["_pagina_activa"] = destino_key
            st.rerun()


# ─────────────────────────────────────────────
# ENRUTADOR
# ─────────────────────────────────────────────
pagina_id = MODULOS[pagina_actual]

# ── Música ambiental por universo ──
reproducir_musica_universo()

if pagina_id == "inicio":
    pagina_inicio()
elif pagina_id == "test_universo":
    pagina_test_universo()
elif pagina_id == "modulo_1":
    if not st.session_state.get("universo_elegido"):
        pagina_sellada("Tu perfil", "ᚨ", mensaje="Elige primero tu universo para descubrir tu perfil.",
                       destino_key="ᚦ  Test de universo", destino_label="ᚦ Ir al test de universo")
    else:
        pagina_modulo_1()
elif pagina_id == "modulo_2":
    if not st.session_state.get("test_dim_done"):
        pagina_sellada("Tu criatura", "ᚢ")
    else:
        pagina_modulo_2()
elif pagina_id == "modulo_3":
    if not st.session_state.get("test_dim_done"):
        pagina_sellada("Comunicación", "ᚲ")
    else:
        mostrar_modulo_3(orientacion_nd=st.session_state.get("orientacion_nd"))
elif pagina_id == "modulo_4":
    if not st.session_state.get("test_dim_done"):
        pagina_sellada("Aprendizaje", "ᚷ")
    else:
        mostrar_modulo_4(orientacion_nd=st.session_state.get("orientacion_nd"))
elif pagina_id == "modulo_5":
    if not st.session_state.get("test_dim_done"):
        pagina_sellada("Sociabilidad", "ᛉ")
    else:
        mostrar_modulo_5(orientacion_nd=st.session_state.get("orientacion_nd"))
elif pagina_id == "modulo_6":
    if not st.session_state.get("test_dim_done"):
        pagina_sellada("Tu cuerpo", "ᛊ")
    else:
        mostrar_modulo_6(orientacion_nd=st.session_state.get("orientacion_nd"))
elif pagina_id == "modulo_7":
    if not st.session_state.get("test_dim_done"):
        pagina_sellada("Orientación clínica", "ᛏ")
    else:
        mostrar_modulo_7(orientacion_nd=st.session_state.get("orientacion_nd"))
elif pagina_id == "profesional":
    try:
        from modo_profesional import pagina_profesional
        pagina_profesional()
    except ImportError:
        st.warning("Módulo modo_profesional no encontrado en hechizos/")
