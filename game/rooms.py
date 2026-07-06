# Dictionnaire avec toutes les salles du jeu
# Chaque salle a : une descpt, des sorties possible et des objet
ROOMS = {
    #START
    "server_room": {
        "description": (
            "You wake up on a cold metal floor. The room hums with the sound of servers. "
            "Rows of blinking machines surround you. A KEYPAD glows on the north wall beside a locked DOOR. "
            "A BROKEN SCREEN flickers in the corner. Something is written on the floor — an ACCESS CARD lies near your feet. "
            "The only way out is NORTH."
        ),
        "exits": {"north": "corridor"},
        "items": ["keypad", "broken_screen", "access_card"],
        "puzzle": {
            "type": "code",
            "answer": "1984",
            "hint": "The KEYPAD is waiting for a 4-digit code. The BROKEN SCREEN is flickering — have you tried to EXAMINE it?",
            "solved": False,
            "reward": "The door to the north clicks open. Cold air rushes in."
        }
    },

    #COULOIR
    "corridor": {
        "description": (
            "A long corridor stretches before you. Emergency red lights flicker above. "
            "A heavy LOCKED DOOR blocks the way NORTH. A VENT hums on the floor to your left. "
            "A TORN NOTE lies crumpled against the wall. "
            "You came from the SOUTH."
        ),
        "exits": {"south": "server_room", "north": "lab", "east": "storage_room"},
        "items": ["locked_door", "vent", "torn_note"],
        "puzzle": {
            "type": "item",
            "answer": "access_card",
            "hint": "The LOCKED DOOR has a card reader on it. There was an ACCESS CARD earlier — did you TAKE it? Check your INVENTORY.",
            "solved": False,
            "reward": "The door slides open with a hiss. You can now go NORTH or EAST."
        }
    },

    #ENTREPOT

    "storage_room": {
        "description": (
            "A dusty storage room. Metal shelves line the walls, stacked with old equipment. "
            "A FUSE BOX hangs open on the east wall — wires hang loose. "
            "A TOOLBOX sits on the floor. A LOGBOOK rests on a shelf. "
            "The corridor is back to the WEST. A door to the NORTH is sealed with an electronic lock."
        ),
        "exits": {"west": "corridor", "north": "security_office"},
        "items": ["fuse_box", "toolbox", "logbook"],
        "puzzle": {
            "type": "code",
            "answer": "fix",
            "hint": "The electronic lock on the NORTH door has no power. The FUSE BOX is open — have you tried to EXAMINE it? Maybe the TOOLBOX has something useful.",
            "solved": False,
            "reward": "The fuse box sparks. Power restored. The north door unlocks."
        }
    },

    #BUREAU SECU
    "security_office": {
        "description": (
            "A small security office. Monitors line the desk, most of them dead. "
            "One screen still shows a grainy camera feed of the LAB to the west. "
            "A KEYCARD READER blinks red on the wall. A DRAWER is slightly open. "
            "A GUN HOLSTER hangs empty on a hook — whoever was here left in a hurry. "
            "The storage room is SOUTH. The lab is to the WEST."
        ),
        "exits": {"south": "storage_room", "west": "lab"},
        "items": ["monitor", "drawer", "holster"],
        "puzzle": {
            "type": "code",
            "answer": "0451",
            "hint": "The KEYCARD READER needs a PIN. Security offices usually keep codes nearby — have you checked the DRAWER?",
            "solved": False,
            "reward": "Access granted. A hidden panel slides open revealing a MASTER KEYCARD."
        }
    },

    #LAB
    "lab": {
        "description": (
            "An abandoned laboratory. The smell of chemicals fills the air. "
            "A COMPUTER hums in the corner, its login screen glowing. "
            "LAB NOTES are scattered across a desk. A STRANGE VIAL sits in a rack beside them. "
            "A reinforced door leads NORTH toward the reactor. "
            "The corridor is SOUTH, the security office is EAST."
        ),
        "exits": {"south": "corridor", "east": "security_office", "north": "reactor_room"},
        "items": ["computer", "lab_notes", "strange_vial"],
        "puzzle": {
            "type": "code",
            "answer": "dna",
            "hint": "The COMPUTER needs a password. It's a science lab — have you EXAMINED the LAB NOTES on the desk?",
            "solved": False,
            "reward": "The computer unlocks. A file opens: REACTOR OVERRIDE CODE — 7734. The north door clicks open."
        }
    },

    #SALLE REACTEUR
    "reactor_room": {
        "description": (
            "A massive room. A reactor core pulses with dim blue light at the center. "
            "WARNING signs cover every surface. A CONTROL PANEL with dozens of switches lines the west wall. "
            "A RADIATION SUIT hangs near the entrance. A KEYPAD beside the north door awaits a code. "
            "The lab is SOUTH."
        ),
        "exits": {"south": "lab", "north": "control_room"},
        "items": ["control_panel", "radiation_suit", "warning_sign"],
        "puzzle": {
            "type": "code",
            "answer": "7734",
            "hint": "The KEYPAD needs a code. You've been in this facility a while — have you been reading everything you find? Check your INVENTORY for any notes.",
            "solved": False,
            "reward": "REACTOR OVERRIDE ACCEPTED. The north door unlocks with a deep clunk."
        }
    },

    #SALLE DE CNTRL
    "control_room": {
        "description": (
            "The main control room. Banks of switches and screens fill the space. "
            "Most systems are offline. An EMERGENCY BROADCAST plays on a loop from a RADIO in the corner. "
            "A SAFE is built into the wall — its combination dial untouched. "
            "A CLIPBOARD hangs beside it. "
            "The reactor is SOUTH. A ventilation access hatch is to the EAST."
        ),
        "exits": {"south": "reactor_room", "east": "ventilation_shaft"},
        "items": ["radio", "safe", "clipboard"],
        "puzzle": {
            "type": "code",
            "answer": "left42right17left8",
            "hint": "The SAFE has a combination lock. Combination safes use left-right sequences — have you EXAMINED the CLIPBOARD hanging beside it?",
            "solved": False,
            "reward": "The safe swings open. Inside: a FACILITY MAP and an EMERGENCY KEY."
        }
    },

    #CONDUIT DE VENT
    "ventilation_shaft": {
        "description": (
            "You crawl into a narrow ventilation shaft. Metal walls press close. "
            "The air is thick and stale. A dim EMERGENCY LIGHT flickers ahead. "
            "You can hear distant sounds — footsteps? machinery? "
            "A GRATE blocks the path NORTH. A MAINTENANCE LOG is taped to the wall. "
            "You can go back WEST or continue NORTH if you can open the grate."
        ),
        "exits": {"west": "control_room", "north": "morgue"},
        "items": ["grate", "maintenance_log", "emergency_light"],
        "puzzle": {
            "type": "item",
            "answer": "toolbox",
            "hint": "The GRATE is bolted shut. You need something to unscrew it — did you pick up anything useful earlier? Check your INVENTORY.",
            "solved": False,
            "reward": "You unscrew the grate. It falls away with a clang. Path NORTH is open."
        }
    },

    #MORGUE
    "morgue": {
        "description": (
            "A cold, dimly lit morgue. Steel drawers line the walls. "
            "Most are sealed. One drawer is slightly open — a TAG hangs from it. "
            "A MEDICAL CABINET stands in the corner, locked with a padlock. "
            "A PATIENT FILE sits on an examination table. "
            "The ventilation shaft is SOUTH. A stairwell leads NORTH."
        ),
        "exits": {"south": "ventilation_shaft", "north": "director_office"},
        "items": ["drawer_tag", "medical_cabinet", "patient_file"],
        "puzzle": {
            "type": "code",
            "answer": "ex19",
            "hint": "The MEDICAL CABINET is padlocked. Padlocks usually have a code — have you EXAMINED the PATIENT FILE on the table? Or the DRAWER TAG?",
            "solved": False,
            "reward": "The padlock snaps open. Inside the cabinet: a SECURITY BADGE and a SYRINGE labeled 'Antidote'."
        }
    },

    
    #BUREAU DU DIR
    "director_office": {
        "description": (
            "A large, once-luxurious office. A mahogany desk dominates the room. "
            "Papers are scattered everywhere — someone searched this place before you. "
            "A PORTRAIT hangs crooked on the wall — something might be hidden behind it. "
            "A COMPUTER requires a SECURITY BADGE to unlock. "
            "A LETTER lies open on the desk. "
            "The morgue is SOUTH. A locked door leads EAST to the rooftop."
        ),
        "exits": {"south": "morgue", "east": "rooftop"},
        "items": ["portrait", "director_computer", "letter"],
        "puzzle": {
            "type": "item",
            "answer": "security_badge",
            "hint": "The COMPUTER needs a SECURITY BADGE. You've been through a lot of rooms — did you find one? Check your INVENTORY.",
            "solved": False,
            "reward": "The computer unlocks. A message: ROOFTOP ACCESS GRANTED. The east door clicks open."
        }
    },

    #TOIT
    "rooftop": {
        "description": (
            "You burst onto the rooftop. Cold night air hits your face. "
            "The city stretches out below you. A HELICOPTER PAD is marked in faded yellow paint. "
            "A FLARE GUN sits in a case nearby — one shot left. "
            "A RADIO TOWER blinks in the distance. A locked HATCH leads back DOWN. "
            "The director's office is WEST. Freedom is one signal away — NORTH if you can call for help."
        ),
        "exits": {"west": "director_office", "north": "exit"},
        "items": ["flare_gun", "helicopter_pad", "radio_tower"],
        "puzzle": {
            "type": "item",
            "answer": "flare_gun",
            "hint": "You need to signal for rescue. There's a FLARE GUN nearby — have you tried to USE it?",
            "solved": False,
            "reward": "You fire the flare into the sky. A distant helicopter turns toward you. The north gate unlocks."
        }
    },

    #SORTIE
    "exit": {
        "description": (
            "The helicopter descends. Wind whips across the rooftop. "
            "A rope ladder drops to your feet. You grab it. "
            "Below, the facility shrinks into the darkness. You made it."
        ),
        "exits": {},
        "items": [],
        "puzzle": None
    }
}

#DESCRIPTION OBJET

ITEM_DESCRIPTIONS = {
    #ServRoom
    "keypad": "A numeric keypad mounted on the wall. It's waiting for a 4-digit code. The buttons are worn — someone used this often.",
    "broken_screen": "A cracked monitor. You squint through the static. A sticky note is taped to the corner: 'Favorite book by George Orwell.' That's the hint, not the answer.",
    "access_card": "A magnetic access card. The name on it reads: Dr. Chen — Level 3 clearance. Useful for card readers.",

    #corridor
    "locked_door": "A heavy security door with a card reader blinking red on the side. It needs an ACCESS CARD.",
    "vent": "A metal vent cover on the floor. It's bolted shut for now.",
    "torn_note": "A torn piece of paper. You piece it together: 'The answer is in our DNA... literally. —Dr. Chen'",

    #StorageRoom
    "fuse_box": "An open fuse box. Wires are disconnected — that's why the north door has no power. Type 'code fix' to reconnect them.",
    "toolbox": "A red metal toolbox. Inside: screwdrivers, pliers, and a wrench. Could be useful for bolted things.",
    "logbook": "A maintenance logbook. Most entries are routine. One stands out: 'PIN changed to 0451 per security directive. —R.M.'",

    # SecurityOffice
    "monitor": "A security monitor showing a grainy feed. You can make out the lab to the west. Nothing moves.",
    "drawer": "A slightly open desk drawer. Inside: a sticky note that reads '0451 — do NOT lose this'.",
    "holster": "An empty gun holster. Whoever wore this left in a hurry — or didn't make it out.",

    #Lab
    "computer": "An old desktop computer. The login screen blinks: 'PASSWORD REQUIRED'. The cursor waits.",
    "lab_notes": "Pages of research notes. Most are technical. One is circled in red: 'Master password = building block of life. Keep it simple.'",
    "strange_vial": "A vial of glowing blue liquid. Label: 'Sample X-19 — Experimental. DO NOT INGEST.' You set it down carefully.",

    #ReactorRoom
    "control_panel": "A wall of switches and dials. Most are labeled with technical jargon. One switch is labeled: NORTH DOOR OVERRIDE — requires keypad code.",
    "radiation_suit": "A full radiation protection suit. It looks worn but functional. You leave it — you don't have time.",
    "warning_sign": "A bright yellow warning sign: REACTOR CORE ACTIVE — AUTHORIZED PERSONNEL ONLY. Below someone has scrawled: 'override = 7734'.",

    #controlroom
    "radio": "A crackling radio. An emergency broadcast loops: 'All personnel evacuate. This is not a drill.' Nobody answered.",
    "safe": "A wall safe with a combination dial. Three turns required: left, right, left.",
    "clipboard": "A clipboard with a checklist. At the bottom, handwritten: 'Safe combo: left42 right17 left8 — Chief's orders.'",

    #VentilationShaft
    "grate": "A metal grate bolted to the shaft wall. Four screws hold it in place. You need a tool.",
    "maintenance_log": "A maintenance log taped to the wall. Last entry: 'Grate re-bolted after incident. Toolbox left in storage.' — 3 weeks ago.",
    "emergency_light": "A dim emergency light. It flickers every few seconds, casting long shadows through the shaft.",

    #Morgue
    "drawer_tag": "A toe tag hanging from the open drawer. Name: EXPERIMENT X-19. ID: EX19. Date: classified.",
    "medical_cabinet": "A locked medical cabinet. The padlock has a 4-character slot. It looks recently used.",
    "patient_file": "A patient file labeled EXPERIMENT X-19. Most pages are redacted. One line survives: 'Subject ID: EX19'.",

    #DirectorOffice
    "portrait": "A large portrait of a stern-looking man — the director, presumably. It hangs slightly crooked. Nothing behind it. Just a wall.",
    "director_computer": "A sleek computer on the mahogany desk. Screen reads: SECURITY BADGE REQUIRED FOR ACCESS.",
    "letter": "An open letter on the desk. It reads: 'If you're reading this, the facility has been compromised. Get to the rooftop. Signal for rescue. —Director Hale'",

    #Rooftop
    "flare_gun": "A bright orange flare gun. One cartridge loaded. This could signal a rescue helicopter.",
    "helicopter_pad": "A faded yellow H painted on the concrete. Designed for helicopter landings. If only someone knew you were here.",
    "radio_tower": "A tall radio tower in the distance, blinking red. You can't reach it from here."
}
