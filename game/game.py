import random
import time

EVENTS = [
(
"🌑 ECLIPSE",
"La energía mundial cae lentamente."
),
(
"⚡ SOBRECARGA",
"Las acciones energéticas son más poderosas."
),
(
"🌀 DISTORSIÓN",
"El caos aumenta mucho más."
),
(
"💎 LLUVIA DE FRAGMENTOS",
"Explorar produce más fragmentos."
),
(
"🔥 FIEBRE DEL CAOS",
"Sabotear proporciona recompensas adicionales."
),
(
"🌱 RENACIMIENTO",
"El mundo recupera energía."
),
(
"👁️ EL OBSERVADOR",
"El resultado de algunas acciones es imprevisible."
),
(
"🌌 NADA",
"Nadie sabe qué ocurrirá durante esta ronda."
)
]

class Game:

def __init__(self, db):  
    self.db = db  

# -------------------------  
# JUGADORES  
# -------------------------  

def register(self, user):  
    name = user.first_name or "Jugador"  
    username = user.username or ""  

    self.db.create_player(  
        user.id,  
        username,  
        name  
    )  

def join(self, chat_id, user):  
    self.register(user)  

    self.db.create_group(chat_id)  
    self.db.join_group(  
        chat_id,  
        user.id  
    )  

# -------------------------  
# RONDAS  
# -------------------------  

def start_round(self, chat_id):  

    self.db.create_group(chat_id)  

    event, description = random.choice(  
        EVENTS  
    )  

    now = int(time.time())  

    self.db.update_group(  
        chat_id,  
        event=event,  
        round_started=now,  
        round_ends=now + 60  
    )  

    return event, description  

# -------------------------  
# ACCIONES  
# -------------------------  

def perform_action(  
    self,  
    chat_id,  
    user,  
    action  
):  
    self.join(  
        chat_id,  
        user  
    )  

    group = self.db.get_group(  
        chat_id  
    )  

    if not group:  
        return False, "No existe ninguna partida."  

    round_number = group["round"]  

    # Una acción por ronda  
    if self.db.action_exists(  
        chat_id,  
        round_number,  
        user.id  
    ):  
        return (  
            False,  
            "⏳ Ya has actuado en esta ronda."  
        )  

    player = self.db.get_player(  
        user.id  
    )  

    if not player:  
        return (  
            False,  
            "❌ No estás registrado."  
        )  

    if player["energy"] <= 0:  
        return (  
            False,  
            "🔋 No tienes energía suficiente."  
        )  

    result = self.resolve_action(  
        action,  
        group["event"]  
    )  

    self.db.save_action(  
        chat_id,  
        round_number,  
        user.id,  
        action  
    )  

    self.db.update_player(  
        user.id,  
        energy_delta=result["energy"],  
        fragments_delta=result["fragments"],  
        score_delta=result["score"],  
        action_delta=1  
    )  

    self.db.update_group(  
        chat_id,  
        world_energy_delta=result["world"],  
        chaos_delta=result["chaos"]  
    )  

    count = self.db.action_count(  
        chat_id,  
        round_number  
    )  

    return True, (  
        result["message"],  
        count  
    )  

# -------------------------  
# RESULTADO DE UNA ACCIÓN  
# -------------------------  

def resolve_action(  
    self,  
    action,  
    event  
):  

    # =========================  
    # EXPLORAR  
    # =========================  

    if action == "explore":  

        cost = 10  

        fragments = random.randint(  
            1,  
            8  
        )  

        score = fragments * 5  

        world = random.randint(  
            -2,  
            0  
        )  

        chaos = random.randint(  
            0,  
            4  
        )  

        if event == "💎 LLUVIA DE FRAGMENTOS":  
            fragments *= 3  
            score *= 2  

        if event == "👁️ EL OBSERVADOR":  

            if random.random() < 0.20:  
                fragments *= 5  
                score *= 3  

        return {  
            "energy": -cost,  
            "fragments": fragments,  
            "score": score,  
            "world": world,  
            "chaos": chaos,  
            "message":  
                "🧭 *EXPEDICIÓN COMPLETADA*\n\n"  
                f"💎 +{fragments} fragmentos\n"  
                f"⭐ +{score} puntos\n"  
                f"🔋 -{cost} energía"  
        }  

    # =========================  
    # PROTEGER  
    # =========================  

    if action == "protect":  

        cost = 8  

        score = 15  

        world = random.randint(  
            4,  
            10  
        )  

        chaos = -random.randint(  
            1,  
            5  
        )  

        if event == "🌱 RENACIMIENTO":  
            world *= 2  

        if event == "⚡ SOBRECARGA":  
            score *= 2  

        return {  
            "energy": -cost,  
            "fragments": 0,  
            "score": score,  
            "world": world,  
            "chaos": chaos,  
            "message":  
                "🛡️ *DEFENSA ACTIVADA*\n\n"  
                f"🌍 +{world} energía mundial\n"  
                f"⭐ +{score} puntos\n"  
                f"🌀 {chaos} caos\n"  
                f"🔋 -{cost} energía"  
        }  

    # =========================  
    # SABOTEAR  
    # =========================  

    if action == "sabotage":  

        cost = 12  

        fragments = random.randint(  
            2,  
            6  
        )  

        score = fragments * 7  

        world = -random.randint(  
            5,  
            12  
        )  

        chaos = random.randint(  
            8,  
            16  
        )  

        if event == "🔥 FIEBRE DEL CAOS":  
            fragments += 5  
            score += 30  

        if event == "🌀 DISTORSIÓN":  
            chaos *= 2  

        return {  
            "energy": -cost,  
            "fragments": fragments,  
            "score": score,  
            "world": world,  
            "chaos": chaos,  
            "message":  
                "💥 *SABOTAJE COMPLETADO*\n\n"  
                f"💎 +{fragments} fragmentos\n"  
                f"⭐ +{score} puntos\n"  
                f"🌍 {world} energía mundial\n"  
                f"🌀 +{chaos} caos\n"  
                f"🔋 -{cost} energía"  
        }  

    # =========================  
    # MUTAR  
    # =========================  

    if action == "mutate":  

        cost = 20  

        roll = random.randint(  
            1,  
            100  
        )  

        if event == "👁️ EL OBSERVADOR":  

            roll = random.randint(  
                1,  
                120  
            )  

        if roll <= 40:  

            score = 80  

            fragments = random.randint(  
                5,  
                12  
            )  

            message = (  
                "🧬 *MUTACIÓN ESTABLE*\n\n"  
                f"💎 +{fragments} fragmentos\n"  
                f"⭐ +{score} puntos"  
            )  

        elif roll <= 80:  

            score = 20  

            fragments = 1  

            message = (  
                "🧬 *MUTACIÓN INESTABLE*\n\n"  
                "💎 +1 fragmento\n"  
                f"⭐ +{score} puntos"  
            )  

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
            "world": random.randint(  
                -8,  
                8  
            ),  
            "chaos": random.randint(  
                -5,  
                15  
            ),  
            "message": message  
        }  

    # =========================  
    # ACCIÓN DESCONOCIDA  
    # =========================  

    return {  
        "energy": 0,  
        "fragments": 0,  
        "score": 0,  
        "world": 0,  
        "chaos": 0,  
        "message":  
            "❓ Acción desconocida."  
    }  

# -------------------------  
# INFORMACIÓN  
# -------------------------  

def status(self, user_id):  
    return self.db.get_player(  
        user_id  
    )  

def group_status(self, chat_id):  
    return self.db.get_group(  
        chat_id  
    )  

def ranking(self, chat_id):  
    return self.db.ranking(  
        chat_id  
    )
