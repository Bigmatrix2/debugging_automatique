import subprocess
import os
from pathlib import Path
from logging_utils import log_execution

def run_script(venv_path: str, script_path: str, timeout: int = 10, logger=None):
    # Détection de la plateforme
    if os.name == "nt":  # Windows
        python_bin = Path(venv_path) / "Scripts" / "python.exe"
    else:  # Linux / macOS
        python_bin = Path(venv_path) / "bin" / "python"

    if not python_bin.exists():
        result = {
            "stdout": "",
            "stderr": f"Interpréteur introuvable: {python_bin}",
            "returncode": -1
        }
        if logger:
            log_execution(logger, script_path, result)
        return result

    try:
        result_proc = subprocess.run(
            [str(python_bin), str(script_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout
        )
        result = {
            "stdout": result_proc.stdout,
            "stderr": result_proc.stderr,
            "returncode": result_proc.returncode
        }
    except subprocess.TimeoutExpired:
        result = {
            "stdout": "",
            "stderr": f"Timeout: le script a dépassé {timeout} secondes",
            "returncode": -1
        }
    except Exception as e:
        result = {
            "stdout": "",
            "stderr": f"Erreur inattendue: {e}",
            "returncode": -1
        }

    # Journalisation automatique
    if logger:
        log_execution(logger, script_path, result)

    return result
