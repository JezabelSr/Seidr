"""
SEIÐR — Descarga de razas pendientes v2
Ejecutar desde la raíz: python hechizos/descargar_pendientes.py
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
PAUSA   = 10.0

MAPA_WIKIPEDIA = {
    "French Spaniel":                   "French_Spaniel",
    "German Wirehaired Pointer":        "German_Wirehaired_Pointer",
    "Glen of Imaal Terrier":            "Glen_of_Imaal_Terrier",
    "Grand Basset Griffon Vendéen":     "Grand_Basset_Griffon_Vend%C3%A9en",
    "Hamiltonstovare":                  "Hamiltonst%C3%B6vare",
    "Hanoverian Scenthound":            "Hanoverian_Scenthound",
    "Harrier":                          "Harrier_dog",
    "Icelandic Sheepdog":               "Icelandic_Sheepdog",
    "Jagdterrier":                      "Jagdterrier",
    "Japanese Chin":                    "Japanese_Chin",
    "Japanese Spitz":                   "Japanese_Spitz",
    "Jindo":                            "Korean_Jindo_Dog",
    "Kai Ken":                          "Kai_Ken",
    "Kromfohrlander":                   "Kromfohrland%C3%A4r",
    "Lagotto Romagnolo":                "Lagotto_Romagnolo",
    "Lancashire Heeler":                "Lancashire_Heeler",
    "Löwchen":                          "L%C3%B6wchen",
    "Miniature American Shepherd":      "Miniature_American_Shepherd",
    "Miniature Bull Terrier":           "Miniature_Bull_Terrier",
    "Mountain Cur":                     "Mountain_Cur",
    "Nederlandse Kooikerhondje":        "Kooikerhondje",
    "Norrbottenspets":                  "Norrbottenspets",
    "Norwegian Buhund":                 "Norwegian_Buhund",
    "Parson Russell Terrier":           "Parson_Russell_Terrier",
    "Petit Basset Griffon Vendéen":     "Petit_Basset_Griffon_Vend%C3%A9en",
    "Plott Hound":                      "Plott_Hound",
    "Polish Lowland Sheepdog":          "Polish_Lowland_Sheepdog",
    "Porcelaine":                       "Porcelaine_dog",
    "Portuguese Podengo":               "Portuguese_Podengo",
    "Portuguese Podengo Pequeno":       "Portuguese_Podengo",
    "Portuguese Pointer":               "Portuguese_Pointer",
    "Puli":                             "Puli_dog",
    "Rat Terrier":                      "Rat_Terrier",
    "Redbone Coonhound":                "Redbone_Coonhound",
    "Russell Terrier":                  "Jack_Russell_Terrier",
    "Russian Toy":                      "Russian_Toy",
    "Russian Tsvetnaya Bolonka":        "Russian_Tsvetnaya_Bolonka",
    "Scottish Deerhound":               "Scottish_Deerhound",
    "Segugio Italiano":                 "Segugio_Italiano",
    "Skye Terrier":                     "Skye_Terrier",
    "Slovakian Wirehaired Pointer":     "Slovakian_Wirehaired_Pointer",
    "Slovensky Kopov":                  "Slovensk%C3%BD_kopov",
    "Small Munsterlander Pointer":      "Small_M%C3%BCnsterl%C3%A4nder",
    "Spanish Mastiff":                  "Spanish_Mastiff",
    "Spanish Water Dog":                "Spanish_Water_Dog",
    "Spinone Italiano":                 "Spinone_Italiano",
    "Stabyhoun":                        "Stabyhoun",
    "Sussex Spaniel":                   "Sussex_Spaniel",
    "Swedish Lapphund":                 "Swedish_Lapphund",
    "Swedish Vallhund":                 "Swedish_Vallhund",
    "Taiwan Dog":                       "Taiwan_Dog",
    "Teddy Roosevelt Terrier":          "Teddy_Roosevelt_Terrier",
    "Toy Fox Terrier":                  "Toy_Fox_Terrier",
    "Transylvanian Hound":              "Transylvanian_Hound",
    "Treeing Tennessee Brindle":        "Treeing_Tennessee_Brindle",
    "Wetterhoun":                       "Wetterhoun",
    "Wirehaired Pointing Griffon":      "Wirehaired_Pointing_Griffon",
    "Working Kelpie":                   "Australian_Kelpie",
}


def obtener_url_wikipedia(titulo: str) -> str | None:
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{titulo}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data.get("originalimage", {}).get("source") or data.get("thumbnail", {}).get("source")
        print(f"  ❌  HTTP {r.status_code}")
        return None
    except Exception as e:
        print(f"  ❌  Error: {e}")
        return None


def descargar_imagen(url: str, ruta: Path) -> bool:
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            ruta.write_bytes(r.content)
            return True
        return False
    except:
        return False


def nombre_archivo(raza: str, url: str) -> str:
    ext = Path(url.split("?")[0]).suffix or ".jpg"
    nombre = raza.lower().replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "").replace("'", "").replace("/", "_")
    nombre = "".join(c for c in nombre if c.isalnum() or c == "_")
    return f"{nombre}{ext}"


# ── Main ──
total = len(MAPA_WIKIPEDIA)
print("=" * 60)
print(f"SEIÐR — Descarga pendientes ({total} razas, 10s pausa)")
print(f"Tiempo estimado: ~{total * 10 // 60} minutos")
print("=" * 60)

df = pd.read_csv(CSV_ENTRADA)
df["url_imagen"] = df["url_imagen"].astype(str).fillna("").replace("nan", "")

descargadas = 0
fallidas = []

for idx, (raza, titulo) in enumerate(MAPA_WIKIPEDIA.items()):
    fila = df[df["breed"] == raza]
    if fila.empty:
        print(f"[{idx+1}/{total}] ⚠️  No en CSV: {raza}")
        continue

    i = fila.index[0]

    if df.at[i, "url_imagen"].startswith("iconografia/"):
        print(f"[{idx+1}/{total}] ⏭️  Ya descargada: {raza}")
        continue

    print(f"[{idx+1}/{total}] 🔍 {raza}", end=" ... ", flush=True)

    url_img = obtener_url_wikipedia(titulo)
    if url_img:
        archivo = nombre_archivo(raza, url_img)
        if descargar_imagen(url_img, CARPETA_IMGS / archivo):
            df.at[i, "url_imagen"] = f"iconografia/razas/{archivo}"
            descargadas += 1
            print(f"✅ {archivo}")
        else:
            print("❌ fallo descarga")
            fallidas.append(raza)
    else:
        print("⚠️  sin imagen")
        fallidas.append(raza)

    time.sleep(PAUSA)

df.to_csv(CSV_SALIDA, index=False)
print("\n" + "=" * 60)
print(f"✅ Descargadas: {descargadas}/{total}")
print(f"⚠️  Fallidas ({len(fallidas)}): {fallidas}")
print("=" * 60)
