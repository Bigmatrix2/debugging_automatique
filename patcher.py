from pathlib import Path
import shutil

def apply_corrections(script_path: str, corrections: list):
    script = Path(script_path)

    # Sauvegarde du fichier original
    backup = script.with_name(script.stem + "_original.py")
    shutil.copy(script, backup)

    lines = script.read_text(encoding="utf-8").splitlines()

    for corr in corrections:
        line_index = corr["line_number"] - 1  # JSON est 1-based
        applied = False

        # Vérification que "new" n'est pas vide
        if corr["type"] in ["replace", "insert"] and not corr["new"].strip():
            print(f"Correction ignorée car 'new' est vide : {corr}")
            continue

        if 0 <= line_index < len(lines):
            if corr["type"] == "replace":
                lines[line_index] = corr["new"]
                applied = True
            elif corr["type"] == "delete":
                lines.pop(line_index)
                applied = True
            elif corr["type"] == "insert":
                lines.insert(line_index, corr["new"])
                applied = True

        # Recherche par contenu si "old" est fourni
        if not applied and "old" in corr and corr["old"]:
            for i, line in enumerate(lines):
                if corr["old"].strip() in line.strip():
                    if corr["type"] == "replace":
                        lines[i] = corr["new"]
                    elif corr["type"] == "delete":
                        lines.pop(i)
                    elif corr["type"] == "insert":
                        lines.insert(i, corr["new"])
                    applied = True
                    break

        if not applied:
            print(f"Correction non appliquée (index hors limites ou 'old' introuvable) : {corr}")

    # Réécriture du fichier corrigé
    script.write_text("\n".join(lines), encoding="utf-8")

    return str(script), str(backup)
