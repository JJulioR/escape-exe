from flask import Flask, render_template, session ,request, jsonify
from game.ai_narrator import generate_room_description
import requests
import random
import string

app = Flask(__name__)
app.secret_key = "escape_exe_secret"



from game.rooms import ROOMS
# Commandes disponibles affichées avec "help"
HELP_TEXT = """AVAILABLE COMMANDS:
'LOOK' — examine your surroundings\n
'GO [direction]' — move in a direction (north, south, east, west)\n
'TAKE [item]' — pick up an item\n
'USE [item]' — use an item\n
'EXAMINE [item]' — examine an item in your inventory\n
'HINT' — get a hint for the current puzzle\n
'INVENTORY' — check your inventory\n
'HELP' — show this message\n
"""
# Génère un ID 
def generate_player_id():
    chars = string.ascii_uppercase + string.digits
    return "ESC-" + "".join(random.choices(chars, k=4))

# Route pour enregistrer le pseudo du joueur
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username", "Anonymous").strip()
    
    # pseudo à 20 char max
    username = username[:20] if username else "Anonymous"
    
    # crée ID unique
    player_id = generate_player_id()
    
    # Stocke dans la sess
    session["username"] = username
    session["player_id"] = player_id
    session["seconds"] = 0
    
    return jsonify({
        "player_id": player_id,
        "username": username
    })

@app.route("/")
def index():
    return render_template("index.html")

# Route qui reçoit les commandes du joueur depuis JS
@app.route("/command", methods=["POST"])
def command():
    # Récupère la commande envoyée par JS
    data = request.get_json()
    cmd = data.get("command", "").strip().lower()
    session["seconds"] = data.get("seconds", 0)  # Met à jour le temps écoulé
    session.modified = True  # Indique que la session a été modifiée pour s'assurer que les changements sont sauvegardés !!!

    # Initialise la session du joueur si c sa première commande
    if "room" not in session or "room_items" not in session:
        session["room"] = "server_room"       # Salle de départ c'est la salle serveur
        session["inventory"] = []       # Inventaire vide
        session["puzzles"]= {
            r: False for r in ROOMS if ROOMS[r]["puzzle"]
        }  # Dictionnaire pour suivre les énigmes résolues

        # Copie les items de chaque salle en session
        # pour éviter de modifier ROOMS globalement
        session["room_items"] = {
            room_id: list(room_data["items"])
            for room_id, room_data in ROOMS.items()
        }

    # Traite commande et retourne  réponse
    response = handle_command(cmd)
    return jsonify({"message": response})

#logiQ de commandes

def handle_command(cmd):
    #Traite la commande du joueur et retourne un message
    room_id = session.get("room", "server_room")
    room = ROOMS[room_id]
    room_items = session["room_items"][room_id] 

    # Commande : START
    if cmd == "start":
        session["room"] = "server_room"
        session["inventory"] = []
        session["puzzles"]= {r: False for r in ROOMS if ROOMS[r]["puzzle"]}
        session["room_items"] = {
            room_id: list(room_data["items"])
            for room_id, room_data in ROOMS.items()
        }
        session.modified = True
        return generate_room_description("server_room", session["room_items"]["server_room"], "Game just started")

    # Commande : HELP
    elif cmd == "help":
        return HELP_TEXT

    # Commande : look — décrit la salle actuelle
    elif cmd == "look":
        return generate_room_description(room_id, room_items)

    # Commande : INVENTORY
    elif cmd == "inventory":
        inv = session.get("inventory", [])
        if not inv:
            return "Your inventory is empty."
        return "INVENTORY: " + ", ".join(inv)
    
    # Commande : HINT
    elif cmd == "hint":
        puzzle = room.get("puzzle")
        if not puzzle:
            return "There is no puzzle in this room...Or maybe you already solved it?"
        return "HINT: " + puzzle["hint"]
    
    # Commande TAKE [item]
    elif cmd.startswith("take "):
        item = cmd[5:].strip().replace(" ", "_") # (ex: "take access card" → "access_card")
        if item in room_items:
            session["inventory"] = session.get("inventory", []) + [item] 
            session["room_items"][room_id].remove(item)  # retire de la session
            session.modified = True
            return f"You have the {item.replace('_', ' ')}."
        return f"There is no {item.replace('_', ' ')} here."
    
    # Commande EXAMINE [item]
    elif cmd.startswith("examine "):
        item = cmd[8:].strip().replace(" ", "_")
        if item in session.get("inventory", []) or item in room_items:
            return generate_room_description(room_id, [item],f"You examine the {item.replace('_', ' ')}. It looks ordinary... but maybe it has a hidden use?")
        return f"There is no {item.replace('_', ' ')} here."
    
    # Commande USE [item]
    elif cmd.startswith("use "):
        item = cmd[4:].strip().replace(" ", "_")
        return handle_use(item, room_id, room)
    
     #CODE [answer] pour  énigme  type code
    elif cmd.startswith("code "):
        answer = cmd[5:].strip()
        return handle_code(answer, room_id, room)
    
    # Commande : GO [direction]
    elif cmd.startswith("go "):
        direction = cmd[3:].strip() # Extrait la direction (ex: "go north" → "north")
        return handle_movement(direction, room_id, room)
    
    # Essaie de traiter comme un code direct si rien d'autre ne correspond
    elif cmd.isdigit() or (len(cmd) <= 10 and " " not in cmd and cmd not in ["look", "inventory", "examine", "hint", "help", "start"]):
     return handle_code(cmd, room_id, room)


    # Commande inconnue
    else:
        return "Unknown command. Type 'help' for available commands."
    
def handle_use(item, room_id, room):
    #Gère la commande USE — utiliser un objet sur une énigme
    inventory = session.get("inventory", [])

    # Vérifie si joueur a l'objet
    if item not in inventory:
        return f"You don't have a {item.replace('_', ' ')} in your inventory."

    puzzle = room.get("puzzle")

    # Vérifie s'il y a une énigme type 'item
    if puzzle and puzzle["type"] == "item" and not session["puzzles"].get(room_id):
        if item == puzzle["answer"]:
            # Marque l'énigme comme résolue
            session["puzzles"][room_id] = True
            session.modified = True  # Indique que la session a été modifiée pour s'assurer que les changements sont sauvegardés !!!
            return puzzle["reward"]
        else:
            return f"You use the {item.replace('_', ' ')} but nothing happens."

    return f"You use the {item.replace('_', ' ')} but nothing happens."

def handle_code(answer, room_id, room):
    #Gère la commande CODE — entrer un code pour résoudre une énigme
    puzzle = room.get("puzzle")

    if not puzzle or puzzle["type"] != "code":
        return "There is no keypad or code input here."

    if session["puzzles"].get(room_id):
        return "You already solved the puzzle in this room."

    if answer == puzzle["answer"]:
        session["puzzles"][room_id] = True
        session.modified = True  # Indique que la session a été modifiée pour s'assurer que les changements sont sauvegardés !!!
        return puzzle["reward"]
    else:
        return "Wrong code. Try again."
    
def handle_movement(direction, room_id, room):
    #gère la commande GO — déplacer le joueur
    exits = room.get("exits", {})

    if direction not in exits:
        return "You can't go that way."

    next_room_id = exits[direction]

    # Vérifie si la salle suivante nécessite un puzzle résolu
    locked_paths = {
        ("server_room", "north"): "server_room",
        ("corridor", "north"): "corridor"
    }

    lock_key = (room_id, direction)
    if lock_key in locked_paths:
        required_room = locked_paths[lock_key]
        if not session["puzzles"].get(required_room):
            puzzle = ROOMS[required_room].get("puzzle")
            hint = puzzle["hint"] if puzzle else ""
            return f"The way is blocked. {hint}"
    
    # Déplace le joueur
    session["room"] = next_room_id

    # Vérifie si c'est la sortie (victoire !)
    if next_room_id == "exit":
        username = session.get("username", "Anonymus")
        player_id = session.get("player_id", "???")
        time_seconds = session.get("seconds", 0)

        try :
          requests.post("https://jrinvil.com/escape_exe/scores.php", json={
            "player_id": player_id,
            "username": username,
            "time_seconds": time_seconds
        })
        except:
         pass
    
        return "🎉 SYSTEM BREACH COMPLETE. You escaped! Congratulations!"

    # Génère une description IA de la nouvelle salle
    room_items = session["room_items"][next_room_id]
    return generate_room_description(next_room_id, room_items, "Player just entered")


if __name__ == "__main__":
    app.run(debug=True)

@app.route("/reset")
def reset():
    session.clear()
    return "Session cleared! You can go back to the page to start a new game."
