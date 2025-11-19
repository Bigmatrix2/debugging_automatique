def apply_patches(path, patch):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    fixes = sorted(patch["fixes"], key=lambda x: x["line"], reverse=True)

    for fix in fixes:
        index = fix["line"] - 1
        action = fix["action"]

        if action == "delete":
            if 0 <= index < len(lines):
                lines.pop(index)

        elif action == "replace":
            if 0 <= index < len(lines):
                lines[index] = fix["content"] + "\n"

        elif action == "insert":
            if 0 <= index <= len(lines):
                lines.insert(index, fix["content"] + "\n")

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
