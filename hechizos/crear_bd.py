"""
SEIÐR — Script de creación y migración a SQLite
Ejecutar desde la raíz del proyecto: python hechizos/crear_bd.py

Los CSVs son la fuente de verdad.
Este script crea seidr.db desde cero cada vez que se llama.
Se llama automáticamente desde app.py si la BD no existe.
"""

import sqlite3
import pandas as pd
from pathlib import Path
import sys

# ── Rutas ────────────────────────────────────────────────────────────────────

RUTA_BD     = Path("seidr.db")
RUTA_BASE   = Path("universos")
RUTA_RR     = RUTA_BASE / "recursos_reales"

CSVS = {
    "universos":            RUTA_BASE / "universos.csv",
    "personajes":           RUTA_BASE / "personajes.csv",
    "criaturas":            RUTA_BASE / "criaturas.csv",
    "preguntas":            RUTA_BASE / "preguntas.csv",
    "perfiles_nd_clinicos": RUTA_BASE / "perfiles_nd_clinicos.csv",
    "razas_akc_limpio":     RUTA_BASE / "razas_akc_limpio.csv",
    "contenido_modulos":    RUTA_BASE / "contenido_modulos.csv",
    "recursos":             RUTA_RR   / "recursos.csv",
    "organizaciones_espana":RUTA_RR   / "organizaciones_espana.csv",
}


# ── Función principal ─────────────────────────────────────────────────────────

def crear_bd(forzar: bool = False) -> bool:
    """
    Crea seidr.db desde los CSVs.
    
    - Si la BD ya existe y forzar=False, no hace nada.
    - Si forzar=True o la BD no existe, la crea desde cero.
    
    Devuelve True si creó/actualizó, False si ya existía y no se forzó.
    """
    if RUTA_BD.exists() and not forzar:
        return False

    print("🗡️  Seiðr — Construyendo base de datos...")

    if RUTA_BD.exists():
        RUTA_BD.unlink()

    conn = sqlite3.connect(RUTA_BD)

    errores = []
    for tabla, ruta_csv in CSVS.items():
        if not ruta_csv.exists():
            print(f"  ⚠️  {tabla}: CSV no encontrado en {ruta_csv}")
            errores.append(tabla)
            continue
        try:
            df = pd.read_csv(ruta_csv, encoding="utf-8-sig")
            # Limpiar BOM en nombres de columnas
            df.columns = [c.strip().lstrip("\ufeff") for c in df.columns]
            df.to_sql(tabla, conn, if_exists="replace", index=False)
            print(f"  ✅ {tabla}: {len(df)} filas")
        except Exception as e:
            print(f"  ❌ {tabla}: error — {e}")
            errores.append(tabla)

    # Crear índices para las consultas más frecuentes
    cur = conn.cursor()
    indices = [
        "CREATE INDEX IF NOT EXISTS idx_personajes_universo ON personajes(universo_id)",
        "CREATE INDEX IF NOT EXISTS idx_criaturas_universo  ON criaturas(universo_id)",
        "CREATE INDEX IF NOT EXISTS idx_preguntas_universo  ON preguntas(universo_id)",
        "CREATE INDEX IF NOT EXISTS idx_contenido_nd        ON contenido_modulos(nd, modulo)",
        "CREATE INDEX IF NOT EXISTS idx_recursos_modulo     ON recursos(modulo)",
    ]
    for idx_sql in indices:
        try:
            cur.execute(idx_sql)
        except Exception:
            pass

    conn.commit()
    conn.close()

    if errores:
        print(f"\n⚠️  BD creada con {len(errores)} tabla(s) con errores: {errores}")
    else:
        print(f"\n✅ BD creada correctamente en {RUTA_BD}")

    return True


def get_conn() -> sqlite3.Connection:
    """Devuelve una conexión a la BD, creándola si no existe."""
    crear_bd(forzar=False)
    return sqlite3.connect(RUTA_BD)


if __name__ == "__main__":
    forzar = "--forzar" in sys.argv or "-f" in sys.argv
    crear_bd(forzar=forzar)
