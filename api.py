from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import google.generativeai as genai
from ingest import create_cloud_sql_database_connection, get_embeddings, get_vector_store
from retrieve import get_relevant_documents, format_relevant_documents
from config import TABLE_NAME

load_dotenv()
API_KEY = os.getenv('API_KEY')
genai.configure(api_key=API_KEY)

app = FastAPI(
    title="SorakaBot API",
    description="API pour l'assistant médical SorakaBot",
    version="1.0.0"
)

class UserInput(BaseModel):
    question: str
    temperature: float
    language: str
    previous_context: List[dict] = []

def get_llm(temperature: float = 0.3):
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=API_KEY,
        temperature=temperature,
        verbose=True
    )


# Initialisation des connexions aux services
engine = create_cloud_sql_database_connection()
embedding = get_embeddings()
vector_store = get_vector_store(engine, TABLE_NAME, embedding)

@app.get("/")
async def root():
    return {"status": "SorakaBot API is running"}

@app.post("/answer")
async def answer(user_input: UserInput):
    try:
        results = vector_store.similarity_search_with_score(user_input.question, k=1)
        if results:
            doc, score = results[0]
            
            if score < 0.2:  # Bonne correspondance
                # D'abord obtenir une réponse ciblée de Gemini
                llm = get_llm(user_input.temperature)
                prompt = ChatPromptTemplate.from_messages([
                    (
                        "system",
                        """Tu es SorakaBot, un assistant médical virtuel spécialisé.
                        Voici une réponse de référence : {reference_answer}
                        
                        Utilise cette information pour répondre de manière précise à la question suivante en {language}.
                        Sois concis et direct dans ta réponse.
                        
                        Question: {question}"""
                    ),
                    ("human", "{question}")
                ])
                
                chain = prompt | llm
                llm_response = chain.invoke({
                    "language": user_input.language,
                    "question": user_input.question,
                    "reference_answer": doc.metadata['answer']
                })
                
                return {
                    "message": f"""Réponse: {llm_response.content}

Pour plus de détails :
{doc.metadata['answer']}

Source : {doc.metadata['source']}
Domaine médical : {doc.metadata['focus_area']}
Score de similarité : {score:.4f}""",
                    "metadata": {
                        "source": doc.metadata['source'],
                        "focus_area": doc.metadata['focus_area'],
                        "similarity_score": f"{score:.4f}"
                    }
                }
            else:  # Pas de bonne correspondance - laisser Gemini répondre librement
                llm = get_llm(user_input.temperature)
                prompt = ChatPromptTemplate.from_messages([
                    (
                        "system",
                        """Tu es SorakaBot, un assistant médical virtuel spécialisé.
                        
Réponds à la question de manière claire et précise en {language}.
Base ta réponse sur tes connaissances médicales générales.
N'oublie pas de recommander de consulter un professionnel de santé si nécessaire.

Question: {question}"""
                    ),
                    ("human", "{question}")
                ])
                
                chain = prompt | llm
                response = chain.invoke({
                    "language": user_input.language,
                    "question": user_input.question
                })

                return {
                    "message": response.content
                }

    except Exception as e:
        print(f"Erreur détaillée: {str(e)}")
        return {
            "message": "Une erreur s'est produite lors du traitement de votre demande.",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8181)