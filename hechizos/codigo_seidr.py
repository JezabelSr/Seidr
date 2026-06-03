"""
SEIÐR — Sistema de códigos de regreso
Codifica el perfil completo en un string portable sin base de datos.

Formato: SEIDR-[U][PID]-[NDs]-[DIMS]
Ejemplo: SEIDR-1-51-TOC.AACC-54505005

Campos:
  U    = universo_id (1-6)
  PID  = personaje_id (1-999, 3 dígitos)
  NDs  = nombres ND separados por punto, abreviados
  DIMS = 8 dígitos, uno por dimensión (0-5, redondeado)
"""

# ── Mapeo universo_id → código ────────────────────────────────────────────────
UNIVERSO_CODIGO = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6"}
CODIGO_UNIVERSO = {v: k for k, v in UNIVERSO_CODIGO.items()}

NOMBRES_UNIVERSOS = {
    1: "Harry Potter",
    2: "La Brújula Dorada",
    3: "Pokémon",
    4: "Studio Ghibli",
    5: "Cómo entrenar a tu dragón",
    6: "Disney/Pixar",
}

# ── Abreviaturas de NDs ───────────────────────────────────────────────────────
ND_ABREV = {
    "Dislexia":                   "DIS",
    "TDAH":                       "TDA",
    "TEA":                        "TEA",
    "AACC":                       "AAC",
    "Discalculia":                "DCA",
    "Dispraxia/TDC":              "DPX",
    "Síndrome de Tourette":       "TOU",
    "SPD":                        "SPD",
    "Tartamudez":                 "TAR",
    "Discapacidad Intelectual":   "DIN",
    "TOC":                        "TOC",
    "Mutismo Selectivo":          "MUT",
    "Trastorno de Ansiedad Social": "TAS",
    "TANV":                       "TNV",
}
ABREV_ND = {v: k for k, v in ND_ABREV.items()}

# ── Orden de dimensiones ──────────────────────────────────────────────────────
DIMS_ORDEN = [
    "hiperfoco", "regulacion_emocional", "sensorialidad", "comunicacion",
    "aprendizaje", "sociabilidad", "propiocepcion", "funcion_ejecutiva",
]


def generar_codigo(
    universo_id: int,
    personaje_id: int,
    orientacion_nd: list,
    perfil_usuario: dict,
) -> str:
    """Genera el código de regreso a partir del perfil del usuario."""

    # Universo
    u = UNIVERSO_CODIGO.get(universo_id, str(universo_id))

    # Personaje ID (3 dígitos)
    pid = str(personaje_id).zfill(3)

    # NDs abreviadas
    if orientacion_nd:
        nds_str = ".".join(ND_ABREV.get(nd, nd[:3].upper()) for nd in orientacion_nd)
    else:
        nds_str = "NT"

    # Dimensiones (8 dígitos, valor 0-5 redondeado)
    dims_str = "".join(
        str(min(5, max(0, round(float(perfil_usuario.get(d, 0))))))
        for d in DIMS_ORDEN
    )

    return f"SEIDR-{u}-{pid}-{nds_str}-{dims_str}"


def decodificar_codigo(codigo: str) -> dict | None:
    """
    Decodifica un código de regreso.
    Devuelve dict con todos los campos o None si el código es inválido.
    """
    try:
        codigo = codigo.strip().upper()
        partes = codigo.split("-")

        if len(partes) != 5 or partes[0] != "SEIDR":
            return None

        _, u, pid, nds_str, dims_str = partes

        # Universo
        universo_id = CODIGO_UNIVERSO.get(u)
        if not universo_id:
            return None

        # Personaje ID
        personaje_id = int(pid)

        # NDs
        if nds_str == "NT":
            orientacion_nd = []
        else:
            orientacion_nd = [
                ABREV_ND.get(abrev, abrev)
                for abrev in nds_str.split(".")
            ]

        # Dimensiones
        if len(dims_str) != 8 or not dims_str.isdigit():
            return None

        perfil = {
            dim: float(dims_str[i])
            for i, dim in enumerate(DIMS_ORDEN)
        }

        return {
            "universo_id":    universo_id,
            "universo_nombre": NOMBRES_UNIVERSOS.get(universo_id, ""),
            "personaje_id":   personaje_id,
            "orientacion_nd": orientacion_nd,
            "perfil_usuario": perfil,
        }

    except Exception:
        return None


def validar_codigo(codigo: str) -> bool:
    return decodificar_codigo(codigo) is not None
