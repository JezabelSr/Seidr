# SEIÐR — Documento de contexto completo
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

- Python · pandas · SQLite · Streamlit · Plotly · Selenium · BeautifulSoup
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

**REGLA DE HIPERFOCO:** El hiperfoco es una obsesión que consume todo lo demás de forma constante. Ser bueno en algo, tener valores sólidos o dedicación NO es hiperfoco. Se ha corregido muchas veces durante la codificación.

---

## LAS 20 NEURODIVERGENCIAS CUBIERTAS

1. Dislexia · 2. TDAH · 3. TEA (incluye TEA Grado 1) · 4. AACC · 5. Discalculia
6. Dispraxia/TDC · 7. Disgrafía · 8. Síndrome de Tourette · 9. TEL · 10. Disfasia
11. SPD · 12. Dislalia · 13. Tartamudez · 14. Hiperlexia · 15. Discapacidad Intelectual
16. TPA · 17. TOC · 18. Mutismo Selectivo · 19. Síndrome de Irlen · 20. TPV

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

### Lanzamiento v1.0 (6 universos):
1. Harry Potter · 2. La Brújula Dorada · 3. Pokémon
4. Studio Ghibli · 5. Cómo entrenar a tu dragón · 6. Disney/Pixar

### Siguientes fases (12 universos):
7. Digimon · 8. One Piece · 9. La Tierra Media · 10. Universo Rick Riordan
11. Avatar Aang/Korra · 12. Juego de Tronos · 13. Las Crónicas de Narnia
14. **Naruto** (sustituyó a Dragon Ball) · 15. Dragon Age
16. The Legend of Zelda · 17. Dragon Quest · 18. Avatar James Cameron

### Agrupación para el test de universo:
- **Grupo A:** HP, Brújula Dorada, Narnia, Rick Riordan, Zelda
- **Grupo B:** Pokémon, HTTYD, Digimon, Dragon Quest, Avatar Cameron
- **Grupo C:** Ghibli, Disney/Pixar
- **Grupo D:** GoT, Dragon Age, La Tierra Media
- **Grupo E:** Naruto, One Piece, Avatar Aang/Korra

---

## ESTADO DE CODIFICACIÓN POR UNIVERSO

### 1. HARRY POTTER ✅ COMPLETO
- 51 personajes codificados (IDs 1-51)
- 32 criaturas con equivalencias (IDs 1-32)
- 22 preguntas test de universo (IDs 1-22, universo_id=0)
- 24 preguntas de dimensiones (IDs 23-46, universo_id=1)

### 2. LA BRÚJULA DORADA ✅ COMPLETO
- 15 personajes (IDs 52-66, universo_id=2)
- 12 criaturas (IDs 33-44, universo_id=2)
- 24 preguntas de dimensiones (IDs 47-70, universo_id=2)

### 3. POKÉMON 🔄 PENDIENTE
- 16 personajes humanos:
  Ash, Misty, Brock, Gary Oak, Profesor Oak, Dawn, Iris, Cilan,
  Serena, Clemont, Tracey, Jessie, James, Giovanni,
  Enfermera Joy, Oficial Jenny
- 72 Pokémon válidos de gen 1 (análisis completo hecho)
- Preguntas: pendiente

### 4. STUDIO GHIBLI 🔄 PENDIENTE
- 23 personajes:
  Chihiro, Haku, Yubaba, Lin, Nausicaä, Lord Yupa, Kushana,
  Ashitaka, San, Lady Eboshi, Sophie, Howl, Calcifer, Kiki,
  Ponyo, Porco Rosso, Sheeta, Pazu, Satsuki, Mei,
  El Baron, Muta, Arrietty
- 12 criaturas:
  Totoro grande, Catbus, Ponyo(forma pez), Jiji, Ohmu, Teto,
  Los Kodama, El espíritu del bosque, El espantapájaros Cabeza de Nabo,
  Los hollines Susuwatari, El bebé ratón, Los lobos de Moro
- Preguntas: pendiente

### 5. HTTYD 🔄 PENDIENTE
- 12 personajes:
  Hipo, Astrid, Gambas, Bocazas, Patán, Valka, Gobber,
  Estoico, Rufino, Zancudo, Drago Bludvist, Eret
- 8 criaturas:
  Desdentado, Tormenta, Meatlug, Barf y Belch,
  Hookfang, Skullcrusher, Cloudjumper, Light Fury
- Preguntas: pendiente

### 6. DISNEY/PIXAR 🔄 PENDIENTE
- 55 personajes (44 ND + 11 neurotípicos):
  ND: Mudito, Pinocho, Alicia, Sombrerero Loco, Conejo Blanco,
  Arthur/Grillo, Tigger, Piglet, Tod, Basilio, Ariel, Bella, Bestia,
  Yago, Rex, Quasimodo, Hércules, Flik, Jane Porter, Kronk,
  Milo Thatch, Lilo, Dory, Marlin, Edna Moda, Rayo McQueen,
  WALL-E, Russell, Rapunzel, Vanellope, Elsa, Hiro Hamada,
  Tristeza, Héctor, Forky, 22, Bruno Madrigal, Giulia,
  Ember, Wade, Ansiedad, Elio, Gary, Merida, Megara
  Neurotípicos: Cenicienta, Tiana, Kida, Esmeralda, Mirabel,
  Aladdín, Li Shang, Príncipe Eric, Flynn Rider, Kristoff
- 55 criaturas (lista completa en manuscritos)
- Preguntas: pendiente

---

## POKÉMON GEN 1 — LISTA DE 72 VÁLIDOS

Incluidos por tener personalidad y vínculo evaluable:
Bulbasaur, Venusaur, Charmander, Charmeleon, Charizard,
Squirtle, Wartortle, Blastoise, Butterfree, Beedrill,
Pidgeotto, Pidgeot, Ekans, Arbok, Pikachu, Raichu,
Clefairy, Clefable, Vulpix, Ninetales, Jigglypuff, Wigglytuff,
Diglett, Dugtrio, Meowth, Persian, Psyduck, Golduck,
Primeape, Growlithe, Arcanine, Abra, Kadabra, Alakazam,
Victreebel, Ponyta, Rapidash, Slowpoke, Slowbro,
Farfetch'd, Muk, Gastly, Haunter, Gengar, Onix,
Krabby, Cubone, Marowak, Koffing, Weezing,
Chansey, Kangaskhan, Horsea, Goldeen, Staryu,
Mr. Mime, Scyther, Tauros, Magikarp, Gyarados,
Lapras, Ditto, Eevee, Vaporeon, Jolteon, Flareon,
Porygon, Snorlax, Dratini, Dragonair, Dragonite

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

## NUMERACIÓN ACTUAL DE IDs

- **Personajes:** último ID usado = 66 (El padre Gomez, Brújula Dorada)
- **Criaturas:** último ID usado = 44 (Balthamos y Baruch, Brújula Dorada)
- **Preguntas:** último ID usado = 70 (función ejecutiva, Brújula Dorada)

---

## DECISIONES TÉCNICAS CLAVE

1. **Sin login en bootcamp** — ahorra ~46h. SQLite con tabla usuarios vacía preparada.
2. **La criatura se asigna automáticamente** desde el perfil de 8 dimensiones. No hay test separado.
3. **Los módulos de vida real** (educación, trabajo, familia) se derivan de las 8 dimensiones en v1.0. Se amplían en post-bootcamp.
4. **Escala AKC (0.2-1.0) convertida a Seiðr (0-5):** valor_seidr = round(valor_akc × 5)
5. **Razas NO repetidas** dentro del mismo universo. Sí pueden repetirse entre universos.
6. **Personajes neurotípicos incluidos** — el test debe funcionar para todo tipo de usuarios.

---

## ARCHIVOS CREADOS EN GITHUB

- manuscritos/arquitectura.md — arquitectura completa del proyecto
- manuscritos/fuentes_clinicas.md — fuentes verificadas para las 20 ND
- universos/razas_akc.csv — dataset AKC original
- universos/razas_akc_limpio.csv — dataset limpio con escala Seiðr
- universos/recursos_reales/organizaciones_espana.csv — 38 organizaciones scrapeadas
- universos/personajes.csv — en construcción
- universos/criaturas.csv — en construcción
- universos/preguntas.csv — en construcción
- runas/01_exploracion_razas.ipynb — EDA completo con 7 visualizaciones
- runas/scraping_organizaciones.ipynb — scraping con Selenium

---

## PRÓXIMA TAREA

Continuar con **Pokémon** — universo 3:
- 16 personajes humanos
- 72 Pokémon como criaturas
- Preguntas de dimensiones

El proceso es: validar perfil → ok → código → siguiente.
Al final de cada universo: código completo junto para pegar de una vez.

---

*Documento generado el 25 de mayo de 2025*
*Continúa en nuevo chat — toda la información necesaria está aquí*
