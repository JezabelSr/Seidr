# Seiðr — Arquitectura del proyecto
*Cuando tu saga se convierte en brújula*

---

## Las 8 dimensiones de rasgos

La columna vertebral de todo el proyecto.
Cada personaje, criatura, pregunta y recurso 
se codifica con estas 8 dimensiones en escala 0-5.

| # | Dimensión | Qué mide |
|---|-----------|----------|
| 1 | Hiperfoco | Intensidad y concentración en intereses específicos |
| 2 | Regulación emocional | Cómo se gestiona y expresa la emoción |
| 3 | Sensorialidad | Cómo se procesa el entorno sensorial |
| 4 | Comunicación | Estilo y forma de expresarse |
| 5 | Aprendizaje | Cómo se absorbe y procesa la información |
| 6 | Sociabilidad | Cómo se relaciona con los demás |
| 7 | Propiocepción | Conciencia y necesidades del propio cuerpo |
| 8 | Función ejecutiva | Planificación, organización, inicio de tareas, flexibilidad cognitiva |

---

## Las 20 neurodivergencias cubiertas

1. Dislexia
2. TDAH
3. TEA (incluye TEA Grado 1, antes llamado Asperger)
4. Altas Capacidades (AACC)
5. Discalculia
6. Dispraxia / TDC
7. Disgrafía
8. Síndrome de Tourette
9. TEL — Trastorno Específico del Lenguaje
10. Disfasia
11. Procesamiento Sensorial Atípico (SPD)
12. Dislalia
13. Tartamudez / Disfluencia
14. Hiperlexia
15. Discapacidad Intelectual (DI)
16. Trastorno de Procesamiento Auditivo (TPA)
17. TOC — Trastorno Obsesivo Compulsivo
18. Mutismo Selectivo
19. Síndrome de Irlen / Estrés Visual
20. Trastorno del Procesamiento Visual (TPV)

---

## Esquema de tablas — detalle completo

### universos/universos.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| universo_id | INT | Identificador único (PK) |
| nombre | TEXT | Nombre del universo |
| tono | TEXT | aventura / drama / fantasia / anime / animacion |
| audiencia | TEXT | infantil / juvenil / adulto / multigeneracional |
| paleta_css | TEXT | Nombre del tema CSS asociado |
| activo | BOOLEAN | True si está en la versión actual |

### universos/neurodivergencias.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| nd_id | INT | Identificador único (PK) |
| nombre | TEXT | Nombre de la neurodivergencia |
| descripcion_breve | TEXT | Qué es en una frase |
| dimensiones_afectadas | TEXT | Dimensiones principales que afecta |

### universos/personajes.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| personaje_id | INT | Identificador único (PK) |
| universo_id | INT | FK → universos.csv |
| nombre | TEXT | Nombre del personaje |
| rol | TEXT | protagonista / aliado / mentor / antagonista |
| hiperfoco | INT | 0-5 |
| regulacion_emocional | INT | 0-5 |
| sensorialidad | INT | 0-5 |
| comunicacion | INT | 0-5 |
| aprendizaje | INT | 0-5 |
| sociabilidad | INT | 0-5 |
| propiocepcion | INT | 0-5 |
| funcion_ejecutiva | INT | 0-5 |
| estilo_comunicacion | TEXT | verbal_directo / verbal_indirecto / no_verbal / mixto |
| estilo_aprendizaje | TEXT | teorico / practico / asociativo / especializado / visual |
| estilo_socializacion | TEXT | expansivo / intimo / autonomo / selectivo / cuidador |
| perfil_sensorial | TEXT | buscador / evitador / mixto / hiposensible / hipersensible |
| justificacion | TEXT | Por qué tiene esas puntuaciones — cita del canon |

### universos/criaturas.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| criatura_id | INT | Identificador único (PK) |
| universo_id | INT | FK → universos.csv |
| nombre | TEXT | Nombre de la criatura |
| calma | INT | 0-5 |
| vinculo | INT | 0-5 |
| estimulacion | INT | 0-5 |
| independencia | INT | 0-5 |
| raza_real_id | INT | FK → razas_asistencia.csv |
| explicacion_equivalencia | TEXT | Por qué esa raza real |

### universos/razas_asistencia.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| raza_id | INT | Identificador único (PK) |
| nombre_raza | TEXT | Nombre de la raza |
| caracteristicas | TEXT | Descripción de características clave |
| nivel_energia | INT | 0-5 |
| tamano | TEXT | pequeno / mediano / grande |
| facilidad_entrenamiento | INT | 0-5 |
| organizaciones_espana | TEXT | Nombres de asociaciones |
| fuentes_verificadas | TEXT | URLs de fuentes clínicas |

### universos/preguntas.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| pregunta_id | INT | Identificador único (PK) |
| universo_id | INT | FK → universos.csv (0 = test general) |
| dimension | TEXT | Nombre de la dimensión que mide |
| modulo | INT | 0=test universo / 1-6=modulo |
| texto | TEXT | Texto de la pregunta |
| opcion_a | TEXT | Texto opción A |
| puntuacion_a | INT | Puntuación opción A |
| opcion_b | TEXT | Texto opción B |
| puntuacion_b | INT | Puntuación opción B |
| opcion_c | TEXT | Texto opción C |
| puntuacion_c | INT | Puntuación opción C |

### universos/recursos_reales/recursos.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| recurso_id | INT | Identificador único (PK) |
| nombre | TEXT | Nombre del recurso |
| tipo | TEXT | terapia / herramienta / curso / asociacion / test |
| descripcion | TEXT | Qué es y para qué sirve |
| edad | TEXT | infantil / adulto / ambos |
| gratuito | BOOLEAN | True si es gratuito |
| url | TEXT | Enlace verificado |
| fuente | TEXT | Organización que lo avala |
| modulo | INT | Módulo al que pertenece (3-7) |

### universos/recursos_reales/recursos_nd.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT | Identificador único (PK) |
| recurso_id | INT | FK → recursos.csv |
| nd_id | INT | FK → neurodivergencias.csv |

---

## Los 7 módulos

| Módulo | Dimensión principal | Capa friki | Capa real |
|--------|---------------------|------------|-----------|
| 1 | Todas | Tu personaje | Perfil orientativo ND |
| 2 | Todas | Tu criatura de asistencia | Raza real + organizaciones |
| 3 | Comunicación | Tu forma de comunicarte | Logopedia, CAA, recursos |
| 4 | Aprendizaje + F.Ejecutiva | Tu forma de aprender | Técnicas, adaptaciones |
| 5 | Sociabilidad | Tu forma de socializar | Hobbies, comunidades |
| 6 | Propiocepción + Sensorialidad | Tu propiocepción | Autorregulación, TO |
| 7 | Todas | Módulo clínico | Tests gratuitos, profesionales |

---

## Los 18 universos

### Lanzamiento v1.0
1. Harry Potter
2. La Brújula Dorada
3. Pokémon
4. Studio Ghibli
5. Cómo entrenar a tu dragón
6. Disney / Pixar

### Siguientes fases
7. Digimon · 8. One Piece · 9. La Tierra Media
10. Universo Rick Riordan · 11. Avatar Aang/Korra
12. Juego de Tronos · 13. Las Crónicas de Narnia
14. Dragon Ball · 15. Dragon Age
16. The Legend of Zelda · 17. Dragon Quest
18. Avatar James Cameron

---

## Ámbitos de la capa real

- 🏫 Educación: adaptaciones curriculares, estilos de aprendizaje
- 👨‍👩‍👧 Familia: convivencia, comunicación, post-diagnóstico
- 🏠 Vida autónoma: organización, trabajo, rutinas
- 🤝 Social: habilidades sociales, comunidades, ocio
- 🐕 Asistencia animal: perros de asistencia, organizaciones
- 🏥 Salud: terapias, profesionales, tests verificados

---

*Versión 1.0 — Mayo 2025*
*Autora: Jezabel Sr*