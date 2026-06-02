# SEIÐR
### *Cuando tu saga se convierte en brújula*

> **Seiðr** *(pronunciado "say-thr")* era la magia de los videntes nórdicos: el arte de leer los hilos invisibles del destino y encontrar el camino propio.

Seiðr no es un proyecto. Es una parte de mí hecha código.

Durante años busqué formas de entender cómo funciona mi mente — y la que mejor me funcionó fue siempre la misma: verlo a través de lo que amo, de mis universos de ficción, de mi frikismo. Seiðr nació de la necesidad de ponerle cara a eso que me costó tanto tiempo nombrar, y de hacerlo de una forma que pudiera resonar en otras personas que también llevan años buscando un lenguaje para lo suyo.

Seiðr usa universos de ficción como puerta de entrada a información clínica rigurosa sobre neurodivergencia. Elige tu saga favorita, descubre qué personaje se parece a ti, y encuentra recursos reales adaptados a cómo funciona tu mente.

**La ficción es el vehículo. El conocimiento, el destino.**

🌐 **[seidr-app.streamlit.app](https://seidr-app.streamlit.app)**

---

## ¿Qué hace Seiðr?

La neurodivergencia afecta a entre un 15-20% de la población, pero acceder a información clínica rigurosa puede ser difícil, árido o intimidante. Seiðr propone una puerta de entrada diferente: usar el universo de ficción favorito del usuario como lenguaje para explorar su propio perfil neurocognitivo.

**No es una herramienta de diagnóstico.** Es un punto de partida orientativo que conecta con recursos reales verificados.

---

## Flujo de usuario

```
1. Test de universo    →  El usuario elige su saga favorita (Harry Potter, Pokémon, Ghibli...)
2. Tu perfil           →  24 preguntas en lenguaje del universo → perfil de 8 dimensiones
3. Tu criatura         →  Criatura de asistencia asignada + equivalente en raza canina real
4. Módulos 3-7         →  Recursos reales personalizados: comunicación, aprendizaje,
                          sociabilidad, cuerpo y orientación clínica
```

---

## Stack técnico

| Capa | Tecnología |
|------|-----------|
| Frontend | Streamlit · CSS personalizado · HTML |
| Visualización | Plotly · SVG generado dinámicamente |
| Base de datos | SQLite (generada desde CSV al arrancar) |
| Datos | pandas · 9 tablas · ~1.000 registros |
| Scraping | Selenium · BeautifulSoup |
| Análisis | scipy · numpy · sklearn |
| Deploy | Streamlit Cloud |

---

## Arquitectura de datos

```
universos/
├── universos.csv           # 6 universos disponibles (v1.0)
├── personajes.csv          # 171 personajes con perfil de 8 dimensiones
├── criaturas.csv           # 194 criaturas con equivalencia en raza canina real
├── preguntas.csv           # 166 preguntas en lenguaje de cada universo
├── perfiles_nd_clinicos.csv # 14 neurodivergencias con rangos DSM-5/ICD-11
├── razas_akc_limpio.csv    # 277 razas caninas AKC con escala Seiðr
├── contenido_modulos.csv   # 56 guías personalizadas (14 ND × 4 módulos)
└── recursos_reales/
    ├── recursos.csv        # 50 recursos verificados por módulo
    └── organizaciones_espana.csv  # 38 organizaciones españolas
```

### Las 8 dimensiones del perfil

1. **Hiperfoco** — intensidad y concentración en intereses específicos
2. **Regulación emocional** — cómo se gestiona y expresa la emoción
3. **Sensorialidad** — cómo se procesa el entorno sensorial
4. **Comunicación** — estilo y forma de expresarse
5. **Aprendizaje** — cómo se absorbe y procesa la información
6. **Sociabilidad** — cómo se relaciona con los demás
7. **Propiocepción** — conciencia y necesidades del propio cuerpo
8. **Función ejecutiva** — planificación, organización, inicio de tareas

### Algoritmo de orientación ND

El perfil del usuario (puntuaciones 0-5 en 8 dimensiones) se compara con los rangos clínicos de 14 neurodivergencias usando un sistema de dimensiones clave obligatorias + umbral mínimo de coincidencia. El resultado es orientativo, nunca diagnóstico.

---

## Universos disponibles (v1.0)

| # | Universo | Personajes | Criaturas |
|---|---------|-----------|---------|
| 1 | Harry Potter | 51 | 32 |
| 2 | La Brújula Dorada | 15 | 12 |
| 3 | Pokémon | 17 | 77 |
| 4 | Studio Ghibli | 23 | 11 |
| 5 | Cómo entrenar a tu dragón | 11 | 8 |
| 6 | Disney/Pixar | 55 | 55 |

**12 universos adicionales** planificados para fases posteriores.

---

## Instalación local

```bash
# Clonar el repositorio
git clone https://github.com/JezabelSr/Seidr.git
cd Seidr

# Crear entorno virtual e instalar dependencias
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Mac/Linux

pip install -r requirements.txt

# Ejecutar
streamlit run app.py
```

La base de datos SQLite se genera automáticamente desde los CSVs al arrancar por primera vez.

---

## Estructura del proyecto

```
Seidr/
├── app.py                    # Punto de entrada Streamlit
├── seidr.db                  # Base de datos SQLite (generada automáticamente)
├── hechizos/                 # Módulos Python
│   ├── crear_bd.py           # Migración CSV → SQLite
│   ├── db.py                 # Capa de acceso a datos
│   ├── orientacion_nd.py     # Algoritmo de orientación ND
│   ├── narrador.py           # Textos narrativos por universo
│   ├── razas_helper.py       # Búsqueda de razas por nombre
│   ├── test_universo.py      # Test de selección de universo
│   ├── modulo_1.py           # Tu perfil
│   ├── modulo_2.py           # Tu criatura
│   ├── modulo_3.py           # Comunicación
│   ├── modulo_4.py           # Aprendizaje
│   ├── modulo_5.py           # Sociabilidad
│   ├── modulo_6.py           # Tu cuerpo
│   ├── modulo_7.py           # Orientación clínica
│   └── modo_profesional.py   # Acceso directo para profesionales
├── universos/                # Datos CSV
├── iconografia/              # Imágenes, fondos, música
│   ├── fondos/               # Fondos por universo (.webp)
│   └── musica/               # Música ambiental por universo (.mp3)
├── runas/                    # Notebooks Jupyter (EDA, scraping)
└── manuscritos/              # Documentación técnica
```

---

## Licencias

- **Código:** [AGPL v3](LICENSE)
- **Datos y contenido:** [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)
- **Imágenes de personajes/criaturas:** uso educativo no comercial — atribución por universo en la app
- **Fuentes clínicas:** DSM-5, ICD-11, literatura científica revisada por pares

---

## Sobre el proyecto

Proyecto personal desarrollado durante el bootcamp de Data Analytics de [Adalab](https://adalab.es).

**Autora:** Jezabel S. R. · [GitHub](https://github.com/JezabelSr) · [jsr.dataanalyst@gmail.com](mailto:jsr.dataanalyst@gmail.com)

---

*Seiðr no es una herramienta de diagnóstico. Es un punto de partida.*