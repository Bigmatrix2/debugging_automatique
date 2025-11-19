import os
import json
from mistralai import Mistral
def get_mistral_client():
    api_key = os.environ.get('MISTRAL_API_KEY')
    if not api_key:
        raise ValueError('MISTRAL_API_KEY non défini')
    return Mistral(api_key=api_key)
def build_prompt(file_path: str, source_code: str, error_text: str) -> list:
    system = (
        'You are an automated code fixer. '
        'Only respond with JSON, schema: {""fixes"": [{""file"":""<file>"", ""action"":""replace|insert_before|insert_after|delete"", '
        '""line"":<int>, ""content"":""<str>"", ""reason"":""<str>""}]}.' 
    )
    user = (
        f'File: {file_path}\n'
        f'Code:\n{source_code}\n'
        f'Error:\n{error_text}\n'
        'Return a JSON following the schema above. If no fix, return {""fixes"":[]}'
    )
    return [{'role':'system','content':system},{'role':'user','content':user}]
def ask_mistral_for_fixes(file_path: str, source_code: str, error_text: str) -> dict:
    client = get_mistral_client()
    messages = build_prompt(file_path, source_code, error_text)

    # Appel correct du modèle
    resp = client.chat.complete(
        model="mistral-small-latest",
        messages=messages,
        max_tokens=800
    )

    # Nouveau format de réponse (2025)
    text = resp.choices[0].message.content

    # Parsing JSON sécurisé
    try:
        return json.loads(text)
    except:
        import re
        match = re.search(r"(\{.*\}|\[.*\])", text, flags=re.S)
        if match:
            return json.loads(match.group(1))
        return {"fixes": []}
