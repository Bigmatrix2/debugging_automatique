# main.py

from utils_gmail import gmail_connect, get_all_messages, parse_email
from classification_mail import classify_ticket
from utils_sheets import append_to_sheet


def main():
    print("Connexion à Gmail...")
    gmail = gmail_connect()

    print("Récupération des mails...")
    messages = get_all_messages(gmail)

    print(f"{len(messages)} mails trouvés.")

    for msg in messages:
        sujet, corps, date_envoi = parse_email(msg)
        print(f"\nTraitement du ticket : {sujet}")

        data = classify_ticket(sujet, corps)

        categorie = data["categorie"]
        urgence = data["urgence"]
        synthese = data["synthese"]

        print(f"→ Catégorie : {categorie}")
        print(f"→ Urgence   : {urgence}")

        append_to_sheet(categorie, sujet, urgence, synthese, date_envoi)


    print("\n Tous les tickets ont été écrits dans Google Sheets.")


if __name__ == "__main__":
    main()
