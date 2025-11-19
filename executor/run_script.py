import subprocess
import os

def run_with_venv(script_path, venv_path):
    # Détection Windows / Linux / Mac
    if os.name == "nt":  # Windows
        python_bin = os.path.join(venv_path, "Scripts", "python.exe")
    else:  # Linux / Mac
        python_bin = os.path.join(venv_path, "bin", "python")

    # Vérifier que l'interpréteur existe
    if not os.path.exists(python_bin):
        return None, f"Interpréteur introuvable : {python_bin}"

    try:
        result = subprocess.run(
            [python_bin, script_path],
            capture_output=True,
            text=True
        )
        return result.stdout, result.stderr

    except Exception as e:
        return None, str(e)