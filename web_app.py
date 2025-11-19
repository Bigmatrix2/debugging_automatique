import streamlit as st
from utils import run_script, read_file, apply_fixes_to_file
from prompt import ask_mistral_for_fixes
st.title('Debugging Agent - Web Interface')
script_path = st.text_input('Chemin du script à analyser','sample_buggy.py')
if st.button('Exécuter et demander corrections'):
    rc, out, err = run_script(script_path)
    st.subheader('Résultat de l\'exécution')
    st.text('STDOUT:\\n' + (out or '[vide]'))
    st.text('STDERR:\\n' + (err or '[vide]'))
    if err.strip() == '':
        st.success('Aucune erreur détectée.')
    else:
        st.info('Envoi du code et de l\'erreur à Mistral...')
        source = read_file(script_path)
        fixes = ask_mistral_for_fixes(script_path, source, err).get('fixes', [])
        st.subheader('Corrections proposées')
        st.json(fixes)
        if fixes:
            if st.button('Appliquer les corrections'):
                apply_fixes_to_file(script_path, fixes)
                st.success('Corrections appliquées au script !')
