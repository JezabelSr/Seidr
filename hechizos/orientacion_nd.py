import pandas as pd
import numpy as np

dimensiones = [
    "hiperfoco", "reg_emocional", "sensorialidad",
    "comunicacion", "aprendizaje", "sociabilidad",
    "propiocepcion", "f_ejecutiva"
]

dimensiones_clave = {
    "Dislexia":                                ["aprendizaje", "comunicacion"],
    "TDAH":                                    ["hiperfoco", "f_ejecutiva"],
    "TEA":                                     ["hiperfoco", "sociabilidad"],
    "AACC":                                    ["hiperfoco", "aprendizaje"],
    "Discalculia":                             ["aprendizaje"],
    "Dispraxia/TDC":                           ["propiocepcion"],
    "Disgrafía":                               ["comunicacion"],
    "Síndrome de Tourette":                    ["sensorialidad"],
    "TEL":                                     ["comunicacion"],
    "SPD":                                     ["sensorialidad", "reg_emocional"],
    "Tartamudez":                              ["comunicacion"],
    "Discapacidad Intelectual":                ["aprendizaje", "f_ejecutiva"],
    "TOC":                                     ["hiperfoco", "f_ejecutiva"],
    "Mutismo Selectivo":                       ["comunicacion", "sociabilidad"],
    "Síndrome de Irlen":                       ["sensorialidad", "aprendizaje"],
    "Trastorno Fonológico":                    ["comunicacion"],
    "Trastorno de Comunicación Social":        ["comunicacion", "sociabilidad"],
    "Trastorno por Movimientos Estereotipados": ["propiocepcion", "f_ejecutiva"],
    "Trastorno de Ansiedad Social":            ["sociabilidad", "reg_emocional"],
    "TANV":                                    ["aprendizaje", "propiocepcion"]
}

def orientar_nd(perfil_usuario, df_nd, umbral=7):
    """
    Orienta el perfil del usuario hacia las ND más probables.
    Fuente clínica: DSM-5 / ICD-11

    Parámetros:
    - perfil_usuario: dict con puntuaciones 0-5 para las 8 dimensiones
    - df_nd: dataframe con perfiles clínicos (perfiles_nd_clinicos.csv)
    - umbral: mínimo de dimensiones en rango (default=7)

    Retorna: dataframe con orientación ND
    """
    resultados = []

    for _, row in df_nd.iterrows():
        nd_nombre = row["nombre"]
        claves = dimensiones_clave.get(nd_nombre, [])

        claves_ok = all(
            row[f"{dim}_min"] <= perfil_usuario[dim] <= row[f"{dim}_max"]
            for dim in claves
        )
        if not claves_ok:
            continue

        dims_en_rango = []
        for dim in dimensiones:
            if row[f"{dim}_min"] <= perfil_usuario[dim] <= row[f"{dim}_max"]:
                dims_en_rango.append(dim)

        porcentaje = round((len(dims_en_rango) / len(dimensiones)) * 100, 1)
        vector_nd = np.array([row[f"{dim}_medio"] for dim in dimensiones])
        vector_usr = np.array([perfil_usuario[dim] for dim in dimensiones])
        distancia = round(np.sqrt(np.sum((vector_usr - vector_nd) ** 2)), 2)

        resultados.append({
            "nd_id": row["nd_id"],
            "nombre": nd_nombre,
            "dims_en_rango": len(dims_en_rango),
            "porcentaje": porcentaje,
            "distancia": distancia
        })

    if not resultados:
        return pd.DataFrame([{
            "posicion": 1, "nd_id": 0,
            "nombre": "Perfil Neurotípico",
            "etiqueta": "Sin coincidencias ND",
            "coincidencia": "-"
        }])

    df_res = pd.DataFrame(resultados).sort_values(
        ["dims_en_rango", "distancia"],
        ascending=[False, True]
    ).reset_index(drop=True)

    salida = []
    nd_8 = df_res[df_res["dims_en_rango"] == 8]
    nd_7 = df_res[df_res["dims_en_rango"] >= umbral]

    if len(nd_8) >= 1:
        for i, (_, row) in enumerate(nd_8.head(2).iterrows()):
            salida.append({
                "posicion": i + 1,
                "nd_id": row["nd_id"],
                "nombre": row["nombre"],
                "etiqueta": "Perfil compatible",
                "coincidencia": "100%"
            })
    elif len(nd_7) >= 1:
        mejor = nd_7.iloc[0]
        salida.append({
            "posicion": 1,
            "nd_id": mejor["nd_id"],
            "nombre": mejor["nombre"],
            "etiqueta": "Posible perfil",
            "coincidencia": f"{mejor['porcentaje']}%"
        })
    else:
        salida.append({
            "posicion": 1,
            "nd_id": 0,
            "nombre": "Perfil Neurotípico",
            "etiqueta": "Sin coincidencias ND",
            "coincidencia": "-"
        })

    return pd.DataFrame(salida)
