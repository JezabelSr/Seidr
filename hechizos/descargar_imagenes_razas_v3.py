"""
SEIÐR — Script de descarga de imágenes de razas v3
Para las razas que no están en Dog CEO, usa Wikipedia con nombre correcto.
Ejecutar desde la raíz: python hechizos/descargar_imagenes_razas_v3.py
"""

import pandas as pd
import requests
import time
from pathlib import Path

CSV_ENTRADA  = "universos/razas_akc_limpio.csv"
CSV_SALIDA   = "universos/razas_akc_limpio.csv"
CARPETA_IMGS = Path("iconografia/razas")
CARPETA_IMGS.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Seidr/1.0 (github.com/JezabelSr/Seidr)"}
PAUSA   = 3.0

# Nombres exactos de Wikipedia para razas problemáticas
MAPA_WIKIPEDIA = {
    "American Leopard Hound":        "American_Leopard_Hound",
    "Appenzeller Sennenhund":        "Appenzeller_Sennenhund",
    "Australian Stumpy Tail Cattle Dog": "Australian_Stumpy_Tail_Cattle_Dog",
    "Azawakh":                       "Azawakh",
    "Barbet":                        "Barbet_(dog)",
    "Bavarian Mountain Scent Hound": "Bavarian_Mountain_Hound",
    "Bedlington Terrier":            "Bedlington_Terrier",
    "Bergamasco Sheepdog":           "Bergamasco_Shepherd",
    "Berger Picard":                 "Berger_Picard",
    "Bichon Frise":                  "Bichon_Frisé",
    "Black Russian Terrier":         "Black_Russian_Terrier",
    "Bluetick Coonhound":            "Bluetick_Coonhound",
    "Bohemian Shepherd":             "Bohemian_Shepherd",
    "Bolognese":                     "Bolognese_(dog)",
    "Boykin Spaniel":                "Boykin_Spaniel",
    "Bracco Italiano":               "Bracco_Italiano",
    "Braque Francais Pyrenean":      "Braque_Français_Pyrenean",
    "Carolina Dog":                  "Carolina_dog",
    "Cesky Terrier":                 "Český_Terrier",
    "Chinese Crested":               "Chinese_Crested_Dog",
    "Chinook":                       "Chinook_(dog)",
    "Cirneco dell'Etna":             "Cirneco_dell'Etna",
    "Clumber Spaniel":               "Clumber_Spaniel",
    "Croatian Sheepdog":             "Croatian_Sheepdog",
    "Curly-Coated Retriever":        "Curly-coated_Retriever",
    "Dandie Dinmont Terrier":        "Dandie_Dinmont_Terrier",
    "Danish-Swedish Farmdog":        "Danish–Swedish_Farmdog",
    "Deutscher Wachtelhund":         "Deutscher_Wachtelhund",
    "Dogo Argentino":                "Dogo_Argentino",
    "Dogue de Bordeaux":             "Dogue_de_Bordeaux",
    "Drentsche Patrijshond":         "Drentsche_Patrijshond",
    "Drever":                        "Drever",
    "Dutch Shepherd":                "Dutch_Shepherd_Dog",
    "English Springer Spaniel":      "English_Springer_Spaniel",
    "English Toy Spaniel":           "English_Toy_Spaniel",
    "Finnish Lapphund":              "Finnish_Lapphund",
    "French Spaniel":                "French_Spaniel",
    "German Wirehaired Pointer":     "German_Wirehaired_Pointer",
    "Glen of Imaal Terrier":         "Glen_of_Imaal_Terrier",
    "Grand Basset Griffon Vendéen":  "Grand_Basset_Griffon_Vendéen",
    "Greater Swiss Mountain Dog":    "Greater_Swiss_Mountain_Dog",
    "Hamiltonstovare":               "Hamiltonstövare",
    "Hanoverian Scenthound":         "Hanoverian_Scenthound",
    "Harrier":                       "Harrier_(dog)",
    "Hokkaido":                      "Hokkaido_(dog)",
    "Icelandic Sheepdog":            "Icelandic_Sheepdog",
    "Jagdterrier":                   "Jagdterrier",
    "Japanese Chin":                 "Japanese_Chin",
    "Japanese Spitz":                "Japanese_Spitz",
    "Jindo":                         "Korean_Jindo_Dog",
    "Kai Ken":                       "Kai_Ken",
    "Karelian Bear Dog":             "Karelian_Bear_Dog",
    "Kromfohrlander":                "Kromfohrländer",
    "Lagotto Romagnolo":             "Lagotto_Romagnolo",
    "Lancashire Heeler":             "Lancashire_Heeler",
    "Löwchen":                       "Löwchen",
    "Manchester Terrier (Standard)": "Manchester_Terrier",
    "Manchester Terrier (Toy)":      "Manchester_Terrier",
    "Miniature American Shepherd":   "Miniature_American_Shepherd",
    "Miniature Bull Terrier":        "Miniature_Bull_Terrier",
    "Mountain Cur":                  "Mountain_Cur",
    "Nederlandse Kooikerhondje":     "Kooikerhondje",
    "Norfolk Terrier":               "Norfolk_Terrier",
    "Norrbottenspets":               "Norrbottenspets",
    "Norwegian Buhund":              "Norwegian_Buhund",
    "Norwegian Lundehund":           "Norwegian_Lundehund",
    "Norwich Terrier":               "Norwich_Terrier",
    "Parson Russell Terrier":        "Parson_Russell_Terrier",
    "Petit Basset Griffon Vendéen":  "Petit_Basset_Griffon_Vendéen",
    "Plott Hound":                   "Plott_Hound",
    "Polish Lowland Sheepdog":       "Polish_Lowland_Sheepdog",
    "Porcelaine":                    "Porcelaine_(dog)",
    "Portuguese Podengo":            "Portuguese_Podengo",
    "Portuguese Podengo Pequeno":    "Portuguese_Podengo",
    "Portuguese Pointer":            "Portuguese_Pointer",
    "Puli":                          "Puli_(dog)",
    "Pumi":                          "Pumi_(dog)",
    "Rafeiro do Alentejo":           "Rafeiro_do_Alentejo",
    "Rat Terrier":                   "Rat_Terrier",
    "Redbone Coonhound":             "Redbone_Coonhound",
    "Russell Terrier":               "Jack_Russell_Terrier",
    "Russian Toy":                   "Russian_Toy",
    "Russian Tsvetnaya Bolonka":     "Russian_Tsvetnaya_Bolonka",
    "Scottish Deerhound":            "Scottish_Deerhound",
    "Segugio Italiano":              "Segugio_Italiano",
    "Shikoku":                       "Shikoku_(dog)",
    "Skye Terrier":                  "Skye_Terrier",
    "Sloughi":                       "Sloughi",
    "Slovakian Wirehaired Pointer":  "Slovakian_Wirehaired_Pointer",
    "Slovensky Kopov":               "Slovenský_Kopov",
    "Small Munsterlander Pointer":   "Small_Münsterländer",
    "Smooth Fox Terrier":            "Smooth_Fox_Terrier",
    "Spanish Mastiff":               "Spanish_Mastiff",
    "Spanish Water Dog":             "Spanish_Water_Dog",
    "Spinone Italiano":              "Spinone_Italiano",
    "Stabyhoun":                     "Stabyhoun",
    "Standard Schnauzer":            "Schnauzer",
    "Sussex Spaniel":                "Sussex_Spaniel",
    "Swedish Lapphund":              "Swedish_Lapphund",
    "Swedish Vallhund":              "Swedish_Vallhund",
    "Taiwan Dog":                    "Taiwan_Dog",
    "Teddy Roosevelt Terrier":       "Teddy_Roosevelt_Terrier",
    "Tosa":                          "Tosa_(dog)",
    "Toy Fox Terrier":               "Toy_Fox_Terrier",
    "Transylvanian Hound":           "Transylvanian_Hound",
    "Treeing Tennessee Brindle":     "Treeing_Tennessee_Brindle",
    "Wetterhoun":                    "Wetterhoun",
    "Wirehaired Pointing Griffon":   "Wirehaired_Pointing_Griffon",
    "Working Kelpie":                "Australian_Kelpie",
}

NO_ENCONTRADAS = list(MAPA_WIKIPEDIA.keys())


def obtener_url_wikipedia(titulo: str) -> str | None:
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{titulo}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            img = data.get("originalimage", {}).get("source")
            if not img:
                img = data.get("thumbnail", {}).get("source")
            return img
        return None
    except:
        return None


def descargar_imagen(url: str, ruta_local: Path) -> bool:
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            ruta_local.write_bytes(r.content)
            return True
        return False
    except:
        return False


def nombre_archivo(nombre_raza: str, url: str) -> str:
    extension = Path(url.split("?")[0]).suffix or ".jpg"
    nombre = nombre_raza.lower().replace(" ", "_").replace("/", "_").replace("-", "_").replace("(", "").replace(")", "").replace("'", "")
    nombre = "".join(c for c in nombre if c.isalnum() or c == "_")
    return f"{nombre}{extension}"


# ── Main ──
print("=" * 60)
print("SEIÐR — Descarga v3 (Wikipedia — razas especiales)")
print("=" * 60)

df = pd.read_csv(CSV_ENTRADA)
df["url_imagen"] = df["url_imagen"].astype(str).fillna("").replace("nan", "")
df["caracter"]   = df["caracter"].astype(str).fillna("").replace("nan", "")

total = len(NO_ENCONTRADAS)
descargadas = 0
fallidas = []

for idx, raza in enumerate(NO_ENCONTRADAS):
    fila = df[df["breed"] == raza]
    if fila.empty:
        print(f"[{idx+1}/{total}] ⚠️  No está en CSV: {raza}")
        continue

    i = fila.index[0]

    if df.at[i, "url_imagen"].startswith("iconografia/"):
        print(f"[{idx+1}/{total}] ⏭️  Ya descargada: {raza}")
        continue

    titulo_wiki = MAPA_WIKIPEDIA[raza]
    print(f"[{idx+1}/{total}] 🔍 {raza} → {titulo_wiki}")

    url_img = obtener_url_wikipedia(titulo_wiki)

    if url_img:
        archivo = nombre_archivo(raza, url_img)
        ruta_local = CARPETA_IMGS / archivo
        if descargar_imagen(url_img, ruta_local):
            df.at[i, "url_imagen"] = f"iconografia/razas/{archivo}"
            descargadas += 1
            print(f"         ✅ {archivo}")
        else:
            fallidas.append(raza)
    else:
        print(f"  ⚠️  Sin imagen: {raza}")
        fallidas.append(raza)

    time.sleep(PAUSA)

df.to_csv(CSV_SALIDA, index=False)

print("\n" + "=" * 60)
print(f"✅ Descargadas: {descargadas}/{total}")
print(f"⚠️  Fallidas ({len(fallidas)}): {fallidas}")
print(f"📄 CSV actualizado: {CSV_SALIDA}")
print("=" * 60)
