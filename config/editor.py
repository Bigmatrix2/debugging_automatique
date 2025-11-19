from .loader import load_config, save_config
def update_config(script_path=None, venv_path=None):
    d=load_config()
    if script_path: d['script_path']=script_path
    if venv_path: d['venv_path']=venv_path
    save_config(d)
