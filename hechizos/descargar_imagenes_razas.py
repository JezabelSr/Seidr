"""
SEIÐR — Script de descarga de imágenes de razas v2
Usa Dog CEO API (https://dog.ceo/api) — sin límite de peticiones
Ejecutar desde la raíz del proyecto: python hechizos/descargar_imagenes_razas.py
"""

import pandas as pd
import requests
import time
from pathlib import Path

# ── Configuración ──
CSV_ENTRADA  = "universos/razas_akc_limpio.csv"
CSV_SALIDA   = "universos/razas_akc_limpio.csv"
CARPETA_IMGS = Path("iconografia/razas")
CARPETA_IMGS.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Seidr/1.0"}
PAUSA   = 0.3  # Dog CEO no tiene límite estricto, 0.3s es suficiente

# ── Mapa de nombres AKC → Dog CEO ──
# Dog CEO usa nombres en minúsculas sin espacios o con guión
# Algunos necesitan mapeo manual
MAPA_RAZAS = {
    "Afghan Hound":                    "hound/afghan",
    "Akita":                           "akita",
    "Alaskan Malamute":                "malamute",
    "American English Coonhound":      "hound/english",
    "American Eskimo Dog":             "eskimo",
    "American Foxhound":               "hound/blood",
    "American Hairless Terrier":       "terrier/american",
    "American Staffordshire Terrier":  "terrier/staffordshire",
    "American Water Spaniel":          "spaniel/cocker",
    "Australian Shepherd":             "australian/shepherd",
    "Australian Cattle Dog":           "cattledog/australian",
    "Australian Terrier":              "terrier/australian",
    "Basenji":                         "basenji",
    "Basset Hound":                    "hound/basset",
    "Beagle":                          "beagle",
    "Bearded Collie":                  "collie/border",
    "Bernese Mountain Dog":            "mountain/bernese",
    "Bichon Frise":                    "bichon",
    "Bloodhound":                      "hound/blood",
    "Border Collie":                   "collie/border",
    "Border Terrier":                  "terrier/border",
    "Boston Terrier":                  "terrier/boston",
    "Boxer":                           "boxer",
    "Brittany":                        "spaniel/brittany",
    "Bull Terrier":                    "terrier/bull",
    "Bullmastiff":                     "mastiff/bull",
    "Cairn Terrier":                   "terrier/cairn",
    "Cardigan Welsh Corgi":            "corgi/cardigan",
    "Chesapeake Bay Retriever":        "retriever/chesapeake",
    "Chihuahua":                       "chihuahua",
    "Chinese Crested":                 "chinese/crested",
    "Chow Chow":                       "chow",
    "Cocker Spaniel":                  "spaniel/cocker",
    "Collie":                          "collie/border",
    "Dachshund":                       "dachshund",
    "Dalmatian":                       "dalmatian",
    "Doberman Pinscher":               "doberman",
    "Dutch Shepherd":                  "shepherd/dutch",
    "English Cocker Spaniel":          "spaniel/cocker",
    "English Setter":                  "setter/english",
    "English Springer Spaniel":        "spaniel/springer",
    "French Bulldog":                  "bulldog/french",
    "German Shepherd Dog":             "germanshepherd",
    "German Shorthaired Pointer":      "pointer/germanlonghair",
    "Giant Schnauzer":                 "schnauzer/giant",
    "Golden Retriever":                "retriever/golden",
    "Great Dane":                      "dane/great",
    "Great Pyrenees":                  "pyrenees",
    "Greyhound":                       "greyhound/italian",
    "Havanese":                        "havanese",
    "Irish Setter":                    "setter/irish",
    "Irish Terrier":                   "terrier/irish",
    "Irish Water Spaniel":             "spaniel/irish",
    "Irish Wolfhound":                 "wolfhound/irish",
    "Italian Greyhound":               "greyhound/italian",
    "Japanese Chin":                   "japanese",
    "Keeshond":                        "keeshond",
    "Kerry Blue Terrier":              "terrier/kerryblue",
    "Komondor":                        "komondor",
    "Labrador Retriever":              "retriever/labrador",
    "Lhasa Apso":                      "lhasa",
    "Maltese":                         "maltese",
    "Mastiff":                         "mastiff/english",
    "Miniature Pinscher":              "pinscher/miniature",
    "Miniature Schnauzer":             "schnauzer/miniature",
    "Newfoundland":                    "newfoundland",
    "Norwegian Elkhound":              "elkhound/norwegian",
    "Old English Sheepdog":            "sheepdog/english",
    "Papillon":                        "papillon",
    "Pembroke Welsh Corgi":            "corgi/cardigan",
    "Pointer":                         "pointer",
    "Pomeranian":                      "pomeranian",
    "Poodle (Miniature)":              "poodle/miniature",
    "Poodle (Standard)":               "poodle/standard",
    "Poodle (Toy)":                    "poodle/toy",
    "Pug":                             "pug",
    "Puli":                            "puli",
    "Rhodesian Ridgeback":             "ridgeback/rhodesian",
    "Rottweiler":                      "rottweiler",
    "Saint Bernard":                   "stbernard",
    "Saluki":                          "saluki",
    "Samoyed":                         "samoyed",
    "Schipperke":                      "schipperke",
    "Scottish Terrier":                "terrier/scottish",
    "Sealyham Terrier":                "terrier/sealyham",
    "Siberian Husky":                  "husky",
    "Silky Terrier":                   "terrier/silky",
    "Skye Terrier":                    "terrier/skye",
    "Springer Spaniel":                "spaniel/springer",
    "Standard Schnauzer":              "schnauzer/standard",
    "Tibetan Mastiff":                 "mastiff/tibetan",
    "Tibetan Terrier":                 "terrier/tibetan",
    "Vizsla":                          "vizsla",
    "Weimaraner":                      "weimaraner",
    "Welsh Springer Spaniel":          "spaniel/welsh",
    "Welsh Terrier":                   "terrier/welsh",
    "West Highland White Terrier":     "terrier/westhighland",
    "Whippet":                         "whippet",
    "Wire Fox Terrier":                "terrier/fox",
    "Wirehaired Pointing Griffon":     "griffon/wirehaired",
    "Yorkshire Terrier":               "yorkshire",
}


def obtener_url_imagen(nombre_raza: str) -> str | None:
    """Obtiene URL de imagen desde Dog CEO API."""
    clave = MAPA_RAZAS.get(nombre_raza)
    if not clave:
        # Intentar conversión automática: "Golden Retriever" -> "goldenretriever"
        clave = nombre_raza.lower().replace(" ", "").replace("-", "")

    url = f"https://dog.ceo/api/breed/{clave}/images/random"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "success":
                return data["message"]
        print(f"  ⚠️  No encontrada en Dog CEO: {nombre_raza} (clave: {clave})")
        return None
    except Exception as e:
        print(f"  ❌  Error para {nombre_raza}: {e}")
        return None


def descargar_imagen(url: str, ruta_local: Path) -> bool:
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            ruta_local.write_bytes(r.content)
            return True
        return False
    except Exception as e:
        print(f"  ❌  Error descargando: {e}")
        return False


def nombre_archivo(nombre_raza: str, url: str) -> str:
    extension = Path(url.split("?")[0]).suffix or ".jpg"
    nombre = nombre_raza.lower().replace(" ", "_").replace("/", "_").replace("-", "_").replace("(", "").replace(")", "")
    nombre = "".join(c for c in nombre if c.isalnum() or c == "_")
    return f"{nombre}{extension}"


# ── Main ──
print("=" * 60)
print("SEIÐR — Descarga de imágenes de razas v2 (Dog CEO API)")
print("=" * 60)

df = pd.read_csv(CSV_ENTRADA)
df["url_imagen"] = df["url_imagen"].astype(str).fillna("").replace("nan", "")
df["caracter"]   = df["caracter"].astype(str).fillna("").replace("nan", "")

total = len(df)
descargadas = 0
no_encontradas = []

for i, row in df.iterrows():
    raza = row["breed"]

    if row["url_imagen"].startswith("iconografia/"):
        print(f"[{i+1}/{total}] ⏭️  Ya descargada: {raza}")
        continue

    print(f"[{i+1}/{total}] 🔍 Buscando: {raza}")

    url_img = obtener_url_imagen(raza)

    if url_img:
        archivo = nombre_archivo(raza, url_img)
        ruta_local = CARPETA_IMGS / archivo
        if descargar_imagen(url_img, ruta_local):
            df.at[i, "url_imagen"] = f"iconografia/razas/{archivo}"
            descargadas += 1
            print(f"         ✅ {archivo}")
        else:
            no_encontradas.append(raza)
    else:
        no_encontradas.append(raza)

    time.sleep(PAUSA)

df.to_csv(CSV_SALIDA, index=False)

print("\n" + "=" * 60)
print(f"✅ Descargadas: {descargadas}/{total}")
print(f"⚠️  No encontradas ({len(no_encontradas)}): {no_encontradas}")
print(f"📄 CSV actualizado: {CSV_SALIDA}")
print("=" * 60)
