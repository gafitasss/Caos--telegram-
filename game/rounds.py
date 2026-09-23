import time


ROUND_DURATION = 60

WORLD_MIN = 0
WORLD_MAX = 100

CHAOS_MIN = 0
CHAOS_MAX = 100


def start_round(db, chat_id, event):
    """
    Inicia una nueva ronda para un grupo.
    """

    now = int(time.time())

    group = db.get_group(chat_id)

    if not group:
        return None

    round_number = group["round"] + 1

    db.update_group(
        chat_id,
        round=round_number,
        event=event["id"],
        round_started=now,
        round_ends=now + ROUND_DURATION
    )

    return {
        "round": round_number,
        "event": event,
        "started": now,
        "ends": now + ROUND_DURATION
    }


def round_active(group):
    """
    Comprueba si la ronda sigue activa.
    """

    if not group:
        return False

    ends = group.get("round_ends", 0)

    return int(time.time()) < ends


def remaining_seconds(group):
    """
    Devuelve los segundos que quedan.
    """

    if not group:
        return 0

    remaining = group.get("round_ends", 0) - int(time.time())

    return max(0, remaining)


def clamp_world(value):
    """
    Mantiene la energía mundial entre 0 y 100.
    """

    return max(
        WORLD_MIN,
        min(WORLD_MAX, value)
    )


def clamp_chaos(value):
    """
    Mantiene el caos entre 0 y 100.
    """

    return max(
        CHAOS_MIN,
        min(CHAOS_MAX, value)
    )


def apply_world_change(
    db,
    chat_id,
    world_delta=0,
    chaos_delta=0
):
    """
    Aplica los cambios producidos
    por las acciones de los jugadores.
    """

    group = db.get_group(chat_id)

    if not group:
        return None

    current_world = group.get(
        "world_energy",
        50
    )

    current_chaos = group.get(
        "chaos",
        0
    )

    new_world = clamp_world(
        current_world + world_delta
    )

    new_chaos = clamp_chaos(
        current_chaos + chaos_delta
    )

    db.update_group(
        chat_id,
        world_energy=new_world,
        chaos=new_chaos
    )

    return {
        "world_energy": new_world,
        "chaos": new_chaos
    }


def world_state(group):
    """
    Devuelve una descripción visual
    del estado actual del mundo.
    """

    if not group:
        return "🌌 Mundo desconocido."

    world = group.get(
        "world_energy",
        50
    )

    chaos = group.get(
        "chaos",
        0
    )

    # Estado de energía mundial

    if world <= 15:
        world_status = "☠️ COLAPSO"

    elif world <= 30:
        world_status = "🔴 CRÍTICO"

    elif world <= 50:
        world_status = "🟠 INESTABLE"

    elif world <= 75:
        world_status = "🟢 ESTABLE"

    else:
        world_status = "🌟 FLORECIENTE"

    # Estado del caos

    if chaos >= 85:
        chaos_status = "☠️ ABSOLUTO"

    elif chaos >= 65:
        chaos_status = "🔥 EXTREMO"

    elif chaos >= 40:
        chaos_status = "🌀 ALTO"

    elif chaos >= 20:
        chaos_status = "⚠️ MODERADO"

    else:
        chaos_status = "😴 BAJO"

    return (
        f"🌍 Energía mundial: {world}/100\n"
        f"{world_status}\n\n"
        f"🌀 Caos: {chaos}/100\n"
        f"{chaos_status}"
    )


def check_world_condition(group):
    """
    Comprueba si el mundo ha alcanzado
    una condición especial.
    """

    if not group:
        return None

    world = group.get(
        "world_energy",
        50
    )

    chaos = group.get(
        "chaos",
        0
    )

    # COLAPSO

    if world <= 0:

        return {
            "type": "collapse",
            "message": (
                "☠️ *EL MUNDO HA COLAPSADO*\n\n"
                "La energía mundial ha llegado a cero."
            )
        }

    # RENACIMIENTO

    if world >= 100:

        return {
            "type": "rebirth",
            "message": (
                "🌟 *RENACIMIENTO MUNDIAL*\n\n"
                "La energía mundial ha alcanzado su máximo."
            )
        }

    # CAOS ABSOLUTO

    if chaos >= 100:

        return {
            "type": "chaos",
            "message": (
                "🌀 *CAOS ABSOLUTO*\n\n"
                "El caos ha escapado completamente de control."
            )
        }

    return None
