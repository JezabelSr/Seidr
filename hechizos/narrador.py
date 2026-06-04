"""
SEIÐR — Narrador contextual
Textos narrativos por universo para momentos clave de la app.
Revisado: 03/06/2026
"""

NARRADOR = {
    1: {  # Harry Potter
        "universo_elegido": (
            "El Sombrero Seleccionador no se equivoca. "
            "Has llegado al mundo al que perteneces. "
            "Lo que descubras aquí quedará grabado en los registros de Hogwarts."
        ),
        "perfil_completado": (
            "Tu perfil ha quedado registrado en el Libro de Admisiones. "
            "Como bien saben los magos, conocerse a uno mismo es el hechizo más poderoso que existe. "
            "Lo que ves aquí no es un diagnóstico, es un mapa."
        ),
        "criatura_asignada": (
            "En el mundo mágico, los vínculos entre humano y criatura no se fabrican, se reconocen. "
            "Ese vínculo ya existe, ahora solo queda honrarlo."
        ),
        "modulo_recursos": (
            "El conocimiento es el arma más poderosa que existe. "
            "Cada recurso que encuentres aquí ha sido seleccionado con cuidado, "
            "como los libros de la Gran Biblioteca, "
            "solo que esto puedes llevártelo contigo."
        ),
    },
    2: {  # La Brújula Dorada
        "universo_elegido": (
            "Tu daimonion ha tomado forma. "
            "Hay mundos paralelos donde versiones de ti ya conocen lo que estás a punto de descubrir. "
            "La Verdad no duele, ilumina."
        ),
        "perfil_completado": (
            "El aletiómetro no miente nunca. "
            "Tu perfil es una lectura honesta de quién eres, "
            "no de quién deberías ser. "
            "Guárdalo como una brújula, no como una sentencia."
        ),
        "criatura_asignada": (
            "Los daimonions no se eligen, nacen contigo y toman forma a medida que te descubres. "
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
            "Coge tu Pokédex y prepárate, "
            "porque lo que estás a punto de descubrir no aparece en ningún registro anterior. "
            "Averigüemos qué tipo de entrenador eres."
        ),
        "perfil_completado": (
            "¡Datos registrados en la Pokédex! "
            "Tu perfil acaba de actualizarse con información que ningún otro entrenador tiene: "
            "el mapa completo de cómo funciona tu mente. "
            "¡Úsalo bien!"
        ),
        "criatura_asignada": (
            "Hay Pokémon que esperan al entrenador adecuado. "
            "El tuyo ha dejado de esperar. "
            "Lo que construyáis juntos depende de lo que tú decidas hacer con esto."
        ),
        "modulo_recursos": (
            "Las batallas más complejas no son físicas. "
            "Aquí tienes todas las entradas de la Pokédex para entrenar la parte "
            "que ningún gimnasio enseña: conocerte y saber lo que necesitas."
        ),
    },
    4: {  # Studio Ghibli
        "universo_elegido": (
            "El viento te ha traído hasta aquí. "
            "En los mundos de Miyazaki nada ocurre por casualidad, "
            "has elegido bien."
        ),
        "perfil_completado": (
            "Los espíritus del bosque reconocen a quienes se conocen a sí mismos. "
            "Tu perfil es un reflejo tranquilo, como el agua antes de que sople el viento. "
            "Mírate en él sin prisa."
        ),
        "criatura_asignada": (
            "Las criaturas de Ghibli no aparecen ante cualquiera. "
            "La tuya ha decidido acompañarte, "
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
            "No todos los vikingos luchan igual, y eso está bien. "
            "Hipo cambió su mundo entendiéndolo primero. "
            "Tú también puedes."
        ),
        "perfil_completado": (
            "Un buen vikingo conoce sus fuerzas y sus límites. "
            "Tu perfil no es una debilidad, es inteligencia táctica. "
            "Los mejores jinetes de dragón saben que conocerse es el primer paso del camino."
        ),
        "criatura_asignada": (
            "Los dragones no se doman, te ganas su confianza. "
            "Tu criatura te la ha dado. "
            "Eso no se consigue con fuerza, sino con presencia."
        ),
        "modulo_recursos": (
            "En Isla Mema, el Libro de los Dragones contenía todo lo que creían saber. "
            "Cuando descubrieron de verdad lo que había en los dragones, "
            "ese libro se enriqueció para siempre. "
            "Aquí tienes las primeras páginas para el tuyo."
        ),
    },
    6: {  # Disney/Pixar
        "universo_elegido": (
            "Cada historia de Disney empieza con un momento de verdad. "
            "Un instante en el que el personaje deja de huir, se mira al espejo "
            "y decide ser honesto consigo mismo. "
            "Es incómodo, da miedo, pero ahí empieza la magia. "
            "Acabas de iniciar un nuevo capítulo en tu historia "
            "en la que solo tú eres el protagonista."
        ),
        "perfil_completado": (
            "Inside Out nos enseñó que todas las emociones tienen su lugar. "
            "Tu perfil hace lo mismo: no juzga cómo funciona tu mente, la mapea. "
            "Y un mapa nunca está mal, solo te dice dónde estás."
        ),
        "criatura_asignada": (
            "La magia Disney no está en los castillos, "
            "nace cuando dos seres se conocen y se reconocen. "
            "Tu criatura te ha reconocido. "
            "Eso no es casualidad, es el inicio de algo real."
        ),
        "modulo_recursos": (
            "En la cabeza de Riley, cada recuerdo y cada herramienta tenía su estantería. "
            "Aquí tienes las tuyas. "
            "Estos recursos no son magia, "
            "son el trabajo real que hace posible que la magia ocurra."
        ),
    },
}


def get_narrador(universo_id: int, momento: str) -> str:
    """
    Devuelve el texto narrativo para un universo y momento dados.

    momentos: universo_elegido | perfil_completado | criatura_asignada | modulo_recursos
    """
    return NARRADOR.get(universo_id, {}).get(momento, "")
