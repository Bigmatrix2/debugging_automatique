import subprocess
from pathlib import Path
from typing import Tuple, List, Dict
def run_script(script_path: str, timeout: int = 10) -> Tuple[int, str, str]:
    proc = subprocess.run(['python', script_path], capture_output=True, text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr
def read_file(path: str) -> str:
    return Path(path).read_text(encoding='utf-8')
def write_file(path: str, content: str):
    Path(path).write_text(content, encoding='utf-8')
def apply_fix(lines: List[str], fix: Dict) -> List[str]:
    action = fix['action']
    line = fix.get('line', None)
    content = fix.get('content', '')
    if action == 'delete':
        return lines[:line-1] + lines[line:]
    elif action == 'replace':
        lines[line-1] = content + ('\n' if not content.endswith('\n') else '')
        return lines
    elif action == 'insert_before':
        return lines[:line-1] + [content + '\n'] + lines[line-1:]
    elif action == 'insert_after':
        return lines[:line] + [content + '\n'] + lines[line:]
    else:
        raise ValueError('Action inconnue: '+action)
def apply_fixes_to_file(file_path: str, fixes: List[Dict]):
    lines = read_file(file_path).splitlines(keepends=True)
    for fix in fixes:
        lines = apply_fix(lines, fix)
    write_file(file_path, ''.join(lines))
