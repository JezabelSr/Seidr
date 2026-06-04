import pandas as pd
import numpy as np

dimensiones = [
    "hiperfoco", "reg_emocional", "sensorialidad",
    "comunicacion", "aprendizaje", "sociabilidad",
    "propiocepcion", "f_ejecutiva"
]

dimensiones_clave = {
    "Dislexia":                     ["aprendizaje", "comunicacion"],
    "TDAH":                         ["hiperfoco", "f_ejecutiva"],
    "TEA":                          ["hiperfoco", "sociabilidad"],
    "AACC":                         ["hiperfoco", "aprendizaje"],
    "Discalculia":                  ["aprendizaje"],
    "Dispraxia/TDC":                ["propiocepcion"],
    "Síndrome de Tourette":         ["sensorialidad"],
    "SPD":                          ["sensorialidad", "reg_emocional"],
    "Tartamudez":                   ["comunicacion"],
    "Discapacidad Intelectual":     ["aprendizaje", "f_ejecutiva"],
    "TOC":                          ["hiperfoco", "f_ejecutiva"],
    "Mutismo Selectivo":            ["comunicacion", "sociabilidad"],
    "Trastorno de Ansiedad Social": ["sociabilidad", "reg_emocional"],
    "TANV":                         ["aprendizaje", "propiocepcion"],
}

# Banda central NT: todas las dimensiones entre estos valores → Perfil Neurotípico
NT_MIN = 1.5
NT_MAX = 3.5


def _es_perfil_nt(perfil_usuario: dict) -> bool:
    """Devuelve True si todas las dimensiones están dentro de la banda NT."""
    return all(NT_MIN <= perfil_usuario.get(d, 0) <= NT_MAX for d in dimensiones)


def _es_perfil_atipico(perfil_usuario: dict) -> bool:
    """
    Devuelve True si hay picos fuera de la banda NT pero el algoritmo
    no encuentra ninguna ND con suficiente coincidencia.
    Se usa después de comprobar que no es NT y no hay resultados ND.
    """
    return any(
        perfil_usuario.get(d, 0) < NT_MIN or perfil_usuario.get(d, 0) > NT_MAX
        for d in dimensiones
    )


def orientar_nd(perfil_usuario, df_nd, umbral=7):
    """
    Orienta el perfil del usuario hacia una o dos NDs, NT o perfil atípico.

    Cambios respecto a v1:
    - NT definido activamente (banda 1.5-3.5 en todas las dimensiones)
    - Perfil atípico: picos fuera de banda pero sin ND definida
    - Umbral bajado de 8 a 7 para "Perfil compatible"
    - 6/8 dimensiones → "Posible perfil"
    """

    # ── 1. Comprobar NT activo ──────────────────────────────────────────────
    if _es_perfil_nt(perfil_usuario):
        return pd.DataFrame([{
            "posicion":    1,
            "nd_id":       0,
            "nombre":      "Perfil Neurotípico",
            "etiqueta":    "Perfil neurotípico",
            "coincidencia": "-"
        }])

    # ── 2. Buscar coincidencias ND ──────────────────────────────────────────
    resultados = []

    for _, row in df_nd.iterrows():
        nd_nombre = row["nombre"]
        claves = dimensiones_clave.get(nd_nombre, [])

        claves_ok = all(
            row[f"{dim}_min"] <= perfil_usuario.get(dim, 0) <= row[f"{dim}_max"]
            for dim in claves
        )
        if not claves_ok:
            continue

        dims_en_rango = []
        for dim in dimensiones:
            if row[f"{dim}_min"] <= perfil_usuario.get(dim, 0) <= row[f"{dim}_max"]:
                dims_en_rango.append(dim)

        porcentaje = round((len(dims_en_rango) / len(dimensiones)) * 100, 1)
        vector_nd  = np.array([row[f"{dim}_medio"] for dim in dimensiones])
        vector_usr = np.array([perfil_usuario.get(dim, 0) for dim in dimensiones])
        distancia  = round(np.sqrt(np.sum((vector_usr - vector_nd) ** 2)), 2)

        resultados.append({
            "nd_id":         row["nd_id"],
            "nombre":        nd_nombre,
            "dims_en_rango": len(dims_en_rango),
            "porcentaje":    porcentaje,
            "distancia":     distancia
        })

    # ── 3. Sin resultados → atípico o NT ───────────────────────────────────
    if not resultados:
        if _es_perfil_atipico(perfil_usuario):
            return pd.DataFrame([{
                "posicion":    1,
                "nd_id":       -1,
                "nombre":      "Perfil Atípico",
                "etiqueta":    "Perfil no parametrizable",
                "coincidencia": "-"
            }])
        else:
            return pd.DataFrame([{
                "posicion":    1,
                "nd_id":       0,
                "nombre":      "Perfil Neurotípico",
                "etiqueta":    "Perfil neurotípico",
                "coincidencia": "-"
            }])

    # ── 4. Ordenar y seleccionar ────────────────────────────────────────────
    df_res = pd.DataFrame(resultados).sort_values(
        ["dims_en_rango", "distancia"],
        ascending=[False, True]
    ).reset_index(drop=True)

    salida = []

    # 7/8 o más → Perfil compatible
    nd_top = df_res[df_res["dims_en_rango"] >= umbral]
    # 6/8 → Posible perfil
    nd_posible = df_res[df_res["dims_en_rango"] >= 6]

    if len(nd_top) >= 1:
        for i, (_, row) in enumerate(nd_top.head(2).iterrows()):
            salida.append({
                "posicion":    i + 1,
                "nd_id":       row["nd_id"],
                "nombre":      row["nombre"],
                "etiqueta":    "Perfil compatible",
                "coincidencia": f"{row['porcentaje']}%"
            })
    elif len(nd_posible) >= 1:
        mejor = nd_posible.iloc[0]
        salida.append({
            "posicion":    1,
            "nd_id":       mejor["nd_id"],
            "nombre":      mejor["nombre"],
            "etiqueta":    "Posible perfil",
            "coincidencia": f"{mejor['porcentaje']}%"
        })
    else:
        # Hay resultados pero ninguno llega a 6/8 → atípico
        if _es_perfil_atipico(perfil_usuario):
            salida.append({
                "posicion":    1,
                "nd_id":       -1,
                "nombre":      "Perfil Atípico",
                "etiqueta":    "Perfil no parametrizable",
                "coincidencia": "-"
            })
        else:
            salida.append({
                "posicion":    1,
                "nd_id":       0,
                "nombre":      "Perfil Neurotípico",
                "etiqueta":    "Perfil neurotípico",
                "coincidencia": "-"
            })

    return pd.DataFrame(salida)
