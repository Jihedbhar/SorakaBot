import pandas as pd
import numpy as np
import requests
from utils_eval import calculate_relevance, was_answer_found_in_db, display_evaluation_results
import time

def load_random_samples(n=10):
    """Charge n exemples aléatoires du dataset"""
    df = pd.read_csv("./downloaded_files/medquad.csv")
    # Nettoyer les questions (supprimer les "? ?" ou espaces multiples)
    df['question'] = df['question'].str.replace(r'\s*\?\s*\?', '?', regex=True).str.strip()
    return df.sample(n=n, random_state=42)

def get_chatbot_response(question: str) -> dict:
    """
    Appelle l'API déployée sur Cloud Run pour obtenir une réponse.
    """
    url = "https://mjb-api-217448161611.europe-west1.run.app/answer"
    payload = {
        "question": question,
        "temperature": 0.5,
        "language": "en",
        "session_id": ""  # Champ optionnel, laissé vide
    }
    try:
        start_time = time.time()
        response = requests.post(url, json=payload, timeout=60)  # Timeout à 60s pour cold starts
        response_time = time.time() - start_time
        
        if response.ok:
            json_data = response.json()
            message = json_data.get("message", "")
            
            # Parser le message pour extraire les champs
            response_text = message.split("Pour plus de détails :")[0].replace("Réponse: ", "").strip() if "Pour plus de détails :" in message else message
            db_answer = message.split("Pour plus de détails :\n")[1].split("\nSource :")[0].strip() if "Pour plus de détails :" in message else ""
            source = json_data.get("metadata", {}).get("source", "") or (message.split("Source : ")[1].split("\n")[0].strip() if "Source :" in message else "")
            focus_area = json_data.get("metadata", {}).get("focus_area", "") or (message.split("Domaine médical : ")[1].split("\n")[0].strip() if "Domaine médical :" in message else "")
            score = float(json_data.get("metadata", {}).get("similarity_score", "0.0")) or float(message.split("Score de similarité : ")[1].strip() if "Score de similarité :" in message else "0.0")
            response_type = "combined_response" if "Pour plus de détails :" in message else "llm_response"
            
            return {
                "response": response_text,
                "db_answer": db_answer,
                "source": source,
                "focus_area": focus_area,
                "score": score,
                "type": response_type,
                "response_time": response_time
            }
        else:
            print(f"Erreur HTTP {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"Erreur lors de la requête: {str(e)}")
        return None

def evaluate_response(question, true_answer, chatbot_response):
    """Évalue une réponse du chatbot"""
    if chatbot_response is None:
        return {
            "relevance_score": 0.0,
            "retrieval_success": False,
            "response_time": 0.0
        }
    
    metrics = {
        "relevance_score": calculate_relevance(chatbot_response, true_answer),
        "retrieval_success": was_answer_found_in_db(chatbot_response),
        "response_time": chatbot_response["response_time"]
    }
    return metrics

def main():
    samples = load_random_samples(10)
    results = []
    for _, row in samples.iterrows():
        question = row['question']
        true_answer = row['answer']
        chatbot_response = get_chatbot_response(question)
        metrics = evaluate_response(question, true_answer, chatbot_response)
        results.append({
            "question": question,
            "true_answer": true_answer,
            "chatbot_response": chatbot_response,
            **metrics
        })
    display_evaluation_results(results)

if __name__ == "__main__":
    main()