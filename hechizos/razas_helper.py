"""
SEIÐR — Helper para buscar razas
- Universos 1-2: raza_real_id es un número (índice 1-based en CSV)
- Universos 3-6: raza_real_id es el nombre en inglés directamente
- La explicacion_equivalencia puede o no tener el formato "Nombre — descripción"
"""

# Mapeo nombre en español → nombre en inglés (para universos 1-2)
MAPA_RAZA_ES_EN = {
    "Alaskan Malamute":              "Alaskan Malamute",
    "Australian Shepherd":           "Australian Shepherd",
    "Basenji":                       "Basenji",
    "Basset Hound":                  "Basset Hound",
    "Beagle":                        "Beagle",
    "Bichón Maltés":                 "Maltese",
    "Bloodhound":                    "Bloodhound",
    "Border Collie":                 "Border Collie",
    "Borzoi":                        "Borzoi",
    "Bulldog Inglés":                "Bulldog",
    "Caucasian Shepherd":            "Caucasian Shepherd Dog",
    "Cavalier King Charles Spaniel": "Cavalier King Charles Spaniel",
    "Chihuahua":                     "Chihuahua",
    "Coonhound":                     "American English Coonhound",
    "Corgi":                         "Pembroke Welsh Corgi",
    "Dálmata":                       "Dalmatian",
    "Dobermann":                     "Doberman Pinscher",
    "Fila Brasileiro":               "Neapolitan Mastiff",
    "Galgo":                         "Greyhound",
    "Galgo Afgano":                  "Afghan Hound",
    "Golden Retriever":              "Golden Retriever",
    "Gran Danés":                    "Great Dane",
    "Husky":                         "Siberian Husky",
    "Husky Siberiano":               "Siberian Husky",
    "Jack Russell Terrier":          "Russell Terrier",
    "Labrador Retriever":            "Labrador Retriever",
    "Leonberger":                    "Leonberger",
    "Mastín Napolitano":             "Neapolitan Mastiff",
    "Pastor Belga Malinois":         "Belgian Malinois",
    "Perro de Groenlandia":          "Alaskan Malamute",
    "Pharaoh Hound":                 "Pharaoh Hound",
    "Pinscher Miniatura":            "Miniature Pinscher",
    "Pomerania":                     "Pomeranian",
    "Poodle":                        "Poodle (Standard)",
    "Rottweiler":                    "Rottweiler",
    "Saluki":                        "Saluki",
    "Samoyedo":                      "Samoyed",
    "Shar Pei":                      "Chinese Shar-Pei",
    "Shiba Inu":                     "Shiba Inu",
    "Terranova":                     "Newfoundland",
    "Tosa Inu":                      "Tosa",
    "Whippet":                       "Whippet",
}


def buscar_raza(raza_real_id, explicacion: str, df_razas) -> tuple:
    """
    Busca la raza correcta y devuelve (fila_raza, nombre_display).
    
    Lógica:
    - Si raza_real_id es numérico → universos 1-2: extraer nombre del texto de equivalencia
      y buscar en el CSV por ese nombre usando el mapeo ES→EN
    - Si raza_real_id es texto → universos 3-6: buscar directamente en el CSV por ese nombre
    
    Devuelve (pd.Series | None, str)
    """
    raza = None
    nombre_display = ""

    rid = str(raza_real_id).strip()
    if rid.endswith(".0"):
        rid = rid[:-2]

    # ── Caso A: raza_real_id es numérico (universos 1-2) ──
    if rid.isdigit() and int(rid) > 0:
        # Extraer nombre del texto de equivalencia
        equiv = str(explicacion) if explicacion else ""
        if " — " in equiv:
            nombre_display = equiv.split(" — ")[0].strip()
        elif " - " in equiv:
            nombre_display = equiv.split(" - ")[0].strip()

        # Traducir al inglés y buscar en CSV
        nombre_en = MAPA_RAZA_ES_EN.get(nombre_display, "")
        if nombre_en:
            match = df_razas[df_razas["breed"] == nombre_en]
            if not match.empty:
                raza = match.iloc[0]
        # Fallback: búsqueda parcial
        if raza is None and nombre_display:
            match = df_razas[df_razas["breed"].str.lower().str.contains(
                nombre_display.lower().split()[0], na=False)]
            if not match.empty:
                raza = match.iloc[0]

    # ── Caso B: raza_real_id ya es el nombre en inglés (universos 3-6) ──
    elif rid and rid.lower() not in ("nan", "none", ""):
        # Buscar directamente por nombre exacto
        match = df_razas[df_razas["breed"] == rid]
        if match.empty:
            # Búsqueda parcial
            match = df_razas[df_razas["breed"].str.lower().str.contains(
                rid.lower().split()[0], na=False)]
        if not match.empty:
            raza = match.iloc[0]
            nombre_display = rid  # El nombre en inglés es el display

    return raza, nombre_display
