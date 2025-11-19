from utils import run_script, read_file, apply_fixes_to_file
from prompt import ask_mistral_for_fixes
SCRIPT_PATH = 'sample_buggy.py'
def main():
    rc, out, err = run_script(SCRIPT_PATH)
    print('STDOUT:', out)
    print('STDERR:', err)
    if err.strip() == '':
        print('Aucune erreur détectée.')
        return
    source = read_file(SCRIPT_PATH)
    fixes = ask_mistral_for_fixes(SCRIPT_PATH, source, err).get('fixes', [])
    print('Fixes proposés:', fixes)
    if fixes:
        apply_fixes_to_file(SCRIPT_PATH, fixes)
        print('Corrections appliquées.')
if __name__ == '__main__':
    main()
