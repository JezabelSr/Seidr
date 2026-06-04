# SEIÐR — Documento de contexto v4
*Actualizado: 03/06/2026*

---

## Identidad
- **Nombre:** Seiðr · *Cuando tu saga se convierte en brújula*
- **Repo:** https://github.com/JezabelSr/Seidr
- **Deploy:** https://seidr-app.streamlit.app
- **Ruta local:** C:\Users\jezab\OneDrive\Escritorio\Adalab\Proyectos\Seidr\
- **Stack:** Python · pandas · SQLite · Streamlit · Plotly · fpdf2 · scipy · numpy
- **Licencias:** Código AGPL v3 · Datos CC BY-NC-ND 4.0

---

## Arquitectura de archivos

```
app.py                          ← raíz, punto de entrada
seidr.db                        ← SQLite generada automáticamente desde CSVs
requirements.txt                ← incluye fpdf2
hechizos/
├── crear_bd.py                 ← migración CSV→SQLite (python hechizos/crear_bd.py --forzar)
├── db.py                       ← capa de acceso a datos con @st.cache_data TTL=3600
├── orientacion_nd.py           ← algoritmo orientación ND
├── narrador.py                 ← 24 textos narrativos (6 universos × 4 momentos)
├── codigo_seidr.py             ← codificación/decodificación código SEIDR-U-PID-NDs-DIMS
├── razas_helper.py             ← búsqueda razas por nombre español
├── generador_pdf.py            ← genera PDFs saga + módulos 3-7 (fpdf2, sin imagen raza)
├── modulo_regreso.py           ← módulo "Ya estuve aquí" con código Seiðr
├── test_universo.py            ← test de universo con orden aleatorio estable por sesión
├── modulo_1.py                 ← Tu perfil (24 preguntas, orden y opciones aleatorias)
├── modulo_2.py                 ← Tu criatura + descarga PDF saga
├── modulo_3.py  (base)         ← Comunicación + funciones compartidas por 4-7
├── modulo_4.py                 ← Aprendizaje
├── modulo_5.py                 ← Sociabilidad
├── modulo_6.py                 ← Tu cuerpo
├── modulo_7.py                 ← Orientación clínica
└── modo_profesional.py         ← acceso directo por ND y por universo
universos/
├── universos.csv · personajes.csv · criaturas.csv · preguntas.csv
├── perfiles_nd_clinicos.csv · razas_akc_limpio.csv
├── contenido_modulos.csv       ← 56 filas (14 ND × 4 módulos)
└── recursos_reales/recursos.csv · organizaciones_espana.csv
iconografia/
├── fondos/                     ← 6 fondos .webp por universo
├── musica/                     ← 6 MP3 por universo
├── razas/                      ← 277 imágenes .jpg de razas AKC
├── portada_seidr.png · textura_piedra.png · favicon_seidr.png
```

---

## Datos

- 171 personajes · 194 criaturas · 166 preguntas · 277 razas AKC
- 14 NDs activas · 50 recursos · 38 organizaciones España
- 6 universos v1.0: Harry Potter, Brújula Dorada, Pokémon, Ghibli, HTTYD, Disney/Pixar

---

## Módulos del sidebar (MODULOS dict en app.py)

```
ᚱ  Inicio           → inicio
ᚦ  Test de universo → test_universo
ᚨ  Tu perfil        → modulo_1
ᚢ  Tu criatura      → modulo_2
ᚲ  Comunicación     → modulo_3
ᚷ  Aprendizaje      → modulo_4
ᛉ  Sociabilidad     → modulo_5
ᛊ  Tu cuerpo        → modulo_6
ᛏ  Orientación clínica → modulo_7
⚕  Modo profesional → profesional
ᚺ  Ya estuve aquí   → regreso
```

---

## Funcionalidades implementadas (estado actual)

### Core
- ✅ Test de universo (7 preguntas en 2 bloques, elección directa)
- ✅ Test de perfil (24 preguntas, 8 dimensiones, 0-5)
- ✅ Asignación de personaje por distancia euclidiana
- ✅ Asignación de criatura por perfil compensatorio
- ✅ Módulos 3-7 con contenido personalizado por ND (contenido_modulos.csv)
- ✅ Algoritmo orientación ND con dimensiones clave obligatorias

### UX/UI
- ✅ Fondos dinámicos por universo (webp)
- ✅ Música ambiental por universo (MP3, autoplay loop vol 30%)
- ✅ Narrador contextual: 4 momentos × 6 universos = 24 textos
- ✅ Raíz nórdica SVG como barra de progreso (viewBox 660×90)
- ✅ Módulos bloqueados con estética de piedra sellada
- ✅ Orden aleatorio de preguntas y opciones (estable por sesión, semilla de tiempo)
- ✅ Botón RESET en sidebar (limpia session_state + órdenes aleatorios)
- ✅ Scroll al top al cambiar de página (múltiples selectores CSS)
- ✅ Favicon rúnico (iconografia/favicon_seidr.png)

### Descargables
- ✅ PDF saga completa (universo + personaje + 8 dimensiones + ND + criatura + código)
- ✅ PDF por módulo 3-7 (explicación + técnicas + adaptaciones + recursos)
- ✅ Sistema de código Seiðr (SEIDR-U-PID-NDs-DIMS) impreso en PDF

### Módulo regreso (ᚺ Ya estuve aquí)
- ✅ Input de código → decodifica → carga perfil completo en session_state
- ✅ Muestra universo, personaje, criatura, orientación ND
- ✅ Botón "Ir a mis recursos" → módulo 3

### Base de datos
- ✅ SQLite generada automáticamente desde CSVs al arrancar
- ✅ db.py con @st.cache_data TTL=1h y fallback a CSV
- ✅ Índices en columnas frecuentes (universo_id, nd, modulo)

---

## Sistema de código Seiðr

**Formato:** `SEIDR-[U]-[PID]-[NDs]-[DIMS]`
**Ejemplo:** `SEIDR-3-074-AAC.SPD-50554433`

- U = universo_id (1-6)
- PID = personaje_id 3 dígitos
- NDs = abreviaturas separadas por punto (NT si neurotípico)
  - DIS=Dislexia, TDA=TDAH, TEA=TEA, AAC=AACC, DCA=Discalculia
  - DPX=Dispraxia/TDC, TOU=Tourette, SPD=SPD, TAR=Tartamudez
  - DIN=Discapacidad Intelectual, TOC=TOC, MUT=Mutismo Selectivo
  - TAS=Trastorno Ansiedad Social, TNV=TANV
- DIMS = 8 dígitos 0-5 (hiperfoco, reg_emocional, sensorialidad, comunicacion, aprendizaje, sociabilidad, propiocepcion, funcion_ejecutiva)

---

## Narrador contextual (narrador.py)

4 momentos por universo:
- `universo_elegido` — al elegir universo
- `perfil_completado` — al terminar el test de dimensiones
- `criatura_asignada` — al ver la criatura
- `modulo_recursos` — al entrar a módulos 3-7

Textos revisados pendientes (Jezabel tiene PDF de revisión `seidr_narrador_revision.pdf`)

---

## Navegación (app.py)

- `_pagina_activa` en session_state como fuente de verdad
- Radio del sidebar usa `index=opciones.index(st.session_state["_pagina_activa"])`
- `_navegar_a(pagina_key)` para botones internos
- `_navegar_desde_boton` flag para distinguir navegación por botón vs radio

---

## Portada

- Banner 220px + texto Seiðr (pronunciación + descripción + frase final)
- Un solo botón "ᚦ Comienza tu aventura" → test universo
- CSS padding reducido para que el botón sea visible sin scroll

---

## PDFs (fpdf2, generador_pdf.py)

- `generar_pdf_saga()`: universo + personaje + 8 dimensiones con descripción + ND con desc clínica + criatura (descripción narrativa + equivalente real) + código Seiðr
- `generar_pdf_modulo()`: explicación + técnicas + adaptaciones + recursos por módulo
- Fondo oscuro automático en TODAS las páginas (via `SeidrPDF.header()`)
- `_limpiar()` convierte todos los caracteres Unicode→latin-1
- Sin imagen de raza (causaba error "Not enough horizontal space")
- `multi_cell(130, ...)` con ancho fijo (no 0)

---

## Deploy Streamlit Cloud

- URL: seidr-app.streamlit.app
- Favicon: iconografia/favicon_seidr.png
- requirements.txt incluye fpdf2
- CSS: `.stMainBlockContainer { padding-top: 1rem !important; }`

---

## Comandos útiles

```bash
# Activar entorno
source venv/Scripts/activate

# Correr en local
streamlit run app.py

# Regenerar SQLite
python hechizos/crear_bd.py --forzar

# Test PDF
python -c "from hechizos.generador_pdf import generar_pdf_saga; pdf = generar_pdf_saga('Pokemon','Cilan',{},{'hiperfoco':5,'regulacion_emocional':0,'sensorialidad':5,'comunicacion':5,'aprendizaje':4,'sociabilidad':4,'propiocepcion':3,'funcion_ejecutiva':3},['AACC'],'Wartortle','Whippet','Calmado y afectuoso.',universo_id=3,personaje_id=74); print('OK',len(pdf))"
```

---

## Pendiente antes de presentación (17 días)

- [ ] Revisar brillo en otros PCs (overlay adaptativo pendiente de decisión)
- [ ] Revisar todos los universos de punta a punta
- [ ] Ampliar recursos por ND (Jezabel pasará textos)
- [ ] Revisar y mejorar textos del narrador (PDF de revisión generado)
- [ ] Subir imágenes que faltan de personajes/criaturas

## Post-bootcamp

- Login de usuarios
- 12 universos adicionales
- Módulos de vida real (educación, trabajo, familia)
- Versión móvil optimizada
- PDF modo profesional por ND y por universo
