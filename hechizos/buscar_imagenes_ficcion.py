"""
SEIÐR — Script de búsqueda de URLs de imágenes para personajes y criaturas
Busca en wikis de Fandom la imagen principal de cada personaje/criatura
Ejecutar desde la raíz del proyecto: python hechizos/buscar_imagenes_ficcion.py
"""

import pandas as pd
import requests
import time
from pathlib import Path

PERSONAJES_CSV = "universos/personajes.csv"
CRIATURAS_CSV  = "universos/criaturas.csv"
HEADERS = {"User-Agent": "Seidr/1.0 (github.com/JezabelSr/Seidr)"}
PAUSA = 1.0

# Wiki principal por universo_id
WIKIS = {
    1: "harrypotter.fandom.com",
    2: "darkmaterials.fandom.com",
    3: "pokemon.fandom.com",
    4: "ghibli.fandom.com",
    5: "howtotrainyourdragon.fandom.com",
    6: "disney.fandom.com",
}

# Nombres que en la wiki tienen un título diferente al nombre en el CSV
NOMBRES_ESPECIALES_PERSONAJES = {
    "Ash":              "Ash_Ketchum",
    "Hipo":             "Hiccup_Horrendous_Haddock_III",
    "Astrid":           "Astrid_Hofferson",
    "Patapez":          "Snotlout_Jorgenson",
    "Mocoso":           "Ruffnut_Thorston",
    "Chusco":           "Tuffnut_Thorston",
    "Brusca":           "Ruffnut_Thorston",
    "Bocón":            "Fishlegs_Ingerman",
    "Estoico el inmenso":"Stoick_the_Vast",
    "Drago Puño Sangriento": "Drago_Bludvist",
    "El padre Gomez":   "Father_Gomez",
    "Mrs. Coulter":     "Marisa_Coulter",
    "Lord Asriel":      "Lord_Asriel",
    "Gary":             "Gary_De%27Snake",
    "Numero 22":        "22_(Soul)",
    "Número 22":        "22_(Soul)",
    "Nilo Fuentes":     "Wade_Ripple",
    "Candela Lumen":    "Ember_(Elemental)",
    "Tristeza":         "Sadness_(Inside_Out)",
    "Estrella":         "Joy_(Inside_Out)",
    "Ansiedad":         "Anxiety_(Inside_Out_2)",
    "Basile":           "Basil_of_Baker_Street",
    "Arthur/Grillo":    "Jiminy_Cricket",
    "Kronk":            "Kronk_(The_Emperor%27s_New_Groove)",
    "Edna Moda":        "Edna_Mode",
    "Rayo McQueen":     "Lightning_McQueen",
    "Bruno Madrigal":   "Bruno_Madrigal",
}

NOMBRES_ESPECIALES_CRIATURAS = {
    "Desdentado":       "Toothless_(How_to_Train_Your_Dragon)",
    "Tormenta":         "Stormfly",
    "Barrilete":        "Meatlug",
    "Vómito y Eructo":  "Barf_and_Belch",
    "Colmillo":         "Hookfang",
    "Rompecráneos":     "Skullcrusher",
    "Asaltanubes":      "Cloudjumper",
    "Furia Diurna":     "Light_Fury",
    "GatoBus":          "Catbus",
    "Totoro grande":    "Totoro",
    "Susuwataris":      "Soot_Sprites",
    "Los Kodama":       "Kodama_(Princess_Mononoke)",
    "Espantapájaros Cabeza de Nabo": "Turnip-Head",
    "Gran Pabbie":      "Grand_Pabbie",
    "Escarbato":        "Niffler",
    "Snidget dorado":   "Golden_Snidget",
    "El basilisco":     "Basilisk_(Harry_Potter)",
    "Micropuff":        "Pygmy_Puff",
    "Pan":              "Pantalaimon",
    "Panserbjørne":     "Armoured_bear",
    "Vómito y Eructo":  "Barf_and_Belch",
    "Bing Bong":        "Bing_Bong_(Inside_Out)",
    "Machiavelli":      "Machiavelli_(Luca)",
    "El Nokk":          "The_Nokk",
}


def buscar_imagen_fandom(nombre, wiki, nombres_especiales={}):
    titulo = nombres_especiales.get(nombre, nombre.replace(" ", "_"))
    api_url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "titles": titulo.replace("_", " "),
        "prop": "pageimages",
        "pithumbsize": 600,
        "format": "json"
    }
    try:
        r = requests.get(api_url, params=params, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            pages = data.get("query", {}).get("pages", {})
            for page in pages.values():
                if "missing" in page:
                    return None
                thumb = page.get("thumbnail", {}).get("source")
                if thumb:
                    return thumb
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None


def procesar_csv(csv_path, nombres_especiales, tipo):
    df = pd.read_csv(csv_path)
    df["url_imagen"] = df["url_imagen"].astype(str).fillna("").replace("nan", "")

    total = len(df)
    encontradas = 0
    no_encontradas = []

    print(f"\n{'='*60}")
    print(f"SEIÐR — Buscando imágenes: {tipo} ({total})")
    print(f"{'='*60}")

    for i, row in df.iterrows():
        nombre = str(row["nombre"])
        uid = int(row["universo_id"])

        # Saltar si ya tiene URL
        if row["url_imagen"] and row["url_imagen"] not in ("", "nan"):
            print(f"[{i+1}/{total}] ⏭️  Ya tiene imagen: {nombre}")
            continue

        wiki = WIKIS.get(uid)
        if not wiki:
            print(f"[{i+1}/{total}] ⚠️  Sin wiki para universo {uid}: {nombre}")
            continue

        print(f"[{i+1}/{total}] 🔍 {nombre}", end=" ... ", flush=True)
        url = buscar_imagen_fandom(nombre, wiki, nombres_especiales)

        if url:
            df.at[i, "url_imagen"] = url
            encontradas += 1
            print(f"✅")
        else:
            no_encontradas.append(nombre)
            print(f"❌")

        time.sleep(PAUSA)

    df.to_csv(csv_path, index=False)

    print(f"\n✅ Encontradas: {encontradas}/{total}")
    print(f"⚠️  No encontradas ({len(no_encontradas)}): {no_encontradas}")
    return no_encontradas


# ── Main ──
nf_p = procesar_csv(PERSONAJES_CSV, NOMBRES_ESPECIALES_PERSONAJES, "personajes")
nf_c = procesar_csv(CRIATURAS_CSV,  NOMBRES_ESPECIALES_CRIATURAS,  "criaturas")

print("\n" + "="*60)
print("RESUMEN FINAL")
print(f"Personajes sin imagen: {len(nf_p)}")
print(f"Criaturas sin imagen:  {len(nf_c)}")
print("="*60)
