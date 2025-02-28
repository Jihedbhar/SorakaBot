# SorakaBot - Assistant Médical Intelligent

## Description
SorakaBot est un assistant médical virtuel intelligent basé sur un système RAG (Retrieval-Augmented Generation). Il combine une base de connaissances médicales structurée avec les capacités de génération de texte du modèle Gemini pour fournir des réponses précises et contextualisées aux questions médicales.

## Architecture
Le projet est divisé en deux parties principales :

- **API Backend (FastAPI)** : Gère la logique de recherche et génération des réponses
- **Interface Utilisateur (Streamlit)** : Fournit une interface conviviale pour interagir avec l'assistant

## Composants principaux
- Base de données vectorielle PostgreSQL avec **pgvector** sur Google Cloud SQL
- Embeddings générés via **VertexAI textembedding-gecko**
- Modèle de langage **Gemini 1.5 Pro** pour la génération de texte
- Dataset **MedQuAD** (Medical Question-Answering Dataset) comme base de connaissances

## Fonctionnalités
- 🔍 Recherche sémantique dans une base de données médicale
- 💬 Réponses précises basées sur des sources fiables
- 🌐 Interface multilingue (Français, Anglais, Arabe)
- 🔄 Conservation du contexte des conversations
- 📊 Affichage des sources et scores de confiance

## Installation et Configuration

### Prérequis
- Python 3.10+
- Compte Google Cloud Platform avec API Vertex AI activée
- Instance Cloud SQL PostgreSQL
- Clé API Gemini

### Installation locale
1. Cloner le dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/sorakabot.git
   cd sorakabot

2. Créer un environnement virtuel :
    ```bash
    python -m venv venv
    source venv/bin/activate   # Sur Windows: venv\Scripts\activate

3. Installer les dépendances :
    ```bash
    pip install -r requirements.txt

4. Configurer les variables d'environnements : 
    ```bash
    # .env
    API_KEY=votre_clé_api_gemini
    DB_PASSWORD=votre_mot_de_passe_db

6. Télécharger et lancer le proxy Cloud SQL :
    ```bash
    # Dans un terminal
    
    ./cloud-sql-proxy.exe projet-gcp-450616:europe-west1:soraka-instance

8. Lancer l'API et l'interface utilisateur :
    ```bash
    # Dans un terminal
    python api.py

    # Dans un autre terminal
    streamlit run app.py


## Evaluation 

Les performances du système ont été évaluées selon plusieurs métriques :

- Pertinence moyenne : 0.7297

- Temps de réponse moyen : 0.1036 seconde

- Taux de récupération DB : Mesure la qualité de la récupération d'information

## Limitations

- Performance limitée sur les questions très spécifiques non présentes dans la base de données

- Nécessite une formulation claire des questions

- Informations potentiellement incomplètes sur des sujets médicaux émergents

## Structure du projet

sorakabot/
├── api.py                  # API FastAPI
├── app.py                  # Interface Streamlit
├── ingest.py               # Gestion de l'ingestion des données
├── retrieve.py             # Fonctions de récupération des données
├── utils_eval.py           # Outils d'évaluation du système
├── eval.py                 # Script d'évaluation
├── config.py               # Configuration du projet
├── requirements.txt        # Dépendances Python
├── Dockerfile_api          # Dockerfile pour l'API
├── Dockerfile_streamlit    # Dockerfile pour l'interface
└── downloaded_files/       # Fichiers téléchargés


## Considérations éthiques



- SorakaBot est un outil d'information et ne remplace en aucun cas une consultation médicale professionnelle

- Les sources et scores de confiance sont systématiquement affichés

- Aucune donnée utilisateur n'est stockée de manière permanente

## Licence
Ce projet est sous licence MIT.

## Contact

Pour toute question ou suggestion, veuillez me contacter à bharjihed@gmail.com 










