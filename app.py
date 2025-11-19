import streamlit as st
import os

from config.loader import load_config
from config.editor import update_config
from executor.run_script import run_with_venv
from ai.client import ask_model
from patcher.validator import validate_patch_json
from patcher.apply import apply_patches


# ------------------------------ UI STYLE ------------------------------

st.set_page_config(
    page_title="Auto-Debugger Python",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
body { background-color:#f5f6f7; font-family:'Segoe UI',sans-serif; }
h1,h2,h3 { font-weight:600; color:#222; }

.block {
    background:white;
    padding:25px;
    border-radius:10px;
    border:1px solid #e3e3e3;
    margin-bottom:20px;
}

.stButton>button {
    background-color:#3366ff;
    color:white;
    border-radius:6px;
    padding:8px 18px;
}
.stButton>button:hover { background-color:#254eda; }

div[data-testid="stJson"] {
    background:#fafafa !important;
    padding:15px;
    border-radius:8px;
    border:1px solid #ddd;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ------------------------------ SIDEBAR ------------------------------

st.sidebar.title("Configuration")
config = load_config()

script_path = st.sidebar.text_input("Chemin du script Python", config.get("script_path", ""))
venv_path = st.sidebar.text_input("Chemin du dossier venv", config.get("venv_path", ""))

if st.sidebar.button("Enregistrer"):
    update_config(script_path, venv_path)
    st.sidebar.success("Configuration enregistrée !")


# ------------------------------ MAIN TITLE ------------------------------

st.title("Auto-Debugger Python (Ollama + DeepSeek-Instruct)")


# ------------------------------ MAIN BLOCK ------------------------------

st.markdown("<div class='block'>", unsafe_allow_html=True)
st.subheader("Exécution du script")

if st.button("Lancer l'analyse"):

    if not os.path.exists(script_path):
        st.error("Le script spécifié n'existe pas.")
    else:
        stdout, stderr = run_with_venv(script_path, venv_path)

        st.write("### Sortie du script :")
        st.code(stdout or "Aucune sortie.")

        st.write("### Erreur du script :")
        if stderr:
            st.error(stderr)
        else:
            st.success("Aucune erreur détectée.")

        # ---------------- IA -----------------
        if stderr:

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div class='block'>", unsafe_allow_html=True)

            st.subheader("Analyse IA (DeepSeek via Ollama)")

            # Lire le code source
            try:
                code = open(script_path, "r", encoding="utf-8").read()
            except:
                st.error("Impossible de lire le fichier source.")
                code = ""

            analysis = ask_model(code, stderr)

            st.write("### JSON analysé")
            st.json(analysis)

            valid, msg = validate_patch_json(analysis)
            st.write("### Validation du JSON :", msg)

            if valid and analysis["fixes"]:
                if st.button("Appliquer les corrections"):
                    try:
                        apply_patches(script_path, analysis)
                        st.success("Corrections appliquées avec succès !")
                    except Exception as e:
                        st.error(f"Erreur lors de l'application des corrections : {e}")

st.markdown("</div>", unsafe_allow_html=True)
