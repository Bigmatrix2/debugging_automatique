import streamlit as st
from prompt import ask_mistral_for_fixes
import subprocess

# --- Fonctions utilitaires ---

def run_script(path):
    try:
        result = subprocess.run(
            ["python", path],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def apply_fixes_to_file(file_path: str, fixes: list):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for fix in fixes:
        line_idx = fix['line'] - 1
        if fix['action'] == 'replace':
            lines[line_idx] = fix['content'] + '\n'
        elif fix['action'] == 'insert_before':
            lines.insert(line_idx, fix['content'] + '\n')
        elif fix['action'] == 'insert_after':
            lines.insert(line_idx + 1, fix['content'] + '\n')
        elif fix['action'] == 'delete':
            lines.pop(line_idx)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

# --- Streamlit Interface ---

st.title('Debugging Agent - Web Interface')

script_path = st.text_input('Chemin du script à analyser', 'sample_buggy.py')

# Exécution du script et récupération des fixes
if st.button('Exécuter et demander corrections'):
    rc, out, err = run_script(script_path)
    st.session_state['out'] = out
    st.session_state['err'] = err

    st.subheader('Résultat de l\'exécution')
    st.text('STDOUT:\n' + (out or '[vide]'))
    st.text('STDERR:\n' + (err or '[vide]'))

    if err.strip() != '':
        st.info('Envoi du code et de l\'erreur à Mistral...')
        source = read_file(script_path)
        fixes = ask_mistral_for_fixes(script_path, source, err).get('fixes', [])
        st.session_state['fixes'] = fixes
    else:
        st.success('Aucune erreur détectée.')
        st.session_state['fixes'] = []

# Affichage des corrections et bouton pour appliquer
if 'fixes' in st.session_state and st.session_state['fixes']:
    st.subheader('Corrections proposées')
    st.json(st.session_state['fixes'])

    if st.button('Appliquer les corrections'):
        apply_fixes_to_file(script_path, st.session_state['fixes'])
        st.success('Corrections appliquées au script !')
        st.subheader('Nouveau contenu du script')
        st.code(read_file(script_path))
