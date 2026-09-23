
def __init__(self, db):  

    self.db = db  

# ==========================================  
# JUGADORES  
# ==========================================  

def register(self, user):  

    name = (  
        user.first_name  
        or user.username  
        or "Jugador"  
    )  

    username = user.username or ""  

    self.db.create_player(  
        user.id,  
        username,  
        name  
    )  

def join(self, chat_id, user):  

    self.register(user)  

    self.db.create_group(  
        chat_id  
    )  

    self.db.join_group(  
        chat_id,  
        user.id  
    )  

# ==========================================  
# RONDAS  
# ==========================================  

def start_round(self, chat_id):  

    self.db.create_group(  
        chat_id  
    )  

    group = self.db.get_group(  
        chat_id  
    )  

    # Evitar iniciar dos rondas  
    # simultáneamente  

    if round_active(group):  

        return {  
            "success": False,  
            "message": (  
                "⚡ Ya hay una ronda activa."  
            )  
        }  

    event = random_event()  

    result = start_round(  
        self.db,  
        chat_id,  
        event  
    )  

    if not result:  

        return {  
            "success": False,  
            "message": (  
                "❌ No se pudo iniciar "  
                "la ronda."  
            )  
        }  

    return {  
        "success": True,  
        "round": result["round"],  
        "event": event,  
        "ends": result["ends"]  
    }  

# ==========================================  
# ACCIONES  
# ==========================================  

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

        return {  
            "success": False,  
            "message": (  
                "❌ No existe la partida."  
            )  
        }  

    # --------------------------------------  
    # COMPROBAR RONDA  
    # --------------------------------------  

    if not round_active(group):  

        return {  
            "success": False,  
            "message": (  
                "⏰ La ronda ha terminado."  
            )  
        }  

    # --------------------------------------  
    # COMPROBAR ACCIÓN REPETIDA  
    # --------------------------------------  

    if self.db.action_exists(  
        chat_id,  
        group["round"],  
        user.id  
    ):  

        return {  
            "success": False,  
            "message": (  
                "⏳ Ya has realizado "  
                "tu acción en esta ronda."  
            )  
        }  

    # --------------------------------------  
    # COMPROBAR JUGADOR  
    # --------------------------------------  

    player = self.db.get_player(  
        user.id  
    )  

    if not player:  

        return {  
            "success": False,  
            "message": (  
                "❌ No estás registrado."  
            )  
        }  

    # --------------------------------------  
    # COMPROBAR ENERGÍA  
    # --------------------------------------  

    cost = action_cost(  
        action  
    )  

    if player["energy"] < cost:  

        return {  
            "success": False,  
            "message": (  
                "🔋 No tienes suficiente "  
                "energía."  
            )  
        }  

    # --------------------------------------  
    # RESOLVER ACCIÓN  
    # --------------------------------------  

    result = resolve_action(  
        action,  
        group["event"]  
    )  

    # --------------------------------------  
    # GUARDAR ACCIÓN  
    # --------------------------------------  

    self.db.save_action(  
        chat_id,  
        group["round"],  
        user.id,  
        action  
    )  

    # --------------------------------------  
    # ACTUALIZAR JUGADOR  
    # --------------------------------------  

    self.db.update_player(  
        user.id,  
        energy_delta=result["energy"],  
        fragments_delta=result["fragments"],  
        score_delta=result["score"],  
        action_delta=1  
    )  

    # --------------------------------------  
    # ACTUALIZAR MUNDO  
    # --------------------------------------  

    world = apply_world_change(  
        self.db,  
        chat_id,  
        result["world"],  
        result["chaos"]  
    )  

    # --------------------------------------  
    # ESTADO DEL MUNDO  
    # --------------------------------------  

    updated_group = self.db.get_group(  
        chat_id  
    )  

    condition = check_world_condition(  
        updated_group  
    )  

    # --------------------------------------  
    # RESULTADO  
    # --------------------------------------  

    count = self.db.action_count(  
        chat_id,  
        group["round"]  
    )  

    return {  
        "success": True,  

        "message": result["message"],  

        "action": action,  

        "round": group["round"],  

        "actions": count,  

        "world": world,  

        "condition": condition,  

        "remaining": remaining_seconds(  
            updated_group  
        )  
    }  

# ==========================================  
# INFORMACIÓN DEL JUGADOR  
# ==========================================  

def status(self, user_id):  

    return self.db.get_player(  
        user_id  
    )  

# ==========================================  
# ESTADO DEL GRUPO  
# ==========================================  

def group_status(self, chat_id):  

    return self.db.get_group(  
        chat_id  
    )  

# ==========================================  
# RANKING  
# ==========================================  

def ranking(self, chat_id):  

    return self.db.ranking(  
        chat_id  
    )  

# ==========================================  
# JUGADORES DEL GRUPO  
# ==========================================  

def player_count(self, chat_id):  

    return self.db.group_player_count(  
        chat_id  
    )
