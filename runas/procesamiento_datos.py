import pandas as pd


def mapear_akc_a_dimensiones_nd(df_akc):
    """Toma un DataFrame con los datos oficiales de la AKC (valores de 1 a 5)

    y genera las 8 dimensiones clínicas de neurodivergencia (escala 1 a 5)
    para poder hacer el matchmaking euclidiano de forma matemática y rigurosa.
    """
    # Creamos una copia para no alterar el DataFrame original de la AKC
    df_clinico = df_akc[["raza", "imagen", "descripcion"]].copy()

    # --- DEFINICIÓN DE LAS 8 DIMENSIONES CLÍNICAS ---

    # 1. HIPERFOCO
    # Lógica: Un perro idóneo para acompañar estados de hiperfoco suele requerir alta capacidad
    # de concentración propia y sintonía con el humano (Trainability) y un temperamento predecible.
    df_clinico["hiperfoco"] = df_akc["trainability_level"]

    # 2. SENSORIALIDAD
    # Lógica: Para mitigar crisis sensoriales auditivas o táctiles, buscamos perros silenciosos
    # (bajo Barking) y calmados (bajo Energy). Invertimos ambos rasgos restándolos de 6.
    # Si Barking es 5 (ladra mucho) -> 6 - 5 = 1 (aporta poca protección sensorial).
    # Si Barking es 1 (muy silencioso) -> 6 - 1 = 5 (aporta mucha protección sensorial).
    df_clinico["sensorialidad"] = (
        (6 - df_akc["barking_level"]) + (6 - df_akc["energy_level"])
    ) / 2

    # 3. REGULACIÓN EMOCIONAL
    # Lógica: El soporte emocional óptimo viene de perros altamente afectuosos con su núcleo,
    # estables y fáciles de entrenar, pero con una energía moderada/baja para no contagiar ansiedad.
    df_clinico["regulacion_emocional"] = (
        df_akc["affectionate_with_family"]
        + df_akc["trainability_level"]
        + (6 - df_akc["energy_level"])
    ) / 3

    # 4. COMUNICACIÓN
    # Lógica: Perros que se expresan de forma clara, predecible y que responden muy bien a comandos
    # no verbales o sutiles del usuario (alta entrenabilidad).
    df_clinico["comunicacion"] = df_akc["trainability_level"]

    # 5. APRENDIZAJE
    # Lógica: Perros con alta adaptabilidad y curiosidad mental que facilitan dinámicas de
    # aprendizaje mutuo o que asimilan rutinas de asistencia complejas rápidamente.
    df_clinico["aprendizaje"] = (
        df_akc["trainability_level"] + df_akc["mental_stimulation_needs"]
    ) / 2

    # 6. SOCIABILIDAD
    # Lógica: Mide la apertura del perro ante el entorno social del usuario. Perros amigables
    # que facilitan la interacción social externa o que no añaden estrés de manejo en público.
    df_clinico["sociabilidad"] = (
        df_akc["open_to_strangers"] + df_akc["good_with_other_dogs"]
    ) / 2

    # 7. PROPIOCEPCIÓN (Conciencia corporal y espacio)
    # Lógica: Personas con retos propioceptivos se benefician de perros que respeten el espacio,
    # jueguen de forma regulada y tengan un tamaño/fuerza acorde a su nivel de control físico.
    # Usamos Trainability (control) e invertimos un exceso de juego descontrolado (Playfulness).
    df_clinico["propiocepcion"] = (
        df_akc["trainability_level"] + (6 - df_akc["playfulness_level"])
    ) / 2

    # 8. FUNCIÓN EJECUTIVA
    # Lógica: Para ayudar a la estructura de rutinas, inicio de tareas y memoria, se necesitan
    # perros muy juguetones/activos que demanden rutinas fijas de paseo y entrenamiento (alta Trainability).
    df_clinico["funcion_ejecutiva"] = (
        df_akc["trainability_level"] + df_akc["playfulness_level"]
    ) / 2

    # Redondeamos los decimales a 1 dígito para que las puntuaciones queden limpias (ej. 4.3)
    columnas_nd = [
        "hiperfoco",
        "sensorialidad",
        "regulacion_emocional",
        "comunicacion",
        "aprendizaje",
        "sociabilidad",
        "propiocepcion",
        "funcion_ejecutiva",
    ]
    df_clinico[columnas_nd] = df_clinico[columnas_nd].round(1)

    return df_clinico