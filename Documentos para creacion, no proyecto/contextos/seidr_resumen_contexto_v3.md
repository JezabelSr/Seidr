# SEIÐR — Documento de contexto completo v3
## Para continuar en un chat nuevo sin perder nada

---

## IDENTIDAD DEL PROYECTO

**Nombre:** Seiðr
**Subtítulo:** *Cuando tu saga se convierte en brújula*
**Concepto:** Herramienta de datos que usa universos de ficción como puerta de entrada a información clínica rigurosa sobre neurodivergencia. La ficción es el vehículo, nunca el contenido. No es herramienta de diagnóstico.
**Repositorio:** https://github.com/JezabelSr/Seidr (público)
**Ruta local:** C:\Users\jezab\OneDrive\Escritorio\Adalab\Proyectos\Seidr\

---

## STACK TÉCNICO

- Python · pandas · SQLite · Streamlit · Plotly · Selenium · BeautifulSoup · scipy · numpy
- Entorno virtual: venv — activar con `source venv/Scripts/activate`
- Kernel Jupyter: "Seidr (venv)"
- Sin login en bootcamp — arquitectura SQLite preparada para añadirlo post-bootcamp
- Deploy: Streamlit Cloud

---

## LICENCIAS

- **Código:** AGPL v3
- **Datos y contenido:** CC BY-NC-ND 4.0
- **Imágenes de personajes/criaturas:** uso educativo no comercial — atribución por universo en la app

---

## ESTRUCTURA DE CARPETAS

```
Seidr/
├── app.py                          ← punto de entrada Streamlit
├── universos/
│   ├── universos.csv
│   ├── personajes.csv              ✅ 171 personajes con descripcion + url_imagen
│   ├── criaturas.csv               ✅ 194 criaturas con descripcion + url_imagen (4 sin imagen: Kirjava, El gato atigrado, La liebre, El ganso)
│   ├── preguntas.csv               ✅ completo (IDs 1-166)
│   ├── neurodivergencias.csv
│   ├── perfiles_nd_clinicos.csv    ✅ 14 ND con rangos ajustados
│   ├── razas_akc_limpio.csv        ✅ 277 razas con url_imagen + caracter
│   └── recursos_reales/
│       ├── recursos.csv            ✅ 50 recursos módulos 3-7
│       ├── recursos_nd.csv
│       └── organizaciones_espana.csv ✅ 38 organizaciones scrapeadas
├── hechizos/
│   ├── orientacion_nd.py           ✅ algoritmo ND (14 ND, umbral=8)
│   ├── test_universo.py            ✅ módulo test universo
│   ├── modulo_1.py                 ✅ módulo perfil + orientación ND
│   └── modulo_2.py                 ✅ módulo criatura + raza real
├── iconografia/
│   ├── portada_seidr.png           ← imagen de portada (creada por Jezabel)
│   ├── textura_piedra.png          ← textura de fondo
│   ├── razas/                      ✅ 277 imágenes de razas
│   ├── personajes/                 ✅ 171 imágenes (mezcla local + URL fandom)
│   └── criaturas/                  ✅ 190/194 imágenes
├── runas/                          ← notebooks Jupyter
├── manuscritos/                    ← documentación
└── venv/
```

---

## LAS 8 DIMENSIONES (escala 0-5)

1. Hiperfoco
2. Regulación emocional
3. Sensorialidad
4. Comunicación
5. Aprendizaje
6. Sociabilidad
7. Propiocepción
8. Función ejecutiva

**NOMBRES EN EL CÓDIGO:**
- En `personajes.csv` y `modulo_1.py`: `hiperfoco`, `regulacion_emocional`, `sensorialidad`, `comunicacion`, `aprendizaje`, `sociabilidad`, `propiocepcion`, `funcion_ejecutiva`
- En `orientacion_nd.py` y `perfiles_nd_clinicos.csv`: `hiperfoco`, `reg_emocional`, `sensorialidad`, `comunicacion`, `aprendizaje`, `sociabilidad`, `propiocepcion`, `f_ejecutiva`
- ⚠️ El módulo 1 adapta los nombres al llamar a `orientar_nd()` — esto ya está implementado

---

## LAS 14 NEURODIVERGENCIAS ACTIVAS

(Se eliminaron: Disgrafía, Trastorno Fonológico, Trastorno de Comunicación Social, Síndrome de Irlen, Trastorno por Movimientos Estereotipados, TEL)

1. Dislexia · 2. TDAH · 3. TEA · 4. AACC · 5. Discalculia
6. Dispraxia/TDC · 7. Síndrome de Tourette · 8. SPD · 9. Tartamudez
10. Discapacidad Intelectual · 11. TOC · 12. Mutismo Selectivo
13. Trastorno de Ansiedad Social · 14. TANV

---

## ALGORITMO DE ORIENTACIÓN ND

**Archivo:** `hechizos/orientacion_nd.py`
**Función:** `orientar_nd(perfil_usuario, df_nd, umbral=8)`
**Umbral:** 8/8 dimensiones en rango → Perfil compatible (100%)
**Llamada desde modulo_1.py:** `orientar_nd(perfil_nd, df_nd, umbral=8)`

**IMPORTANTE:** El perfil se adapta antes de llamar al algoritmo:
```python
perfil_nd = {
    "hiperfoco":     perfil.get("hiperfoco", 0),
    "reg_emocional": perfil.get("regulacion_emocional", 0),
    "sensorialidad": perfil.get("sensorialidad", 0),
    "comunicacion":  perfil.get("comunicacion", 0),
    "aprendizaje":   perfil.get("aprendizaje", 0),
    "sociabilidad":  perfil.get("sociabilidad", 0),
    "propiocepcion": perfil.get("propiocepcion", 0),
    "f_ejecutiva":   perfil.get("funcion_ejecutiva", 0),
}
```

---

## LOS 7 MÓDULOS — ESTADO ACTUAL

| Módulo | Estado | Archivo |
|--------|--------|---------|
| Test de universo | ✅ COMPLETO | hechizos/test_universo.py |
| 1 · Tu perfil | ✅ COMPLETO | hechizos/modulo_1.py |
| 2 · Tu criatura | ✅ COMPLETO | hechizos/modulo_2.py |
| 3 · Comunicación | 🔄 EN CONSTRUCCIÓN | — |
| 4 · Aprendizaje | 🔄 EN CONSTRUCCIÓN | — |
| 5 · Sociabilidad | 🔄 EN CONSTRUCCIÓN | — |
| 6 · Tu cuerpo | 🔄 EN CONSTRUCCIÓN | — |
| 7 · Orientación clínica | 🔄 EN CONSTRUCCIÓN | — |

---

## APP.PY — ESTADO Y CARACTERÍSTICAS

- **Sidebar:** 9 opciones de navegación con runas
- **Portada:** imagen `iconografia/portada_seidr.png` en banner
- **Textura de fondo:** `iconografia/textura_piedra.png` — cover, centrada, fixed
- **CSS completo:** fuentes Cinzel + Crimson Pro, paleta dorada/oscura
- **Estado de sesión:** universo_elegido, universo_nombre, perfil_usuario, personaje_asignado, personaje_data, criatura_asignada, orientacion_nd, test_universo_done, test_dim_done
- **Imports protegidos:** try/except para cada módulo
- **Módulos 3-7:** muestran página "en construcción" con estética

---

## PRÓXIMAS TAREAS (en orden)

### Inmediatas — antes del deploy:
1. **Módulos 3-7** — mostrar recursos filtrados por perfil ND del usuario
2. **Fondos por universo** — al elegir universo, cambia el fondo de la app
3. **Barra de progreso estética** — raíz que crece o sello que se completa a lo largo de los 7 módulos
4. **Módulos bloqueados con estética** — apariencia de piedra/sellado en lugar de "en construcción"
5. **Accesibilidad visual** — overlay sobre fondos cargados, contraste cómodo

### Post-deploy — v1.1:
6. Música ambiental opcional por universo
7. Narrador contextual — voz diferente por universo
8. Conectar CSVs a SQLite
9. Deploy en Streamlit Cloud

---

## LOS 18 UNIVERSOS — LISTA DEFINITIVA CERRADA

### Lanzamiento v1.0 (6 universos) ✅ TODOS COMPLETOS:
1. Harry Potter · 2. La Brújula Dorada · 3. Pokémon
4. Studio Ghibli · 5. Cómo entrenar a tu dragón · 6. Disney/Pixar

### Siguientes fases (12 universos):
7. Digimon · 8. One Piece · 9. La Tierra Media · 10. Universo Rick Riordan
11. Avatar Aang/Korra · 12. Juego de Tronos · 13. Las Crónicas de Narnia
14. Naruto · 15. Dragon Age · 16. The Legend of Zelda
17. Dragon Quest · 18. Avatar James Cameron

---

## NUMERACIÓN ACTUAL DE IDs

- **Personajes:** último ID = 172
- **Criaturas:** último ID = 194
- **Preguntas:** último ID = 166
- **Recursos:** último ID = 50

---

## ESQUEMA DE TABLAS CSV PRINCIPALES

### universos/personajes.csv
personaje_id, universo_id, nombre, rol,
hiperfoco, regulacion_emocional, sensorialidad, comunicacion,
aprendizaje, sociabilidad, propiocepcion, funcion_ejecutiva,
estilo_comunicacion, estilo_aprendizaje, estilo_socializacion,
perfil_sensorial, justificacion, descripcion, url_imagen

### universos/criaturas.csv
criatura_id, universo_id, nombre,
calma, vinculo, estimulacion, independencia,
raza_real_id, explicacion_equivalencia, descripcion, url_imagen

### universos/perfiles_nd_clinicos.csv
nd_id, nombre,
hiperfoco_min/max/medio, reg_emocional_min/max/medio,
sensorialidad_min/max/medio, comunicacion_min/max/medio,
aprendizaje_min/max/medio, sociabilidad_min/max/medio,
propiocepcion_min/max/medio, f_ejecutiva_min/max/medio,
fuente, explicacion_perfil

### universos/razas_akc_limpio.csv
breed, temperament, popularity, min/max_height, min/max_weight,
min/max_expectancy, group, grooming/shedding/energy/trainability/demeanor
_value/_category/_value_seidr, puntuacion_asistencia, url_imagen, caracter

### universos/recursos_reales/recursos.csv
recurso_id, nombre, tipo, descripcion, edad, gratuito,
url, fuente, modulo, neurodivergencias

---

## DETALLES TÉCNICOS IMPORTANTES

1. **raza_real_id en criaturas.csv** — puede ser número (índice 1-based) o nombre de raza. El módulo 2 maneja ambos casos.
2. **url_imagen en personajes/criaturas** — puede ser ruta local (`iconografia/personajes/nombre.jpg`) o URL de fandom wiki.
3. **Imágenes locales de razas** — todas en `iconografia/razas/` con nombres en minúsculas y guiones bajos.
4. **Imágenes descargadas a mano** — están en `iconografia/personajes/` e `iconografia/criaturas/`.
5. **Copyright** — cada imagen de personaje/criatura muestra atribución según universo. Uso educativo no comercial.
6. **Sin login en bootcamp** — SQLite preparado para añadirlo post-bootcamp.
7. **Módulo 1 bug corregido** — `resetear_modulo1()` limpia el estado para evitar acumulación de respuestas entre tests.

---

## RECURSOS — ESTRUCTURA POR MÓDULO

| Módulo | Nº recursos | Tipos principales |
|--------|------------|-------------------|
| 3 · Comunicación | 10 | asociaciones, herramientas CAA, apps |
| 4 · Aprendizaje | 9 | técnicas, asociaciones, herramientas |
| 5 · Sociabilidad | 8 | asociaciones, comunidades online |
| 6 · Cuerpo | 7 | TO, técnicas, recursos materiales |
| 7 · Clínico | 16 | tests, asociaciones, directorios |

Los recursos se filtran por `neurodivergencias` — columna con lista separada por comas.

---

## NOTAS DE DISEÑO

- **Paleta:** fondo #0d0d12, dorado #c9a84c, texto #e8e0d0, suave #9a9080, azul #4a7fa5
- **Fuentes:** Cinzel (títulos/runas) + Crimson Pro (cuerpo)
- **Imagen portada:** `iconografia/portada_seidr.png` — imagen épica nórdica creada por Jezabel
- **Textura fondo:** `iconografia/textura_piedra.png` — cover, centrada, fixed, sin mosaico
- **Runas del menú:** ᚱ ᚦ ᚨ ᚢ ᚲ ᚷ ᛉ ᛊ ᛏ

---

*Documento generado el 1 de junio de 2026*
*Continúa en nuevo chat — toda la información necesaria está aquí*
