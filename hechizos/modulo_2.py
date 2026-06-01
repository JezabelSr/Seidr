"""
SEIÐR — Módulo 2: Tu criatura de asistencia
Asigna la criatura más afín al perfil del usuario y muestra su equivalente en raza real
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# Mapa de dimensiones del perfil → variables de criatura
# La criatura que mejor encaja es la que más se parece al perfil en estas 4 dimensiones
MAPA_DIMS_CRIATURA = {
    "calma":        "regulacion_emocional",  # alta reg. emocional → criatura calmada
    "vinculo":      "sociabilidad",           # alta sociabilidad → criatura con vínculo fuerte
    "estimulacion": "hiperfoco",              # alto hiperfoco → criatura estimulante
    "independencia":"funcion_ejecutiva",      # alta f.ejecutiva → criatura independiente
}

UNIVERSOS_COPYRIGHT = {
    1: "© Warner Bros. / J.K. Rowling",
    2: "© New Line Cinema / Philip Pullman",
    3: "© Nintendo / The Pokémon Company",
    4: "© Studio Ghibli",
    5: "© DreamWorks Animation",
    6: "© The Walt Disney Company / Pixar",
}


@st.cache_data
def cargar_criaturas(universo_id: int):
    try:
        df = pd.read_csv("universos/criaturas.csv", engine="python")
        return df[df["universo_id"] == universo_id].reset_index(drop=True)
    except Exception:
        return pd.DataFrame()


@st.cache_data
def cargar_razas():
    try:
        return pd.read_csv("universos/razas_akc_limpio.csv", engine="python")
    except Exception:
        return pd.DataFrame()


def encontrar_criatura(perfil: dict, criaturas: pd.DataFrame) -> pd.Series:
    """Encuentra la criatura más afín al perfil usando distancia euclidiana."""
    min_dist = float("inf")
    mejor = None
    for _, row in criaturas.iterrows():
        try:
            dist = np.sqrt(sum(
                (float(perfil.get(dim_perfil, 0)) - float(row[dim_criatura])) ** 2
                for dim_criatura, dim_perfil in MAPA_DIMS_CRIATURA.items()
            ))
            if dist < min_dist:
                min_dist = dist
                mejor = row
        except Exception:
            continue
    return mejor


def cargar_imagen(url: str):
    """Muestra imagen desde ruta local o URL."""
    if not url or str(url).strip() in ("", "nan"):
        st.markdown(
            "<div style='background:#1a1a28;border:1px solid #2a2a3a;"
            "border-radius:4px;padding:3rem;text-align:center;color:#555'>ᚱ</div>",
            unsafe_allow_html=True
        )
        return
    try:
        p = Path(str(url))
        if p.exists():
            st.image(str(p), use_container_width=True)
        else:
            st.image(str(url), use_container_width=True)
    except Exception:
        pass


def pagina_modulo_2():
    universo_id   = st.session_state.get("universo_elegido")
    universo_nombre = st.session_state.get("universo_nombre", "tu universo")
    perfil        = st.session_state.get("perfil_usuario")

    # Cabecera
    st.markdown(
        "<div style='text-align:center;padding:1.5rem 0 1rem'>"
        "<h1 style=\"font-family:'Cinzel',serif;color:#c9a84c;"
        "letter-spacing:0.1em;font-size:1.8rem\">ᚢ Tu criatura de asistencia</h1>"
        "<p style='color:#9a9080;font-style:italic'>"
        f"Universo: {universo_nombre}</p></div>",
        unsafe_allow_html=True
    )

    if not universo_id:
        st.warning("Primero completa el test de universo.")
        return

    if not perfil:
        st.warning("Primero completa el test de perfil en el Módulo 1.")
        return

    criaturas = cargar_criaturas(universo_id)
    razas = cargar_razas()

    if criaturas.empty:
        st.error(f"No hay criaturas para el universo {universo_id}.")
        return

    criatura = encontrar_criatura(perfil, criaturas)
    if criatura is None:
        st.error("No se pudo asignar una criatura.")
        return

    # Guardar en sesión
    st.session_state.criatura_asignada = criatura["nombre"]

    # ── CRIATURA ──
    st.markdown("---")
    st.markdown(
        "<h2 style=\"font-family:'Cinzel',serif;color:#c9a84c;"
        "font-size:1.2rem;text-align:center\">Tu criatura</h2>",
        unsafe_allow_html=True
    )

    col_img, col_desc = st.columns([1, 2])
    with col_img:
        cargar_imagen(criatura.get("url_imagen", ""))
        copyright_txt = UNIVERSOS_COPYRIGHT.get(universo_id, "")
        if copyright_txt:
            st.markdown(
                f"<p style='color:#555;font-size:0.7rem;text-align:center;margin-top:0.3rem'>"
                f"{copyright_txt}. Uso educativo no comercial.</p>",
                unsafe_allow_html=True
            )

    with col_desc:
        st.markdown(
            f"<p style=\"font-family:'Cinzel',serif;color:#c9a84c;"
            f"font-size:1.1rem;margin-bottom:0.5rem\">{criatura['nombre']}</p>",
            unsafe_allow_html=True
        )
        descripcion = str(criatura.get("descripcion", ""))
        if descripcion and descripcion != "nan":
            st.markdown(
                f"<p style='color:#e8e0d0;font-size:0.9rem;line-height:1.6'>"
                f"{descripcion}</p>",
                unsafe_allow_html=True
            )

        # Barras de las 4 dimensiones de la criatura
        st.markdown("<br>", unsafe_allow_html=True)
        dims_criatura = {
            "Calma":         float(criatura.get("calma", 0)),
            "Vínculo":       float(criatura.get("vinculo", 0)),
            "Estimulación":  float(criatura.get("estimulacion", 0)),
            "Independencia": float(criatura.get("independencia", 0)),
        }
        for nombre_dim, valor in dims_criatura.items():
            pct = int((valor / 5) * 100)
            st.markdown(
                f"<div style='margin-bottom:0.6rem'>"
                f"<p style=\"font-family:'Cinzel',serif;color:#c9a84c;"
                f"font-size:0.75rem;margin:0 0 0.2rem\">{nombre_dim}</p>"
                f"<div style='background:#2a2a3a;border-radius:2px;height:5px'>"
                f"<div style='background:#c9a84c;width:{pct}%;height:5px;"
                f"border-radius:2px'></div></div></div>",
                unsafe_allow_html=True
            )

    # ── RAZA REAL ──
    raza_id = criatura.get("raza_real_id")
    if pd.notna(raza_id) and not razas.empty:
        st.markdown("---")
        st.markdown(
            "<h2 style=\"font-family:'Cinzel',serif;color:#c9a84c;"
            "font-size:1.2rem;text-align:center\">Su equivalente real</h2>",
            unsafe_allow_html=True
        )

        explicacion = str(criatura.get("explicacion_equivalencia", ""))
        if explicacion and explicacion != "nan":
            st.markdown(
                f"<div style='background:#1a1a28;border-left:3px solid #4a7fa5;"
                f"padding:1rem 1.5rem;border-radius:0 4px 4px 0;margin-bottom:1.5rem'>"
                f"<p style='color:#9a9080;font-size:0.85rem;line-height:1.6;margin:0'>"
                f"{explicacion}</p></div>",
                unsafe_allow_html=True
            )

        # Buscar la raza — puede ser ID numérico o nombre directo
        raza = None
        try:
            rid = str(raza_id).strip()
            if rid.isdigit() and int(rid) > 0:
                raza = razas.iloc[int(rid) - 1]
            else:
                # Buscar por nombre de raza
                match = razas[razas["breed"].str.lower() == rid.lower()]
                if not match.empty:
                    raza = match.iloc[0]
        except Exception:
            raza = None

        if raza is not None:
            col_raza_img, col_raza_info = st.columns([1, 2])

            with col_raza_img:
                cargar_imagen(raza.get("url_imagen", ""))

            with col_raza_info:
                st.markdown(
                    f"<p style=\"font-family:'Cinzel',serif;color:#c9a84c;"
                    f"font-size:1.1rem;margin-bottom:0.8rem\">{raza['breed']}</p>",
                    unsafe_allow_html=True
                )

                # Carácter
                caracter = str(raza.get("caracter", ""))
                if caracter and caracter != "nan":
                    st.markdown(
                        f"<p style='color:#e8e0d0;font-size:0.9rem;line-height:1.6;"
                        f"margin-bottom:1rem'>{caracter}</p>",
                        unsafe_allow_html=True
                    )

                # Datos estándar
                datos = []
                if pd.notna(raza.get("min_height")) and pd.notna(raza.get("max_height")):
                    datos.append(f"📏 Altura: {int(raza['min_height'])}-{int(raza['max_height'])} cm")
                if pd.notna(raza.get("min_weight")) and pd.notna(raza.get("max_weight")):
                    datos.append(f"⚖️ Peso: {int(raza['min_weight'])}-{int(raza['max_weight'])} kg")
                if pd.notna(raza.get("min_expectancy")) and pd.notna(raza.get("max_expectancy")):
                    datos.append(f"🕰️ Esperanza de vida: {int(raza['min_expectancy'])}-{int(raza['max_expectancy'])} años")
                if raza.get("group"):
                    datos.append(f"🏷️ Grupo: {raza['group']}")

                for dato in datos:
                    st.markdown(
                        f"<p style='color:#9a9080;font-size:0.85rem;margin:0.2rem 0'>{dato}</p>",
                        unsafe_allow_html=True
                    )

    # ── Siguiente paso ──
    st.markdown("---")
    st.markdown(
        "<div style='background:#1a1a28;border-left:3px solid #c9a84c;"
        "padding:1rem 1.5rem;border-radius:0 4px 4px 0;text-align:center'>"
        "<p style='color:#9a9080;font-size:0.9rem;margin:0'>"
        "← Selecciona <strong style='color:#c9a84c'>ᚲ Módulo 3 · Comunicación</strong> "
        "en el menú lateral para continuar</p></div>",
        unsafe_allow_html=True
    )
