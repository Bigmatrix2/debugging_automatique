# utils_sheets.py

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import uuid
from datetime import datetime
from dotenv import load_dotenv
import os

# Charger les variables du .env
load_dotenv()

# ID du Google Sheet
SHEET_ID = os.environ["SHEET_ID"]

# Authentification via service account
creds = Credentials.from_service_account_file(
    "service_account.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

sheet_service = build("sheets", "v4", credentials=creds)

# Mapping catégories → nom de feuille
SHEET_TABS = {
    "Problème technique informatique": "Technique",
    "Demande administrative": "Administratif",
    "Problème d’accès / authentification": "Acces",
    "Support utilisateur": "Support",
    "Demande de support utilisateur": "Support",
    "Bug / dysfonctionnement": "Bug",
}

def append_to_sheet(cat, sujet, urgence, synthese, date_envoi):
    sheet_name = SHEET_TABS[cat]

    # Vérifier si les en-têtes existent déjà
    result = sheet_service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=f"{sheet_name}!A1:E1"
    ).execute()

    values = result.get("values", [])

    # Ajouter en-têtes si absents
    if not values:
        headers = [["ids_mail", "Sujet", "Urgence", "Synthèse", "date_enregistrement"]]
        sheet_service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range=f"{sheet_name}!A1:E1",
            valueInputOption="RAW",
            body={"values": headers}
        ).execute()
        print(f"[OK] En-têtes ajoutés dans '{sheet_name}'")

    # Génération id
    random_id = str(uuid.uuid4())[:8]

    # Ajout : date réelle du mail (déjà convertie)
    new_row = [[random_id, sujet, urgence, synthese, date_envoi]]

    sheet_service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=f"{sheet_name}!A:E",
        valueInputOption="RAW",
        body={"values": new_row}
    ).execute()

    print(f"[OK] Ticket ajouté dans '{sheet_name}'")

