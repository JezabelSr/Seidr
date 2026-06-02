"""
SEIÐR — Narrador contextual
Textos narrativos por universo para momentos clave de la app.
"""

NARRADOR = {
    1: {  # Harry Potter
        "universo_elegido": (
            "El Sombrero Seleccionador no se equivoca. "
            "Has elegido el mundo que te pertenece. "
            "Lo que descubras aquí quedará grabado en los registros de Hogwarts."
        ),
        "perfil_completado": (
            "Tu perfil ha quedado registrado en el Libro de las Admisiones. "
            "Como bien saben los magos, conocerse a uno mismo es el hechizo más poderoso que existe. "
            "Lo que ves aquí no es un diagnóstico — es un mapa."
        ),
        "criatura_asignada": (
            "No todas las criaturas eligen a su compañero por casualidad. "
            "La tuya ha respondido a algo que reconoció en ti. "
            "Cuídala bien — los vínculos mágicos son para siempre."
        ),
        "modulo_recursos": (
            "El conocimiento es el arma más poderosa que existe. "
            "Cada recurso que encuentres aquí ha sido seleccionado con cuidado, "
            "como los libros de la biblioteca de Hogwarts — pero estos puedes llevártelos contigo."
        ),
    },
    2: {  # La Brújula Dorada
        "universo_elegido": (
            "Tu daimonion se ha asentado. "
            "Hay mundos paralelos donde versiones de ti ya conocen lo que estás a punto de descubrir. "
            "La Verdad no duele — ilumina."
        ),
        "perfil_completado": (
            "El aletiómetro no miente nunca. "
            "Tu perfil es una lectura honesta de quién eres, "
            "no de quién deberías ser. "
            "Guárdalo como una brújula, no como una sentencia."
        ),
        "criatura_asignada": (
            "Los daimonions no se eligen — se revelan. "
            "La criatura que te acompaña refleja algo que siempre ha estado en ti, "
            "esperando ser nombrado."
        ),
        "modulo_recursos": (
            "En los mundos paralelos, el conocimiento toma formas distintas. "
            "En este, toma la forma de recursos reales, verificados, "
            "construidos por personas que entienden cómo funciona tu mente."
        ),
    },
    3: {  # Pokémon
        "universo_elegido": (
            "¡Una nueva aventura comienza! "
            "Has elegido tu universo — ahora toca descubrir qué entrenador eres. "
            "¡El Profesor Oak estaría orgulloso!"
        ),
        "perfil_completado": (
            "¡Datos registrados en la Pokédex! "
            "Tu perfil acaba de actualizarse con información que ningún otro entrenador tiene: "
            "el mapa completo de cómo funciona tu mente. "
            "¡Úsalo bien!"
        ),
        "criatura_asignada": (
            "¡Pokémon recibido! "
            "No todos los Pokémon encajan con todos los entrenadores — "
            "el tuyo te ha elegido por una razón. "
            "Juntos seréis más fuertes."
        ),
        "modulo_recursos": (
            "Todo buen entrenador sabe que la batalla no es solo física. "
            "Aquí tienes los recursos para entrenar la parte más importante: "
            "entenderte a ti mismo y pedir lo que necesitas."
        ),
    },
    4: {  # Studio Ghibli
        "universo_elegido": (
            "El viento te ha traído hasta aquí. "
            "En los mundos de Miyazaki, nada ocurre por casualidad — "
            "has elegido bien."
        ),
        "perfil_completado": (
            "Los espíritus del bosque reconocen a quienes se conocen a sí mismos. "
            "Tu perfil es un reflejo tranquilo, como el agua antes de que sople el viento. "
            "Mírate en él sin prisa."
        ),
        "criatura_asignada": (
            "Las criaturas de Ghibli no aparecen ante cualquiera. "
            "La tuya ha decidido acompañarte — "
            "eso significa que hay algo en ti que merece ser acompañado."
        ),
        "modulo_recursos": (
            "El camino de vuelta a casa siempre existe, "
            "aunque a veces necesitemos ayuda para encontrarlo. "
            "Estos recursos son parte de ese camino."
        ),
    },
    5: {  # Cómo entrenar a tu dragón
        "universo_elegido": (
            "No todos los vikingos luchan igual — y eso está bien. "
            "Hipo cambió su mundo entendiéndolo primero. "
            "Tú también puedes."
        ),
        "perfil_completado": (
            "Un buen vikingo conoce sus fuerzas y sus límites. "
            "Tu perfil no es una debilidad — es inteligencia táctica. "
            "Los mejores jinetes de dragón saben exactamente quiénes son."
        ),
        "criatura_asignada": (
            "Los dragones no se doman — se gana su confianza. "
            "Tu criatura te la ha dado. "
            "Eso no se consigue con fuerza, sino con presencia."
        ),
        "modulo_recursos": (
            "Berk no se construyó en un día, y ningún cambio real ocurre de golpe. "
            "Estos recursos son herramientas para construir tu propio Berk: "
            "un lugar donde ser exactamente como eres."
        ),
    },
    6: {  # Disney/Pixar
        "universo_elegido": (
            "Cada historia de Disney empieza con alguien que decide ser honesto consigo mismo. "
            "La tuya acaba de empezar."
        ),
        "perfil_completado": (
            "Como diría Inside Out: todas tus emociones tienen razón de estar ahí. "
            "Tu perfil no juzga cómo funciona tu mente — "
            "la celebra exactamente como es."
        ),
        "criatura_asignada": (
            "Los mejores compañeros de Disney no son perfectos — son fieles. "
            "El tuyo lo será contigo, "
            "igual que tú puedes aprender a serlo contigo mismo."
        ),
        "modulo_recursos": (
            "Incluso Pixar sabe que los finales felices requieren trabajo. "
            "Estos recursos no son magia — son el trabajo real "
            "que hace posible que la magia ocurra."
        ),
    },
}


def get_narrador(universo_id: int, momento: str) -> str:
    """
    Devuelve el texto narrativo para un universo y momento dados.
    
    momentos: universo_elegido | perfil_completado | criatura_asignada | modulo_recursos
    """
    return NARRADOR.get(universo_id, {}).get(momento, "")
