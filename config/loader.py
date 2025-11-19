import json, os
CONFIG_PATH=os.path.join(os.path.dirname(__file__),"config.json")
def load_config():
    with open(CONFIG_PATH) as f: return json.load(f)
def save_config(d):
    with open(CONFIG_PATH,"w") as f: json.dump(d,f,indent=4)
