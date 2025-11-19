#  Debugging Agent – Automatic Python Bug Fixer

##  Contexte du projet

Ce projet est réalisé dans le cadre d’un module de création d’agents intelligents à HETIC. L’objectif est de construire un **agent autonome capable d’exécuter un script Python, détecter des erreurs, demander une correction à un LLM, appliquer automatiquement les correctifs**, et permettre ce processus aussi bien en **CLI** qu’en **interface web (Streamlit)**.

Il s’agit d’un mini-outil de debugging automatisé, utile pour apprendre :

* la manipulation d’erreurs Python (traceback),
* l’automatisation de corrections de code,
* l’intégration d’un agent LLM (Mistral ou fallback),
* la construction d’une UI simple mais fonctionnelle.

---

##  Objectif du projet

Le but principal : **réparer automatiquement un fichier Python buggé**, grâce à un agent autonome.

L’agent doit pouvoir :

1. exécuter un script Python donné,
2. récupérer son erreur,
3. envoyer le code + traceback à un large language model,
4. interpréter la réponse JSON contenant les correctifs,
5. appliquer les modifications au fichier original.

Le tout, avec une interface propre, simple, et éducative.

---

# 🧠 Schéma général du fonctionnement

Voici un schéma du flux complet du système :

```mermaid
flowchart TD
    A[Utilisateur lance l'analyse<br>(CLI ou WebApp)] --> B[Exécution du script Python]
    B --> C{Erreur détectée ?}
    C -- Non --> D[Aucune correction nécessaire]
    C -- Oui --> E[Envoi du code + erreur au LLM]
    E --> F[Réception des correctifs JSON]
    F --> G[Application des correctifs<br>au fichier Python]
    G --> H[Affichage du nouveau code<br>+ réexécution possible]
```

---

#  Arborescence du projet

```
debugging_agent/
│
├── main.py                # Runner CLI
├── web_app.py             # Interface Streamlit
├── prompt.py              # Interaction avec le LLM + fallback JSON
├── sample_buggy.py        # Script Python volontairement buggé
│
├── README.md              # Documentation du projet
├── requirements.txt       # Dépendances
└── .gitignore             # Fichiers à ignorer dans Git
```

---

#  Fonctionnalités principales

###  Détection automatique d’erreurs Python

L’agent exécute un fichier Python avec `subprocess` et récupère :

* stdout,
* stderr,
* code de retour.

###  Analyse de l’erreur

Si une erreur apparaît, elle est envoyée au modèle Mistral via :

```python
ask_mistral_for_fixes()
```

En cas d’échec, un **JSON fallback** est généré pour éviter les crashs.

###  Génération de correctifs

Le modèle renvoie des objets JSON du type :

```json
{
    "file": "sample_buggy.py",
    "action": "replace",
    "line": 4,
    "content": "c = a / b if b != 0 else None",
    "reason": "Prevent division by zero"
}
```

###  Application automatique au fichier

Les actions possibles :

* `replace` : remplacer la ligne,
* `insert_before` : ajouter avant,
* `insert_after` : ajouter après,
* `delete` : supprimer.

###  Interface Web Streamlit

Permet :

* choisir un fichier Python,
* exécuter le script,
* afficher stdout / stderr,
* afficher les correctifs suggérés,
* appliquer les correctifs automatiquement.

---

#  Utilisation

## **1. Lancer la Web App**

```bash
streamlit run web_app.py
```

## **2. Utiliser en CLI**

```bash
python main.py
```

---

