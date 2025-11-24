# classification_mail.py

from groq import Groq, RateLimitError
from dotenv import load_dotenv
import json
import os
import re
import time

# Charger variables du .env
load_dotenv()

client = Groq(api_key=os.environ["GROQ_KEY"])


# --- Charger les fichiers externes ---
def load_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


CONTEXT = load_text_file("context.txt")
PROMPT_TEMPLATE = load_text_file("prompt.txt")


# --- Nettoyage du JSON renvoyé ---
def clean_json(raw: str) -> str:
    """
    Supprime les blocs ```json et ``` autour de la réponse.
    """
    cleaned = re.sub(r"```json|```", "", raw).strip()
    return cleaned


# --- Fonction principale ---
def classify_ticket(subject: str, body: str) -> dict:

    # Construire le prompt final
    prompt = PROMPT_TEMPLATE.replace("{{sujet}}", subject)\
                            .replace("{{contenu}}", body)

    messages = [
        {"role": "system", "content": CONTEXT},
        {"role": "user", "content": prompt}
    ]

    # --------------- Gestion Rate Limit (retry auto) ----------------
    while True:
        try:
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages
            )
            break  # Si ça marche, on sort de la boucle

        except RateLimitError:
            print("\n  Rate limit atteint — pause 2 secondes...\n")
            time.sleep(2)
    # ------------------------------------------------------------------

    # Contenu brut
    raw_response = completion.choices[0].message.content.strip()

    # Debug console
    print("\n===== RÉPONSE GROQ =====")
    print(raw_response)
    print("===== FIN RÉPONSE GROQ =====\n")

    # Nettoyage JSON
    json_text = clean_json(raw_response)

    print("===== JSON NETTOYÉ =====")
    print(json_text)
    print("===== FIN JSON NETTOYÉ =====\n")

    # Conversion
    return json.loads(json_text)
