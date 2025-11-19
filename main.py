import streamlit as st
import json
from pathlib import Path
import sys
from pydantic import BaseModel, ValidationError
from jsonschema import validate as json_validate, ValidationError as JSONSchemaError

from runner import run_script
from llm_client import query_ollama
from validator import validate_json
from patcher import apply_corrections
from logging_utils import setup_logger, log_execution, log_ai_response, log_corrections, log_patch

# --- Définition du schéma Pydantic ---
class ProjectConfig(BaseModel):
    name: str
    script_path: str
    venv_path: str
    backup_enabled: bool
    max_corrections: int

class AIConfig(BaseModel):
    model: str
    system_prompt: str
    user_prompt: str
    temperature: float
    max_tokens: int
    strict_json: bool

class LoggingConfig(BaseModel):
    enabled: bool
    log_file: str
    save_responses: bool

class UIConfig(BaseModel):
    theme: str
    show_stdout: bool
    show_stderr: bool
    auto_apply: bool

class Config(BaseModel):
    project: ProjectConfig
    ai: AIConfig
    logging: LoggingConfig
    ui: UIConfig

# --- Fonction de chargement et validation du config.json ---
def load_config(config_path="config.json", schema_path="config.schema.json") -> Config:
    try:
        raw = json.loads(Path(config_path).read_text())
    except Exception as e:
        st.error(f"Impossible de lire le fichier config.json: {e}")
        sys.exit(1)

    # Validation avec jsonschema
    try:
        schema = json.loads(Path(schema_path).read_text())
        json_validate(instance=raw, schema=schema)
    except JSONSchemaError as e:
        st.error(f"Config invalide selon le schéma JSON: {e.message}")
        sys.exit(1)
    except Exception as e:
        st.error(f"Impossible de lire le schéma JSON: {e}")
        sys.exit(1)

    # Validation avec Pydantic
    try:
        return Config(**raw)
    except ValidationError as e:
        st.error(f"Config invalide selon Pydantic: {e}")
        sys.exit(1)

def main():
    st.title("Agent de Debugging Automatique")

    # Charger configuration
    config = load_config()

    # Initialiser logger
    logger = None
    if config.logging.enabled:
        logger = setup_logger(config.logging.log_file)

    # Pré-remplir champs depuis config.json
    venv_path = st.text_input("Chemin vers l'environnement virtuel", value=config.project.venv_path)
    script_path = st.text_input("Chemin vers le script Python à analyser", value=config.project.script_path)
    model = st.text_input("Nom du modèle Ollama", value=config.ai.model)
    context_file = st.text_input("Fichier system prompt", value=config.ai.system_prompt)
    prompt_file = st.text_input("Fichier user prompt", value=config.ai.user_prompt)

    if st.button("Analyser le script"):
        script = Path(script_path)
        if not script.exists():
            st.error(f"Script introuvable: {script}")
            return

        # 1. Exécution du script
        result = run_script(venv_path, script, logger=logger)

        if config.ui.show_stdout and result["stdout"]:
            st.subheader("Sortie standard (stdout)")
            st.code(result["stdout"], language="text")

        # Affichage du code de sortie
        st.write("Code de sortie:", result["returncode"])

        # Affichage de l'erreur
        if config.ui.show_stderr and result["stderr"]:
            st.subheader("Erreur détectée")
            formatted_err = result["stderr"].replace(str(script), script.name)
            st.code(formatted_err.strip(), language="python")

        if result["returncode"] == 0:
            st.success("Script exécuté sans erreur.")
            return

        # 2. Envoi à Ollama
        code = script.read_text()
        error = result["stderr"]

        try:
            response = query_ollama(
                model=model,
                system_path=context_file,
                prompt_path=prompt_file,
                code=code,
                error=error
            )
        except Exception as e:
            st.error(f"Erreur lors de l'appel à Ollama: {e}")
            return

        if logger and config.logging.save_responses:
            log_ai_response(logger, response)

        # 3. Validation du JSON IA
        try:
            validate_json(response, max_lines=len(code.splitlines()))
        except Exception as e:
            st.error(f"Réponse IA invalide: {e}")
            # Fallback : écrire la suggestion finale dans un fichier séparé
            if "final_suggestion" in response:
                corrected_path = Path(script_path).with_name(Path(script_path).stem + "_corrected.py")
                corrected_path.write_text(response["final_suggestion"], encoding="utf-8")
                st.info(f"Suggestion finale écrite dans: {corrected_path}")
            return

        # 4. Affichage des corrections proposées
        st.subheader("Corrections proposées")
        if response.get("uncertain", False):
            st.warning("L'IA n'est pas certaine du bug.")
        else:
            corrections = response["corrections"]
            if len(corrections) > config.project.max_corrections:
                st.error("Trop de corrections proposées, limite dépassée.")
                return

            for corr in corrections:
                st.write(f"Ligne {corr['line_number']} | {corr['type']} | {corr['reason']}")
                st.code(corr.get("new", "(suppression)"), language="python")

            if logger:
                log_corrections(logger, corrections)

        # 5. Suggestion finale (affichée mais pas appliquée)
        st.subheader("Suggestion finale")
        formatted_suggestion = response["final_suggestion"]
        keywords = ["def ", "for ", "if ", "class ", "while ", "import ", "print("]
        for kw in keywords:
            formatted_suggestion = formatted_suggestion.replace(kw, "\n" + kw)
        st.code(formatted_suggestion.strip(), language="python")

        # 6. Bouton pour appliquer les corrections
        if st.button("Appliquer les corrections"):
            corrected_file, backup = apply_corrections(str(script), response["corrections"])
            st.success(f"Corrections appliquées sur {corrected_file}. Backup créé: {backup}")
            if logger:
                log_patch(logger, str(script), backup)

if __name__ == "__main__":
    main()
