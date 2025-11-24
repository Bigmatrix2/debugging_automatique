# utils_gmail.py

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import base64

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def gmail_connect():
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=0)
    return build("gmail", "v1", credentials=creds)

def get_all_messages(service, max_results=549):
    msgs = []
    results = service.users().messages().list(userId="me", maxResults=max_results).execute()
    for m in results.get("messages", []):
        full = service.users().messages().get(userId="me", id=m["id"]).execute()
        msgs.append(full)
    return msgs

def parse_email(message):
    headers = message["payload"]["headers"]

    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
    date_raw = next((h["value"] for h in headers if h["name"] == "Date"), "")

    # Convertir la date Gmail (RFC2822) en format YYYY/MM/DD
    from email.utils import parsedate_to_datetime
    try:
        dt = parsedate_to_datetime(date_raw)
        date_envoi = dt.strftime("%Y/%m/%d")
    except:
        date_envoi = ""

    body = ""
    payload = message["payload"]
    parts = payload.get("parts", [])

    if parts:
        for part in parts:
            if part["mimeType"] == "text/plain":
                data = part["body"]["data"]
                body = base64.urlsafe_b64decode(data).decode()
    else:
        data = payload["body"].get("data", "")
        if data:
            body = base64.urlsafe_b64decode(data).decode()

    return subject, body, date_envoi
