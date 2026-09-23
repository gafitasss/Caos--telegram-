import random

from game.events import get_event


ACTIONS = {
    "explore": {
        "name": "🧭 EXPLORAR",
        "cost": 10
    },
    "protect": {
        "name": "🛡️ PROTEGER",
        "cost": 8
    },
    "sabotage": {
        "name": "💥 SABOTEAR",
        "cost": 12
    },
    "mutate": {
        "name": "🧬 MUTAR",
        "cost": 20
    }
}


def resolve_action(action, event_id):
    """
    Resuelve una acción del jugador.

    Devuelve:

    energy
    fragments
    score
    world
    chaos
    message
    """

    event = get_event(event_id)

    if not event:

        event_id = "nothing"
        event = get_event(event_id)

    if action not in ACTIONS:

        return {
            "energy": 0,
            "fragments": 0,
            "score": 0,
            "world": 0,
            "chaos": 0,
            "message": "❓ Acción desconocida."
        }

    # ==========================================
    # EXPLORAR
    # ==========================================

    if action == "explore":

        cost = ACTIONS[action]["cost"]

        fragments = random.randint(1, 8)

        score = fragments * 5

        world = random.randint(-2, 0)

        chaos = random.randint(0, 4)

        # Lluvia de fragmentos

        if event_id == "fragments":

            fragments *= 3
            score *= 2

        # El Observador

        if event_id == "observer":

            if random.random() < 0.20:

                fragments *= 5
                score *= 3

        return {
            "energy": -cost,
            "fragments": fragments,
            "score": score,
            "world": world,
            "chaos": chaos,
            "message": (
                "🧭 *EXPEDICIÓN COMPLETADA*\n\n"
                f"💎 +{fragments} fragmentos\n"
                f"⭐ +{score} puntos\n"
                f"🔋 -{cost} energía"
            )
        }

    # ==========================================
    # PROTEGER
    # ==========================================

    if action == "protect":

        cost = ACTIONS[action]["cost"]

        score = 15

        world = random.randint(4, 10)

        chaos = -random.randint(1, 5)

        # Renacimiento

        if event_id == "rebirth":

            world *= 2

        # Sobrecarga

        if event_id == "overload":

            score *= 2

        return {
            "energy": -cost,
            "fragments": 0,
            "score": score,
            "world": world,
            "chaos": chaos,
            "message": (
                "🛡️ *DEFENSA ACTIVADA*\n\n"
                f"🌍 +{world} energía mundial\n"
                f"⭐ +{score} puntos\n"
                f"🌀 {chaos} caos\n"
                f"🔋 -{cost} energía"
            )
        }

    # ==========================================
    # SABOTEAR
    # ==========================================

    if action == "sabotage":

        cost = ACTIONS[action]["cost"]

        fragments = random.randint(2, 6)

        score = fragments * 7

        world = -random.randint(5, 12)

        chaos = random.randint(8, 16)

        # Fiebre del Caos

        if event_id == "chaos_fever":

            fragments += 5

            score += 30

        # Distorsión

        if event_id == "distortion":

            chaos *= 2

        return {
            "energy": -cost,
            "fragments": fragments,
            "score": score,
            "world": world,
            "chaos": chaos,
            "message": (
                "💥 *SABOTAJE COMPLETADO*\n\n"
                f"💎 +{fragments} fragmentos\n"
                f"⭐ +{score} puntos\n"
                f"🌍 {world} energía mundial\n"
                f"🌀 +{chaos} caos\n"
                f"🔋 -{cost} energía"
            )
        }

    # ==========================================
    # MUTAR
    # ==========================================

    if action == "mutate":

        cost = ACTIONS[action]["cost"]

        roll = random.randint(1, 100)

        # El Observador altera la probabilidad

        if event_id == "observer":

            roll = random.randint(1, 120)

        # MUTACIÓN ESTABLE

        if roll <= 40:

            score = 80

            fragments = random.randint(5, 12)

            message = (
                "🧬 *MUTACIÓN ESTABLE*\n\n"
                f"💎 +{fragments} fragmentos\n"
                f"⭐ +{score} puntos"
            )

        # MUTACIÓN INESTABLE

        elif roll <= 80:

            score = 20

            fragments = 1

            message = (
                "🧬 *MUTACIÓN INESTABLE*\n\n"
                "💎 +1 fragmento\n"
                f"⭐ +{score} puntos"
            )

        # MUTACIÓN FALLIDA

        else:

            score = -20

            fragments = 0

            message = (
                "☠️ *MUTACIÓN FALLIDA*\n\n"
                f"⭐ {score} puntos"
            )

        return {
            "energy": -cost,
            "fragments": fragments,
            "score": score,
            "world": random.randint(-8, 8),
            "chaos": random.randint(-5, 15),
            "message": message
        }


def action_name(action):
    """
    Devuelve el nombre visible de una acción.
    """

    action_data = ACTIONS.get(action)

    if not action_data:

        return "❓ DESCONOCIDA"

    return action_data["name"]


def action_cost(action):
    """
    Devuelve el coste energético.
    """

    action_data = ACTIONS.get(action)

    if not action_data:

        return 0

    return action_data["cost"]
