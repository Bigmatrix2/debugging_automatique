def validate_patch_json(d):
    if not isinstance(d, dict): return False, "Format JSON invalide."

    if "explanation" not in d or "fixes" not in d:
        return False, "Champs manquants."

    if not isinstance(d["fixes"], list):
        return False, "fixes doit être une liste."

    for fix in d["fixes"]:
        if not isinstance(fix, dict):
            return False, "Chaque correctif doit être un objet JSON."

        if "line" not in fix or "action" not in fix:
            return False, "Champ line/action manquant."

        if fix["action"] in ("replace", "insert") and "content" not in fix:
            return False, "'content' manquant pour insert/replace."

    return True, "OK"
