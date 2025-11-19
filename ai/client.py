import subprocess
import json
import re
import os
from dotenv import load_dotenv

# Charger .env
load_dotenv()

OLLAMA_PATH = os.getenv("OLLAMA_PATH")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")



#  CLEAN JSON (fixe les formats DeepSeek foireux)

def clean_ai_json(d):
    if "fixes" not in d:
        d["fixes"] = []
        return d

    if not isinstance(d["fixes"], list):
        d["fixes"] = []
        return d

    cleaned = []

    for item in d["fixes"]:
        if isinstance(item, dict) and "line" in item:
            cleaned.append(item)
            continue

        if isinstance(item, dict) and len(item) == 1:
            key = list(item.keys())[0]
            if str(key).isdigit():
                cleaned.append(item[key])
                continue

    d["fixes"] = cleaned
    return d



#  EXTRACT JSON (sans regex récursives)

def extract_json(output: str):
    if not output:
        return None

    output = output.replace("```json", "").replace("```", "")

    depth = 0
    start = None
    blocks = []

    for i, c in enumerate(output):
        if c == "{":
            if depth == 0:
                start = i
            depth += 1

        elif c == "}":
            depth -= 1
            if depth == 0 and start is not None:
                blocks.append(output[start:i+1])

    if not blocks:
        return None

    json_str = max(blocks, key=len)
    json_str = re.sub(r",\s*}", "}", json_str)
    json_str = re.sub(r",\s*]", "]", json_str)

    try:
        return json.loads(json_str)
    except:
        return None



#  CALL OLLAMA (modèle IA local)

def ask_ollama(prompt):

    if not OLLAMA_PATH or not os.path.exists(OLLAMA_PATH):
        return {"explanation": "OLLAMA_PATH invalide ou introuvable.", "fixes": []}

    try:
        result = subprocess.run(
            [OLLAMA_PATH, "run", OLLAMA_MODEL],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"   # <-- évite le bug ?R
        )

        output = result.stdout.strip()
        data = extract_json(output)

        if data:
            return clean_ai_json(data)

        return {
            "explanation": "JSON invalide reçu : " + output[:300],
            "fixes": []
        }

    except Exception as e:
        return {"explanation": f"Erreur Ollama : {e}", "fixes": []}



#  BUILD PROMPT PRO

def ask_model(code, error):

    prompt = f"""
Tu dois répondre UNIQUEMENT par un JSON strict.
Premier caractère = "{{".

INTERDIT :
- markdown (```json)
- texte avant/après le JSON
- clés numériques comme "0": {{}}
- commentaires

OBLIGATOIRE :
- fixes est une LISTE d'objets JSON
- "line" = entier
- "action" ∈ ["replace","insert","delete"]
- "content" obligatoire pour replace/insert

FORMAT STRICT :

{{
  "explanation": "Analyse complète du problème, cause racine, comportement du code.",
  "fixes": [
    {{
      "line": <numéro>,
      "action": "replace | insert | delete",
      "content": "nouvelle ligne"
    }}
  ]
}}

Si aucune correction ne doit être faite :
{{
  "explanation": "aucune correction",
  "fixes": []
}}

Code :
{code}

Erreur :
{error}
"""

    return ask_ollama(prompt)
