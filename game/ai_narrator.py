import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_room_description(room_name, items, context=""):
    """ Génère une description atmosphérique d'une salle via l'IA
    room_name : nom de la salle
    items : liste des objets présents dans la salle
    context : contexte supplémentaire (actions du joueur, etc.)
    """
    try: 
          # Construit le prompt envoyé à l'IA
         prompt = f"""You are the narrator of a retro text-based escape game set in an abandoned research facility.
        
Generate a short atmospheric description (2-3 sentences) for this room:
- Room: {room_name}
- Items visible: {', '.join(items)}
- Context: {context if context else 'Player just entered the room'}

Rules:
- Write in second person (you see, you hear...)
- Be atmospheric and slightly unsettling
- Mention the items naturally in the description
- Keep it under 60 words
- No dialogue
"""
        # Envoie le prompt à Groq
         response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Modèle de l'ia
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,  # Limite la longueur de la réponse
            temperature=0.8  # Créativité (0=prévisible, 1=très créatif)
        )

        # Retourne le texte généré  
         return response.choices[0].message.content.strip()

    except Exception as e:
        # Si l'IA échoue, retourne une description par défaut
        return f"You are in the {room_name}. You see: {', '.join(items)}."
    #except Exception as e:
     # Affiche l'erreur exacte pour d├®bugger
     #return f"AI ERROR: {str(e)}"
