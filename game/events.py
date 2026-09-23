import random


EVENTS = [
    {
        "id": "eclipse",
        "name": "🌑 ECLIPSE",
        "description": "La energía mundial cae lentamente.",
        "effects": {
            "world_energy": -2
        }
    },
    {
        "id": "overload",
        "name": "⚡ SOBRECARGA",
        "description": "Las acciones energéticas son más poderosas.",
        "effects": {
            "protect_score": 2
        }
    },
    {
        "id": "distortion",
        "name": "🌀 DISTORSIÓN",
        "description": "El caos aumenta mucho más.",
        "effects": {
            "chaos_multiplier": 2
        }
    },
    {
        "id": "fragments",
        "name": "💎 LLUVIA DE FRAGMENTOS",
        "description": "Explorar produce muchos más fragmentos.",
        "effects": {
            "explore_fragments": 3
        }
    },
    {
        "id": "chaos_fever",
        "name": "🔥 FIEBRE DEL CAOS",
        "description": "Sabotear proporciona recompensas adicionales.",
        "effects": {
            "sabotage_bonus": 30
        }
    },
    {
        "id": "rebirth",
        "name": "🌱 RENACIMIENTO",
        "description": "El mundo recupera energía.",
        "effects": {
            "protect_world": 2
        }
    },
    {
        "id": "observer",
        "name": "👁️ EL OBSERVADOR",
        "description": "Algunas acciones pueden tener resultados imprevisibles.",
        "effects": {
            "mutation_random": True
        }
    },
    {
        "id": "nothing",
        "name": "🌌 NADA",
        "description": "Nadie sabe qué ocurrirá durante esta ronda.",
        "effects": {}
    }
]


def random_event():
    """
    Selecciona un evento aleatorio.
    """

    return random.choice(EVENTS)


def get_event(event_id):
    """
    Busca un evento por su ID.
    """

    for event in EVENTS:

        if event["id"] == event_id:
            return event

    return None


def event_name(event_id):
    """
    Devuelve solamente el nombre del evento.
    """

    event = get_event(event_id)

    if not event:
        return "🌌 NADA"

    return event["name"]


def event_description(event_id):
    """
    Devuelve la descripción del evento.
    """

    event = get_event(event_id)

    if not event:
        return "No hay ningún evento activo."

    return event["description"]
