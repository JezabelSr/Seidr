# SEIÐR — Documento de contexto completo v2
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

- Python · pandas · SQLite · Streamlit · Plotly · Selenium · BeautifulSoup · scipy
- Entorno virtual: venv — activar con `source venv/Scripts/activate`
- Kernel Jupyter: "Seidr (venv)"
- Sin login en bootcamp — arquitectura SQLite preparada para añadirlo post-bootcamp
- Deploy: Streamlit Cloud

---

## LICENCIAS

- **Código:** AGPL v3
- **Datos y contenido:** CC BY-NC-ND 4.0

---

## ESTRUCTURA DE CARPETAS

```
Seidr/
├── universos/          # datos CSV
│   └── recursos_reales/
├── runas/              # notebooks Jupyter
├── hechizos/           # código Python
│   └── orientacion_nd.py  # ← NUEVO algoritmo de orientación ND
├── iconografia/        # imágenes y assets
├── manuscritos/        # documentación
├── .vscode/settings.json
├── venv/
├── .gitignore
├── LICENSE (AGPL v3)
└── README.md
```

---

## LAS 8 DIMENSIONES DE RASGOS (escala 0-5)

1. Hiperfoco — intensidad y concentración en intereses específicos
2. Regulación emocional — cómo se gestiona y expresa la emoción
3. Sensorialidad — cómo se procesa el entorno sensorial
4. Comunicación — estilo y forma de expresarse
5. Aprendizaje — cómo se absorbe y procesa la información
6. Sociabilidad — cómo se relaciona con los demás
7. Propiocepción — conciencia y necesidades del propio cuerpo
8. Función ejecutiva — planificación, organización, inicio de tareas, flexibilidad cognitiva

**REGLA DE HIPERFOCO:** El hiperfoco es una obsesión que consume todo lo demás de forma constante. Ser bueno en algo, tener valores sólidos o dedicación NO es hiperfoco.

---

## LAS 20 NEURODIVERGENCIAS CUBIERTAS (LISTA ACTUALIZADA)

1. Dislexia · 2. TDAH · 3. TEA · 4. AACC · 5. Discalculia
6. Dispraxia/TDC · 7. Disgrafía · 8. Síndrome de Tourette · 9. TEL · 10. SPD
11. Tartamudez · 12. Discapacidad Intelectual · 13. TOC · 14. Mutismo Selectivo
15. Síndrome de Irlen · 16. Trastorno Fonológico · 17. Trastorno de Comunicación Social
18. Trastorno por Movimientos Estereotipados · 19. Trastorno de Ansiedad Social · 20. TANV

**NOTA:** Se eliminaron Disfasia, Dislalia, Hiperlexia, TPA y TPV por no estar reconocidas como entidades independientes en DSM-5/ICD-11. Se sustituyeron por las 5 nuevas ND anteriores.

---

## ESQUEMA DE TABLAS CSV

### universos/universos.csv
universo_id(PK), nombre, tono, audiencia, paleta_css, activo

### universos/personajes.csv
personaje_id(PK), universo_id(FK), nombre, rol,
hiperfoco, regulacion_emocional, sensorialidad, comunicacion,
aprendizaje, sociabilidad, propiocepcion, funcion_ejecutiva,
estilo_comunicacion, estilo_aprendizaje, estilo_socializacion,
perfil_sensorial, justificacion

### universos/criaturas.csv
criatura_id(PK), universo_id(FK), nombre,
calma, vinculo, estimulacion, independencia,
raza_real_id(FK), explicacion_equivalencia

### universos/preguntas.csv
pregunta_id(PK), universo_id(FK), dimension, modulo, texto,
opcion_a, puntuacion_a, opcion_b, puntuacion_b,
opcion_c, puntuacion_c, opcion_d, puntuacion_d,
opcion_e, puntuacion_e

### universos/neurodivergencias.csv
nd_id(PK), nombre, descripcion_breve, dimensiones_afectadas

### universos/recursos_reales/recursos.csv
recurso_id(PK), nombre, tipo, descripcion, edad, gratuito, url, fuente, modulo

### universos/recursos_reales/recursos_nd.csv
id(PK), recurso_id(FK), nd_id(FK)

### universos/perfiles_nd_clinicos.csv ← NUEVO
nd_id, nombre, hiperfoco_min/max, reg_emocional_min/max, sensorialidad_min/max,
comunicacion_min/max, aprendizaje_min/max, sociabilidad_min/max,
propiocepcion_min/max, f_ejecutiva_min/max, fuente,
+ columnas _medio calculadas

---

## LOS 7 MÓDULOS

| Módulo | Dimensión principal | Capa friki | Capa real |
|--------|--------------------|-----------| ---------|
| 1 | Todas | Tu personaje | Perfil orientativo ND |
| 2 | Todas | Tu criatura de asistencia | Raza real + organizaciones |
| 3 | Comunicación | Tu forma de comunicarte | Logopedia, CAA, recursos |
| 4 | Aprendizaje + F.Ejecutiva | Tu forma de aprender | Técnicas, adaptaciones |
| 5 | Sociabilidad | Tu forma de socializar | Hobbies, comunidades |
| 6 | Propiocepción + Sensorialidad | Tu propiocepción | Autorregulación, TO |
| 7 | Todas | Módulo clínico | Tests gratuitos, profesionales |

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

## ESTADO DE CODIFICACIÓN POR UNIVERSO

### 1. HARRY POTTER ✅ COMPLETO
- 51 personajes (IDs 1-51)
- 32 criaturas (IDs 1-32)
- 22 preguntas test de universo (IDs 1-22, universo_id=0)
- 24 preguntas de dimensiones (IDs 23-46, universo_id=1)

### 2. LA BRÚJULA DORADA ✅ COMPLETO
- 15 personajes (IDs 52-66, universo_id=2)
- 12 criaturas (IDs 33-44, universo_id=2)
- 24 preguntas de dimensiones (IDs 47-70, universo_id=2)

### 3. POKÉMON ✅ COMPLETO
- 17 personajes humanos (IDs 67-83, universo_id=3)
  Ash, Misty, Brock, Gary Oak, Profesor Oak, Dawn, Iris, Cilan,
  Serena, Clemont, Tracey, Jessie, James, Giovanni,
  Enfermera Joy, Oficial Jenny, Profesor Kukui
- 77 criaturas (IDs 45-121, universo_id=3)
  72 Pokémon Gen 1 + 5 Eeveeluciones (Espeon, Umbreon, Leafeon, Glaceon, Sylveon)
- 24 preguntas de dimensiones (IDs 71-94, universo_id=3)

### 4. STUDIO GHIBLI ✅ COMPLETO
- 23 personajes (IDs 84-106, universo_id=4)
  Chihiro, Haku, Yubaba, Lin, Nausicaä, Lord Yupa, Kushana,
  Ashitaka, San, Lady Eboshi, Sophie, Howl, Calcifer, Kiki,
  Ponyo, Porco Rosso, Sheeta, Pazu, Satsuki, Mei,
  El Baron, Muta, Arrietty
- 11 criaturas (IDs 121-131, universo_id=4)
  Totoro grande, GatoBus, Ponyo forma pez, Jiji, Ohmu, Teto,
  Los Kodama, Espantapájaros Cabeza de Nabo, Susuwataris,
  Bebé ratón, Lobos de Moro
  NOTA: El espíritu del bosque fue eliminado por no buscar vínculo
- 24 preguntas de dimensiones (IDs 95-118, universo_id=4)

### 5. CÓMO ENTRENAR A TU DRAGÓN ✅ COMPLETO
- 11 personajes (IDs 107-117, universo_id=5)
  Hipo, Astrid, Patapez, Mocoso, Chusco, Brusca, Bocón,
  Valka, Estoico el inmenso, Drago Puño Sangriento, Eret
- 8 criaturas (IDs 132-139, universo_id=5)
  Desdentado, Tormenta, Barrilete, Vómito y Eructo,
  Colmillo, Rompecráneos, Asaltanubes, Furia Diurna
- 24 preguntas de dimensiones (IDs 119-142, universo_id=5)

### 6. DISNEY/PIXAR ✅ COMPLETO
- 55 personajes (IDs 118-172, universo_id=6)
  ND: Mudito, Pinocho, Alicia, Sombrerero Loco, Conejo Blanco,
  Arthur/Grillo, Tigger, Piglet, Tod, Basilio, Ariel, Bella, Bestia,
  Rex, Quasimodo, Hércules, Flik, Jane Porter, Kronk,
  Milo Thatch, Lilo, Dory, Marlin, Edna Moda, Rayo McQueen,
  WALL-E, Russell, Rapunzel, Vanellope, Elsa, Hiro Hamada,
  Tristeza, Héctor, Forky, Número 22, Bruno Madrigal, Giulia,
  Candela Lumen, Nilo Fuentes, Ansiedad, Elio, Merida, Megara
  NT: Cenicienta, Tiana, Kida, Esmeralda, Mirabel,
  Aladdin, Li Shang, Príncipe Eric, Flynn Rider, Kristoff, Gary
- 55 criaturas (IDs 140-194, universo_id=6)
  Yago, Timothy Q. Mouse, Gato de Cheshire, Arquímedes,
  Rey Louie, Baloo, Winnie Pooh, Ígor, Gurgi, Sebastián,
  Flounder, Genio, Abu, Hugo Víctor y Laverne, Pegaso,
  Filoctetes, Mushu, Cri-Kee, Hermanito, Terk, Tantor,
  Stitch, Sulley, Mike Wazowski, Koda, Remy, Dug, Pascal,
  Maximus, Abuelo Pabbie, Olaf, Baymax, Bing Bong, Dante,
  Pepita, Bruni, El Nokk, Sisu, Tuk Tuk, Machiavelli, Sox,
  Estrella, Pena, Pánico, Sven, Meeko, Flit, Percy, Jack,
  Gus, Angus, Pua, Akela, Raksha, Valentino
- 24 preguntas de dimensiones (IDs 143-166, universo_id=6)

---

## NUMERACIÓN ACTUAL DE IDs

- **Personajes:** último ID usado = 172 (Gary, Disney/Pixar)
- **Criaturas:** último ID usado = 194 (Valentino, Disney/Pixar)
- **Preguntas:** último ID usado = 166 (función ejecutiva, Disney/Pixar)

---

## ALGORITMO DE ORIENTACIÓN ND ← NUEVO

**Archivo:** `hechizos/orientacion_nd.py`
**Función:** `orientar_nd(perfil_usuario, df_nd, umbral=7)`
**Dataset:** `universos/perfiles_nd_clinicos.csv`
**Notebook:** `runas/02_perfiles_nd_clinicos.ipynb`

### Cómo funciona:
1. Cada ND tiene dimensiones clave obligatorias — si el perfil no cae en rango en ellas, la ND se descarta
2. Se calcula cuántas de las 8 dimensiones están en rango clínico
3. Umbral mínimo de 7/8 para considerar una ND
4. Máximo 2 resultados cuando hay dos ND con 8/8

### Reglas de salida:
- 8/8 dimensiones → ✅ Perfil compatible (100%)
- 7/8 dimensiones → 🔶 Posible perfil (87.5%)
- <7/8 dimensiones → ⬜ Perfil Neurotípico

### Dimensiones clave por ND:
```python
dimensiones_clave = {
    'Dislexia':                                ['aprendizaje', 'comunicacion'],
    'TDAH':                                    ['hiperfoco', 'f_ejecutiva'],
    'TEA':                                     ['hiperfoco', 'sociabilidad'],
    'AACC':                                    ['hiperfoco', 'aprendizaje'],
    'Discalculia':                             ['aprendizaje'],
    'Dispraxia/TDC':                           ['propiocepcion'],
    'Disgrafía':                               ['comunicacion'],
    'Síndrome de Tourette':                    ['sensorialidad'],
    'TEL':                                     ['comunicacion'],
    'SPD':                                     ['sensorialidad', 'reg_emocional'],
    'Tartamudez':                              ['comunicacion'],
    'Discapacidad Intelectual':                ['aprendizaje', 'f_ejecutiva'],
    'TOC':                                     ['hiperfoco', 'f_ejecutiva'],
    'Mutismo Selectivo':                       ['comunicacion', 'sociabilidad'],
    'Síndrome de Irlen':                       ['sensorialidad', 'aprendizaje'],
    'Trastorno Fonológico':                    ['comunicacion'],
    'Trastorno de Comunicación Social':        ['comunicacion', 'sociabilidad'],
    'Trastorno por Movimientos Estereotipados': ['propiocepcion', 'f_ejecutiva'],
    'Trastorno de Ansiedad Social':            ['sociabilidad', 'reg_emocional'],
    'TANV':                                    ['aprendizaje', 'propiocepcion']
}
```

### Validación con personajes:
| Personaje | ND esperada | ND obtenida | Resultado |
|---|---|---|---|
| Ash Ketchum | TDAH | TDAH | ✅ 100% |
| Elsa | TEA | TEA | ✅ 100% |
| Hermione Granger | AACC | AACC | ✅ 100% |
| Lilo | TEA | TEA | ✅ 100% |
| Clemont | TEA/AACC | AACC | ✅ 87.5% |
| Perfil NT | Neurotípico | Neurotípico | ✅ |

---

## NOTEBOOKS JUPYTER

### runas/01_exploracion_razas.ipynb ✅
EDA completo de razas AKC con 7 visualizaciones

### runas/02_perfiles_nd_clinicos.ipynb ✅ NUEVO
- Dataset clínico DSM-5/ICD-11 de 20 ND
- Análisis de rangos por dimensión
- Heatmap de perfiles
- Matriz de distancias entre perfiles
- Algoritmo orientar_nd_v4
- Validación con personajes

### runas/scraping_organizaciones.ipynb ✅
Scraping con Selenium de organizaciones en España

---

## DECISIONES TÉCNICAS CLAVE

1. **Sin login en bootcamp** — ahorra ~46h. SQLite con tabla usuarios vacía preparada.
2. **La criatura se asigna automáticamente** desde el perfil de 8 dimensiones.
3. **Los módulos de vida real** se derivan de las 8 dimensiones en v1.0.
4. **Escala AKC (0.2-1.0) convertida a Seiðr (0-5):** valor_seidr = round(valor_akc × 5)
5. **Razas NO repetidas** dentro del mismo universo. Sí pueden repetirse entre universos.
6. **Personajes neurotípicos incluidos** — el test debe funcionar para todo tipo de usuarios.
7. **Algoritmo de orientación ND** — orienta, no diagnostica. Umbral 7/8 + dimensiones clave.

---

## ARCHIVOS EN GITHUB

- manuscritos/arquitectura.md
- manuscritos/fuentes_clinicas.md
- universos/razas_akc.csv
- universos/razas_akc_limpio.csv
- universos/perfiles_nd_clinicos.csv ← NUEVO
- universos/recursos_reales/organizaciones_espana.csv
- universos/personajes.csv ✅ COMPLETO (IDs 1-172)
- universos/criaturas.csv ✅ COMPLETO (IDs 1-194)
- universos/preguntas.csv ✅ COMPLETO (IDs 1-166)
- hechizos/orientacion_nd.py ← NUEVO
- runas/01_exploracion_razas.ipynb
- runas/02_perfiles_nd_clinicos.ipynb ← NUEVO
- runas/scraping_organizaciones.ipynb
- iconografia/rangos_nd_dimensiones.png ← NUEVO
- iconografia/heatmap_nd_dimensiones.png ← NUEVO
- iconografia/distancias_nd.png ← NUEVO

---

## PRÓXIMA TAREA

Construir la **app en Streamlit** — los 7 módulos funcionando:

### Orden sugerido:
1. Estructura base de la app (navegación, tema visual)
2. Test de universo (preguntas universo_id=0)
3. Test de dimensiones por universo (Módulo 1)
4. Algoritmo de orientación ND integrado
5. Asignación de criatura (Módulo 2)
6. Recursos reales (Módulos 3-7)
7. Conectar CSVs a SQLite
8. Deploy en Streamlit Cloud

### Archivos clave para la app:
- `universos/personajes.csv` — perfiles de personajes
- `universos/criaturas.csv` — criaturas con razas reales
- `universos/preguntas.csv` — preguntas del test
- `universos/perfiles_nd_clinicos.csv` — perfiles clínicos ND
- `hechizos/orientacion_nd.py` — función de orientación
- `universos/recursos_reales/recursos.csv` — recursos reales
- `universos/recursos_reales/organizaciones_espana.csv` — organizaciones

---

## TEST DE UNIVERSO — ÁRBOL COMPLETO

**Bloque 1 (3 preguntas generales → 5 grupos)**
**Bloque 2 por grupo:**
- Grupo A: 4 preguntas (HP, Brújula, Narnia, Rick Riordan, Zelda)
- Grupo B: 4 preguntas (Pokémon, HTTYD, Digimon, Dragon Quest, Avatar Cameron)
- Grupo C: 3 preguntas (Ghibli, Disney/Pixar)
- Grupo D: 4 preguntas (GoT, Dragon Age, Tierra Media)
- Grupo E: 4 preguntas (Naruto, One Piece, Avatar Aang/Korra)

**Total: máximo 7 preguntas por usuario. Todas en preguntas.csv con universo_id=0**

---

## ESTRUCTURA DE PREGUNTAS DE DIMENSIONES

- 3 preguntas por dimensión × 8 dimensiones = 24 preguntas por universo
- 4 opciones por pregunta: puntuaciones 0, 2, 4, 5
- En lenguaje del universo, sin jerga clínica
- universo_id = número del universo, modulo = 1

---

*Documento generado el 29 de mayo de 2026*
*Continúa en nuevo chat — toda la información necesaria está aquí*
