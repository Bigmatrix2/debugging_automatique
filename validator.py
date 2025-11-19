def validate_json(data: dict, max_lines: int):
    if not isinstance(data.get("uncertain"), bool):
        raise ValueError("Champ 'uncertain' doit être booléen")

    corrections = data.get("corrections", [])
    if not isinstance(corrections, list):
        raise ValueError("Champ 'corrections' doit être une liste")

    # Nouvelle limite : 10
    if len(corrections) > 10:
        raise ValueError("Trop de corrections proposées (>10)")

    for corr in corrections:
        # Champs obligatoires
        if "type" not in corr or "line_number" not in corr or "reason" not in corr or "new" not in corr:
            raise ValueError("Correction invalide: champs manquants")

        # Validation du type
        if corr["type"] not in ["replace", "insert", "delete"]:
            raise ValueError(f"Correction invalide: type inconnu '{corr['type']}'")

        # Validation du numéro de ligne
        if not isinstance(corr["line_number"], int) or corr["line_number"] < 1 or corr["line_number"] > max_lines:
            raise ValueError(f"Correction invalide: numéro de ligne {corr['line_number']} hors fichier")

        # "old" devient optionnel → pas d'erreur si absent
        if "old" in corr and not isinstance(corr["old"], str):
            raise ValueError("Champ 'old' doit être une chaîne si présent")

        # Conseil d'amélioration : vérifier que "new" n'est pas vide
        if not corr["new"].strip():
            raise ValueError("Correction invalide: champ 'new' vide")

    if "final_suggestion" not in data or not isinstance(data["final_suggestion"], str):
        raise ValueError("Champ 'final_suggestion' manquant ou invalide")

    return True
