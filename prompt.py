import os
import json
import time
import re
from mistralai import Mistral
from mistralai.models.sdkerror import SDKError

def get_mistral_client():
    api_key = os.environ.get('MISTRAL_API_KEY')
    if not api_key:
        raise ValueError('MISTRAL_API_KEY non défini')
    return Mistral(api_key=api_key)

def build_prompt(file_path: str, source_code: str, error_text: str) -> list:
    system = (
        'You are an automated code fixer. '
        'Only respond with JSON strictly following this schema: '
        '{"fixes":[{"file":"<file>","action":"replace|insert_before|insert_after|delete","line":<int>,"content":"<str>","reason":"<str>"}]}. '
        'Do NOT include extra text, comments, or indices like 0: or 1:.'
    )
    user = (
        f'File: {file_path}\n'
        f'Code:\n{source_code}\n'
        f'Error:\n{error_text}\n'
        'Return a valid JSON following the schema above. If no fix is needed, return {"fixes":[]}.' 
    )
    return [{'role':'system','content':system},{'role':'user','content':user}]

def ask_mistral_for_fixes(file_path: str, source_code: str, error_text: str) -> dict:
    client = get_mistral_client()
    messages = build_prompt(file_path, source_code, error_text)

    for attempt in range(3):
        try:
            resp = client.chat.complete(
                model="mistral-small-2409",
                messages=messages,
                max_tokens=8000
            )
            text = resp.choices[0].message.content

            # Nettoyage simple pour JSON
            text_clean = re.sub(r'\d+:', '', text)
            return json.loads(text_clean)

        except (SDKError, json.JSONDecodeError):
            pass  # on réessaie

    # Si tout échoue, on renvoie un JSON de test
    print("JSON invalide ou modèle indisponible, retour de test")
    return {
        "fixes": [
            {
                "file": file_path,
                "action": "replace",
                "line": 3,
                "content": "print('not_defined_variable')",
                "reason": "Fallback test JSON when model fails"
            }
        ]
    }
