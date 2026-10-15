# ERP DigiPrint — prototype Streamlit

## Lancement
1. Installer Python 3.10+.
2. Dans le dossier du projet, exécuter `pip install -r requirements.txt`.
3. Lancer `streamlit run app.py`.
4. Ouvrir l'adresse locale fournie dans le terminal.

## Contenu
- `app.py` : application de démonstration avec navigation par modules.
- `requirements.txt` : dépendances.

## Limites générales
Les données sont fictives et conservées en mémoire de session. Le prototype n'a ni base de données persistante, ni authentification réelle, ni autorisations serveur, ni audit inviolable, ni intégration machine, transporteur, e-mail, comptabilité ou FNE. Il ne doit pas être utilisé pour les opérations réelles.

Avant une mise en production : valider les processus avec chaque service, concevoir le modèle relationnel et ses contraintes, connecter une base de données, mettre en place les rôles côté serveur, sauvegardes, tests, supervision et validation des règles fiscales/comptables applicables en Côte d'Ivoire.
