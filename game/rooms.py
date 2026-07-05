# Dictionnaire avec toutes les salles du jeu
# Chaque salle a : une descpt, des sorties possible et des objet
ROOMS = {
    "server_room": {
        "description": "You wake up in a dark server room. Machines hum around you. There is a DOOR to the north and a KEYPAD on the wall.",
        "exits": {"north": "corridor"},
        "items": ["keypad", "broken_screen", "access_card"],
        "puzzle": {
            "type": "code",                          # Type
            "answer": "1984",                        # Réponse 
            "hint": "The broken screen flickers... you can barely read: 'Favorite book by George Orwell.'",  # Indice
            "solved": False,                        
            "reward": "The door to the north clicks open."  # Message si résolu
        }
    },
    "corridor": {
        "description": "A long corridor. Emergency lights flicker above. There is a LOCKED DOOR to the north and a VENT on the floor.",
        "exits": {"south": "server_room", "north": "lab"},  # 'lab' bloqué au départ
        "items": ["locked_door", "vent", "torn_note"],
        "puzzle": {
            "type": "item",                          # Type d'énigme : utiliser un objet
            "answer": "access_card",                 # Objet à utiliser
            "hint": "The locked door has a card reader.",
            "solved": False,
            "reward": "The door slides open. You can now go north."
        }
    },
    "lab": {
        "description": "An abandoned laboratory. Chemical smell fills the air.",
        "exits": {"south": "corridor", "north": "exit"},
        "items": ["computer", "lab_notes", "strange_vial"],
        "puzzle": {
            "type": "code",
            "answer": "dna",                         # Mot à trouver
            "hint": "The lab notes mention the master password is the building block of life.",
            "solved": False,
            "reward": "The computer unlocks. The exit door opens!"
        }
    },
    "exit": {
        "description": "You see the exit. Freedom is close.",
        "exits": {},
        "items": [],
        "puzzle": None                               # Pas d'énigme, c'est la fin !
    }
}

ITEM_DESCRIPTIONS = {
    "torn_note": "A torn piece of paper. You can barely read: 'The answer is in our DNA... literally.'",
    "broken_screen": "A cracked monitor. Through the static you can make out: 'Favorite book by George Orwell.'",
    "strange_vial": "A vial filled with a glowing blue liquid. The label reads: 'Sample X-19 — DO NOT OPEN'.",
    "access_card": "A security access card. Name: Dr. Chen. Level 3 clearance.",
    "lab_notes": "Scattered research notes. One page reads: 'Master password = building block of life'.",
    "keypad": "A numeric keypad on the wall. It's waiting for a 4-digit code.",
    "computer": "An old computer. The login screen asks for a password.",
    "locked_door": "A heavy door with a card reader. It won't budge without the right card.",
    "vent": "A metal vent on the floor. It's sealed shut."
}