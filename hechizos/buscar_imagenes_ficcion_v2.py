"""
SEIÐR — Script de búsqueda de URLs de imágenes v2
Solo busca los que NO tienen imagen todavía.
Ejecutar desde la raíz: python hechizos/buscar_imagenes_ficcion_v2.py
"""

import pandas as pd
import requests
import time

PERSONAJES_CSV = "universos/personajes.csv"
CRIATURAS_CSV  = "universos/criaturas.csv"
HEADERS = {"User-Agent": "Seidr/1.0 (github.com/JezabelSr/Seidr)"}
PAUSA = 1.0

WIKIS = {
    1: "harrypotter.fandom.com",
    2: "darkmaterials.fandom.com",
    3: "pokemon.fandom.com",
    4: "ghibli.fandom.com",
    5: "howtotrainyourdragon.fandom.com",
    6: "disney.fandom.com",
}

# Personajes y criaturas ya descargados manualmente — se saltarán
YA_DESCARGADOS_PERSONAJES = {
    "Alicia", "Ansiedad", "Astrid", "Bella", "Bestia", "Bocón", "Brusca",
    "Cenicienta", "Chusco", "Conejo Blanco", "Drago Puño Sangriento", "El Baron",
    "Elio", "Eret", "Estoico el inmenso", "Gary", "Ginny Weasley", "Giulia",
    "Hércules", "Hipo", "Kida", "Kronk", "Lilo", "Mirabel", "Mocoso", "Mudito",
    "Numero 22", "Patapez", "Pinocho", "Príncipe Eric", "Ron Weasley",
    "Sombrerero Loco", "Tristeza", "Valka", "Vanellope", "Candela Lumen",
    # Todos los de La Brújula Dorada
    "Lyra Belacqua", "Will Parry", "Mrs. Coulter", "Lord Asriel", "Iorek Byrnison",
    "Farder Coram", "Lee Scoresby", "Serafina Pekkala", "Roger Parslow",
    "Mary Malone", "Lord Faa", "Ruta Skadi", "Xaphania", "Metatrón", "El padre Gomez",
}

NOMBRES_ESPECIALES_PERSONAJES = {
    # Harry Potter
    "Charlie Weasley":          "Charlie_Weasley",
    "Bill Weasley":             "Bill_Weasley",
    "Voldemort":                "Lord_Voldemort",
    "James Potter":             "James_Potter",
    "Lily Potter":              "Lily_Potter",
    # Pokémon
    "Profesor Oak":             "Professor_Oak",
    "Serena":                   "Serena_(anime)",
    "Tracey":                   "Tracey_Sketchit",
    "Enfermera Joy":            "Nurse_Joy",
    "Oficial Jenny":            "Officer_Jenny",
    "Profesor Kukui":           "Professor_Kukui",
    # Ghibli
    "Chihiro":                  "Chihiro_Ogino",
    "Lord Yupa":                "Lord_Yupa",
    "Sophie":                   "Sophie_Hatter",
    "Howl":                     "Howl_(character)",
    "Satsuki":                  "Satsuki_Kusakabe",
    "Mei":                      "Mei_Kusakabe",
    # HTTYD
    "Bocón":                    "Fishlegs_Ingerman",
    # Disney/Pixar
    "Nilo Fuentes":             "Wade_Ripple",
}

NOMBRES_ESPECIALES_CRIATURAS = {
    # Harry Potter
    "Norbert/Norberta":                 "Norbert_(dragon)",
    "La señora Norris":                 "Mrs._Norris",
    "El basilisco":                     "Basilisk_(Harry_Potter)",
    "La esfinge":                       "Sphinx_(Triwizard_Tournament)",
    "Unicornio":                        "Unicorn_(Harry_Potter)",
    # Brújula Dorada
    "Pan":                              "Pantalaimon",
    "Kirjava":                          "Kirjava",
    "Stelmaria":                        "Stelmaria",
    "El mono dorado":                   "Marisa_Coulter%27s_dæmon",
    "El gato atigrado":                 "Farder_Coram%27s_dæmon",
    "La liebre":                        "Lee_Scoresby%27s_dæmon",
    "El ganso":                         "Serafina_Pekkala%27s_dæmon",
    "Panserbjørne":                     "Armoured_bear",
    "Las brujas de Serafina":           "Witch_(His_Dark_Materials)",
    "Los gallivespians":                "Gallivespian",
    "Los mulefa":                       "Mulefa",
    "Balthamos y Baruch":               "Balthamos",
    # Ghibli
    "Ponyo forma pez":                  "Ponyo_(character)",
    "Teto":                             "Teto_(Nausicaä)",
    "Los Kodama":                       "Kodama_(Princess_Mononoke)",
    "Espantapájaros Cabeza de Nabo":    "Turnip-Head",
    "Susuwataris":                      "Soot_Sprite",
    "Bebé ratón":                       "Boh",
    "Lobos de Moro":                    "Moro%27s_sons",
    # HTTYD
    "Desdentado":                       "Toothless_(How_to_Train_Your_Dragon)",
    "Tormenta":                         "Stormfly",
    "Barrilete":                        "Meatlug",
    "Vómito y Eructo":                  "Barf_and_Belch",
    "Colmillo":                         "Hookfang",
    # Disney/Pixar
    "Yago":                             "Iago_(Aladdin)",
    "Gato de Cheshire":                 "Cheshire_Cat",
    "Arquímedes":                       "Archimedes_(The_Sword_in_the_Stone)",
    "Rey Louie":                        "King_Louie",
    "Winnie Pooh":                      "Winnie_the_Pooh_(character)",
    "Ígor":                             "Eeyore",
    "Sebastián":                        "Sebastian_(The_Little_Mermaid)",
    "Genio":                            "Genie_(Aladdin)",
    "Hugo Víctor y Laverne":            "Hugo,_Victor,_and_Laverne",
    "Pegaso":                           "Pegasus_(Hercules)",
    "Filoctetes":                       "Philoctetes_(Hercules)",
    "Hermanito":                        "Little_Brother_(Mulan)",
    "Sulley":                           "James_P._Sullivan",
    "Bing Bong":                        "Bing_Bong_(Inside_Out)",
    "El Nokk":                          "The_Nokk",
    "Machiavelli":                      "Machiavelli_(Luca)",
    "Estrella":                         "Star_(Wish)",
    "Pena":                             "Pain_(Hercules)",
    "Pánico":                           "Panic_(Hercules)",
    "Pua":                              "Pua_(Moana)",
}


def buscar_imagen_fandom(nombre, wiki, nombres_especiales):
    titulo = nombres_especiales.get(nombre, nombre.replace(" ", "_"))
    api_url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "titles": titulo.replace("_", " ").replace("%27", "'"),
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


def procesar_csv(csv_path, nombres_especiales, ya_descargados, tipo):
    df = pd.read_csv(csv_path)
    df["url_imagen"] = df["url_imagen"].astype(str).fillna("").replace("nan", "")

    # Solo los que no tienen imagen Y no están ya descargados manualmente
    pendientes = df[
        (df["url_imagen"].str.strip() == "") &
        (~df["nombre"].isin(ya_descargados))
    ]
    total = len(pendientes)
    encontradas = 0
    no_encontradas = []

    print(f"\n{'='*60}")
    print(f"SEIÐR — {tipo}: {total} pendientes")
    print(f"{'='*60}")

    for i, row in pendientes.iterrows():
        nombre = str(row["nombre"])
        uid = int(row["universo_id"])
        wiki = WIKIS.get(uid)

        print(f"🔍 {nombre}", end=" ... ", flush=True)
        url = buscar_imagen_fandom(nombre, wiki, nombres_especiales)

        if url:
            df.at[i, "url_imagen"] = url
            encontradas += 1
            print("✅")
        else:
            no_encontradas.append(nombre)
            print("❌")

        time.sleep(PAUSA)

    df.to_csv(csv_path, index=False)
    print(f"\n✅ {encontradas}/{total} | ⚠️  Sin imagen: {no_encontradas}")
    return no_encontradas


nf_p = procesar_csv(PERSONAJES_CSV, NOMBRES_ESPECIALES_PERSONAJES, YA_DESCARGADOS_PERSONAJES, "Personajes")
nf_c = procesar_csv(CRIATURAS_CSV,  NOMBRES_ESPECIALES_CRIATURAS,  set(), "Criaturas")

print("\n" + "="*60)
print(f"Personajes sin imagen: {len(nf_p)} → {nf_p}")
print(f"Criaturas sin imagen:  {len(nf_c)} → {nf_c}")
print("="*60)
