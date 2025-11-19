import subprocess
import sys

def run_script(python_bin, script_path, timeout=10):
    try:
        proc = subprocess.Popen(
            [python_bin, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out, err = proc.communicate(timeout=timeout)
        return {
            "stdout": out,
            "stderr": err,
            "returncode": proc.returncode  # cohérent avec main.py
        }
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        return {
            "stdout": out,
            "stderr": f"Timeout: le script a dépassé {timeout} secondes\n{err}",
            "returncode": -1
        }
    except FileNotFoundError:
        return {
            "stdout": "",
            "stderr": f"Erreur: binaire Python introuvable ({python_bin})",
            "returncode": -1
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Erreur inattendue: {e}",
            "returncode": -1
        }