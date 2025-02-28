import pandas as pd
import numpy as np
from api import get_llm, vector_store  # importez vos fonctions existantes
import random
from langchain_core.prompts import ChatPromptTemplate
from utils_eval import calculate_relevance, was_answer_found_in_db, measure_response_time,display_evaluation_results

def load_random_samples(n=10):
    """Charge n exemples aléatoires du dataset"""
    df = pd.read_csv("./downloaded_files/medquad.csv")
    return df.sample(n=n, random_state=42)  # random_state pour reproductibilité

def evaluate_response(question, true_answer, chatbot_response):
    """Évalue une réponse du chatbot"""
    metrics = {
        "relevance_score": calculate_relevance(chatbot_response, true_answer),
        "retrieval_success": was_answer_found_in_db(chatbot_response),
        "response_time": measure_response_time()
    }
    return metrics

def get_chatbot_response(question: str) -> dict:
    """
    Version simplifiée de la fonction answer de l'API pour l'évaluation
    """
    try:
        results = vector_store.similarity_search_with_score(question, k=1)
        if results:
            doc, score = results[0]
            
            if score < 0.2:  # Bonne correspondance
                # Obtenir une réponse ciblée de Gemini
                llm = get_llm(temperature=0.5)
                prompt = ChatPromptTemplate.from_messages([
                    (
                        "system",
                        """Tu es SorakaBot, un assistant médical virtuel spécialisé.
                        Voici une réponse de référence : {reference_answer}
                        
                        Utilise cette information pour répondre de manière précise à la question suivante.
                        Sois concis et direct dans ta réponse.
                        
                        Question: {question}"""
                    ),
                    ("human", "{question}")
                ])
                
                chain = prompt | llm
                llm_response = chain.invoke({
                    "question": question,
                    "reference_answer": doc.metadata['answer']
                })
                
                return {
                    "response": llm_response.content,
                    "db_answer": doc.metadata['answer'],
                    "source": doc.metadata['source'],
                    "focus_area": doc.metadata['focus_area'],
                    "score": score,
                    "type": "combined_response"  # Nouveau type pour cette approche
                }

            else:  # Réponse Gemini
                llm = get_llm(temperature=0.5)
                prompt = ChatPromptTemplate.from_messages([
                    (
                        "system",
                        """Tu es SorakaBot, un assistant médical virtuel spécialisé.
                        Réponds à la question de manière claire et précise.
                        Question: {question}"""
                    ),
                    ("human", "{question}")
                ])
                
                chain = prompt | llm
                response = chain.invoke({
                    "question": question
                })
                
                return {
                    "response": response.content,
                    "score": score,
                    "type": "llm_response"
                }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None




def main():
    # Charger 10 exemples aléatoires
    samples = load_random_samples(10)
    
    results = []
    for _, row in samples.iterrows():
        question = row['question']
        true_answer = row['answer']
        
        # Obtenir la réponse du chatbot
        response_time, chatbot_response = measure_response_time(get_chatbot_response,question)
        
        # Évaluer la réponse
        metrics = {
        "relevance_score": calculate_relevance(chatbot_response, true_answer),
        "retrieval_success": was_answer_found_in_db(chatbot_response),
        "response_time": response_time
    }
        
        results.append({
            "question": question,
            "true_answer": true_answer,
            "chatbot_response": chatbot_response,
            **metrics
        })
    
    # Calculer et afficher les métriques moyennes
    display_evaluation_results(results)

if __name__ == "__main__":
    main()