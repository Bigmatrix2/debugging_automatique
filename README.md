1. AUTO-DEBUGGER (Ollama + Streamlit)

Ce projet propose un système complet de **débogage automatique de scripts Python** en utilisant un modèle IA **local**, exécuté via **Ollama**, combiné à une interface utilisateur simple conçue avec **Streamlit**.

Il analyse un script Python, identifie les erreurs d’exécution, génère une explication détaillée, propose des corrections au format JSON strict, et peut appliquer automatiquement ces correctifs au fichier source.

Ce travail est réalisé dans le cadre du module universitaire :  
**"Agent intelligent autonome & automatisation du débogage"**.

---

2. OBECTIFS DU PROJET
- Automatiser le processus de débogage à l’aide d’un LLM
- Exécuter un script Python de manière isolée dans un **environnement virtuel**.
- Capturer les sorties et erreurs d’exécution.
- Soumettre le code et les erreurs au modèle IA pour obtenir une **analyse détaillée**.
- Appliquer les correctifs en respectant un format JSON strict validé par un moteur interne.
- Fournir une interface ergonomique accessible via un navigateur.

---

3. FONCTIONNEMENT GENERAL
L’utilisateur choisit un fichier Python à analyser.**
Le script est exécuté dans un environnement virtuel dédié.
Tout message d’erreur (ex: `ZeroDivisionError`, `NameError`, etc.) est capturé.
Le code source + l’erreur sont envoyés au modèle DeepSeek via Ollama.
L’IA renvoie un JSON strict contenant :
   - une explication complète de l’erreur,
   - une liste de correctifs (ligne, action, contenu).
Le JSON est validé par un système de validation interne.
Si le JSON est valide, l’utilisateur peut cliquer sur **“Appliquer les corrections”**.
Le fichier original est modifié automatiquement.

---

4 ARCHITECTURE DU PROJET

<img width="560" height="727" alt="image" src="https://github.com/user-attachments/assets/140ac1b2-0054-4aa5-90af-0757395266c1" />

5 SYSTEME DE PATCH INTELLIGENT
<img width="690" height="277" alt="image" src="https://github.com/user-attachments/assets/7712fb31-cb30-450e-955b-adec4ae813cd" />

6 LIMITES ET RISQUES
<img width="1032" height="426" alt="image" src="https://github.com/user-attachments/assets/eb386b58-e5a3-4082-a3ee-ae0f63e29d56" />

7 EXEMPLE DE JSON RETOURNE
<img width="861" height="437" alt="image" src="https://github.com/user-attachments/assets/6629fa16-11ed-4ce0-b6e4-6d4d13c23700" />

8 TECHNOLOGIES UTILISEES
Python 3
Streamlit
Ollama
DeepSeek Coder

9 Conclusion
Ce projet démontre comment :
intégrer un LLM local dans un pipeline automatisé, exécuter du code de manière isolée et contrôlée,
mettre en place un moteur de patch fiable, créer une interface complète,
appliquer des principes de validation stricte.
Il constitue un exemple concret d’agent intelligent autonome, capable d’analyser, raisonner et modifier du code.

