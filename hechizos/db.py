"""
SEIÐR — Capa de acceso a datos
Todos los módulos importan desde aquí en lugar de leer CSVs directamente.
Si la BD no existe, se crea automáticamente desde los CSVs.
"""

import pandas as pd
import streamlit as st
from pathlib import Path


def _get_conn():
    """Conexión a SQLite, creando la BD si no existe."""
    from crear_bd import get_conn
    return get_conn()


# ── Funciones de lectura ──────────────────────────────────────────────────────

@st.cache_data(ttl=3600)
def cargar_tabla(tabla: str) -> pd.DataFrame:
    """Carga una tabla completa de la BD."""
    try:
        conn = _get_conn()
        df = pd.read_sql(f"SELECT * FROM {tabla}", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error cargando tabla {tabla}: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def cargar_personajes(universo_id: int | None = None) -> pd.DataFrame:
    try:
        conn = _get_conn()
        if universo_id:
            df = pd.read_sql(
                "SELECT * FROM personajes WHERE universo_id = ?", conn,
                params=(universo_id,)
            )
        else:
            df = pd.read_sql("SELECT * FROM personajes", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def cargar_criaturas(universo_id: int | None = None) -> pd.DataFrame:
    try:
        conn = _get_conn()
        if universo_id:
            df = pd.read_sql(
                "SELECT * FROM criaturas WHERE universo_id = ?", conn,
                params=(universo_id,)
            )
        else:
            df = pd.read_sql("SELECT * FROM criaturas", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def cargar_preguntas(universo_id: int | None = None) -> pd.DataFrame:
    try:
        conn = _get_conn()
        if universo_id is not None:
            df = pd.read_sql(
                "SELECT * FROM preguntas WHERE universo_id = ?", conn,
                params=(universo_id,)
            )
        else:
            df = pd.read_sql("SELECT * FROM preguntas", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def cargar_razas() -> pd.DataFrame:
    return cargar_tabla("razas_akc_limpio")


@st.cache_data(ttl=3600)
def cargar_perfiles_nd() -> pd.DataFrame:
    return cargar_tabla("perfiles_nd_clinicos")


@st.cache_data(ttl=3600)
def cargar_contenido_modulos() -> pd.DataFrame:
    return cargar_tabla("contenido_modulos")


@st.cache_data(ttl=3600)
def cargar_recursos(modulo: int | None = None) -> pd.DataFrame:
    try:
        conn = _get_conn()
        if modulo:
            df = pd.read_sql(
                "SELECT * FROM recursos WHERE modulo = ?", conn,
                params=(modulo,)
            )
        else:
            df = pd.read_sql("SELECT * FROM recursos", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def cargar_organizaciones() -> pd.DataFrame:
    return cargar_tabla("organizaciones_espana")


def limpiar_cache():
    """Limpia la caché de Streamlit — usar tras recrear la BD."""
    cargar_tabla.clear()
    cargar_personajes.clear()
    cargar_criaturas.clear()
    cargar_preguntas.clear()
    cargar_razas.clear()
    cargar_perfiles_nd.clear()
    cargar_contenido_modulos.clear()
    cargar_recursos.clear()
    cargar_organizaciones.clear()
