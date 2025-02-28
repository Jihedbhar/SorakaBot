import numpy as np
import time
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def cosine_similarity_texts(text1: str, text2: str) -> float:
    """
    Calcule la similarité cosinus entre deux textes.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

def calculate_relevance(chatbot_response, true_answer):
    if not chatbot_response:
        return 0.0
    
    if chatbot_response.get('type') == 'combined_response':
        # Évaluer la réponse générée par rapport à la réponse de référence
        llm_similarity = cosine_similarity_texts(chatbot_response['response'], chatbot_response['db_answer'])
        # Retourner une métrique qui prend en compte à la fois la similarité et le score original
        return (llm_similarity + (1 - float(chatbot_response['score']))) / 2
    else:
        return cosine_similarity_texts(chatbot_response.get('response', ''), true_answer)

def was_answer_found_in_db(chatbot_response):
    """
    Vérifie si une réponse a été trouvée dans la base de données
    """
    if not chatbot_response:
        return False
    return chatbot_response.get('type') == 'database_match'

def measure_response_time(get_response_function, question):
    """
    Mesure le temps de réponse du chatbot
    
    Args:
        get_response_function: La fonction qui génère la réponse
        question: La question posée
    """
    start_time = time.time()
    response = get_response_function(question)
    return time.time() - start_time, response

def display_evaluation_results(results):
    """
    Affiche les résultats de l'évaluation
    """
    print("\nRésultats de l'évaluation sur 10 exemples aléatoires :")
    print("-" * 50)
    
    # Calcul des moyennes
    avg_metrics = {
        "Pertinence moyenne": np.mean([r["relevance_score"] for r in results]),
        "Taux de récupération DB": np.mean([r["retrieval_success"] for r in results]),
        "Temps de réponse moyen": np.mean([r["response_time"] for r in results])
    }
    
    # Affichage des métriques moyennes
    for metric, value in avg_metrics.items():
        print(f"{metric}: {value:.4f}")
    
    # Affichage de quelques exemples détaillés
    print("\nExemples détaillés (5 premiers) :")
    for i, result in enumerate(results[:5], 1):
        print(f"\nExemple {i}:")
        print(f"Question: {result['question']}")
        print(f"Type de réponse: {result['chatbot_response'].get('type', 'unknown')}")
        print(f"Score de similarité: {result['chatbot_response'].get('score', 'N/A')}")
        print(f"Pertinence: {result['relevance_score']:.4f}")

        gcloud run deploy sorakabot \
    --image=europe-west1-docker.pkg.dev/projet-gcp-450616/sorakabot-repo/mjb-api:latest \
    --platform=managed \
    --region=europe-west1 \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_API_KEY="AIzaSyA0BJ-l4g5TYK-Gd0fvK6lJMUIroDsr1rI",DB_PASSWORD="C+B[Q&<07bheSc,n" \ 
    --port 8181