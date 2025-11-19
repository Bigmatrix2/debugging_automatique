# Debugging Agent - version simple avec web
## Installation
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
setx MISTRAL_API_KEY ""sk-xxxx""
## Lancer CLI
python main.py
## Lancer l'interface web
streamlit run web_app.py
## Test
Le script 'sample_buggy.py' contient un bug volontaire.
