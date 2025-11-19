import subprocess
import json
from pathlib import Path

def query_ollama(model: str, system_path: str, prompt_path: str, code: str, error: str):
    system_msg = Path(system_path).read_text(encoding="utf-8", errors="replace")
    user_msg = Path(prompt_path).read_text(encoding="utf-8", errors="replace")

    # Construction du prompt complet
    full_prompt = f"{system_msg}\n\n{user_msg}\n\nCode:\n{code}\n\nErreur:\n{error}"

    # Appel Ollama avec format JSON et encodage UTF-8
    result = subprocess.run(
        ["ollama", "run", model, "--format", "json"],
        input=full_prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if result.stderr:
        print("Erreur Ollama:", result.stderr)

    response = result.stdout.strip()

    # Validation JSON stricte
    try:
        parsed = json.loads(response)
    except json.JSONDecodeError:
        # Essayer de récupérer le premier bloc JSON
        start = response.find("{")
        end = response.rfind("}")
        if start != -1 and end != -1:
            try:
                parsed = json.loads(response[start:end+1])
            except Exception:
                raise ValueError(f"Réponse IA invalide: JSON non parsable\nSortie brute:\n{response}")
        else:
            raise ValueError(f"Réponse IA invalide: JSON non parsable\nSortie brute:\n{response}")

    # Vérification schéma minimal
    required_keys = ["uncertain", "corrections", "final_suggestion"]
    for key in required_keys:
        if key not in parsed:
            raise ValueError(f"Réponse IA invalide: champ '{key}' manquant")

    return parsed
