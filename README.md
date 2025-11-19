# Agent de Debugging Automatique

Ce projet est un **assistant intelligent de correction de code Python**.  
Il combine **Streamlit** pour l’interface utilisateur, **Ollama** (modèle Llama 3 recommandé) pour l’analyse des erreurs, et un pipeline de validation + correction qui applique les suggestions de l’IA de manière sécurisée.

---

## Objectif du projet

Le but est de faciliter le **debugging automatique** des scripts Python.  
Plutôt que de lire manuellement les erreurs et chercher la solution, l’agent :
1. Exécute ton script dans un environnement virtuel.
2. Capture les erreurs (`stderr`) et le code de sortie.
3. Envoie le code + l’erreur à un modèle IA (via Ollama).
4. Valide la réponse JSON pour s’assurer qu’elle est **parsable et fiable**.
5. Affiche les corrections proposées et une **suggestion finale** de code corrigé.
6. Applique les corrections sur le fichier original, avec **backup automatique**.
7. Si la validation échoue, écrit quand même la suggestion finale dans un fichier `*_corrected.py`.

Ainsi, tu as toujours un fichier corrigé disponible, même si la liste de corrections est incomplète.

---

## Structure du projet

<img width="784" height="312" alt="Capture d&#39;écran 2025-11-19 143816" src="https://github.com/user-attachments/assets/8c7c24c3-1602-4375-be56-01dc6a62766a" />


---

## Installation

1. **Cloner le projet** :
   ```bash
   git clone <repo_url>
   cd <repo_name>
   ```
2. Créer un environnement virtuel :

  python -m venv .venv
  source .venv/bin/activate   # Linux/Mac
  .venv\Scripts\activate      # Windows

3. Installer les dépendances :

   pip install -r requirements.txt

4. Installer Ollama et le modèle Llama 3 :
  
   ollama pull llama3

5. Lancer l’interface Streamlit :
   
   streamlit run main.py








