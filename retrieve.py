import os
from ingest import create_cloud_sql_database_connection, get_embeddings, get_vector_store
from langchain_google_cloud_sql_pg import PostgresVectorStore
from langchain_core.documents.base import Document
from config import TABLE_NAME

def get_relevant_documents(query: str, vector_store: PostgresVectorStore) -> list[Document]:
    """
    Retrieve the most relevant document based on a medical query using a vector store.
    
    Args:
        query (str): The medical question.
        vector_store (PostgresVectorStore): An instance of PostgresVectorStore.
    
    Returns:
        list[Document]: A list containing only the most relevant document.
    """
    # Utiliser similarity_search_with_score pour avoir les scores
    results = vector_store.similarity_search_with_score(
        query,
        k=4  # On peut garder k=4 pour avoir un choix mais ne prendre que le meilleur
    )
    
    # Trier par score (plus petit score = plus grande similarité)
    sorted_results = sorted(results, key=lambda x: x[1])
    
    # Ne retourner que le document le plus pertinent
    best_doc = sorted_results[0][0] if sorted_results else None
    return [best_doc] if best_doc else []

def format_relevant_documents(documents: list[Document]) -> str:
    """
    Format medical documents into a readable string.

    Args:
        documents (list[Document]): A list of medical QA documents.

    Returns:
        str: Formatted string with questions, answers, and sources.

    Example:
        >>> documents = [
            Document(page_content: "What is diabetes?", 
                    metadata: {"answer": "Diabetes is...", "source": "NIH", "focus_area": "Diabetes"})
        ]
        >>> doc_str = format_relevant_documents(documents)
        >>> '''
            Question 1: What is diabetes?
            Answer: Diabetes is...
            Source: NIH
            Focus Area: Diabetes
            -----
        '''
    """
    formatted_docs = []
    for i, doc in enumerate(documents):
        formatted_doc = (
            f"Question {i+1}: {doc.page_content}\n"
            f"Answer: {doc.metadata['answer']}\n"
            f"Source: {doc.metadata['source']}\n"
            f"Focus Area: {doc.metadata['focus_area']}\n"
            "-----"
        )
        formatted_docs.append(formatted_doc)
    return "\n".join(formatted_docs)

if __name__ == '__main__':
    engine = create_cloud_sql_database_connection()
    embedding = get_embeddings()
    vector_store = get_vector_store(engine, TABLE_NAME, embedding)
    
    test_query = "What is fever?"
    documents = get_relevant_documents(test_query, vector_store)
    
    # Ajoutons un print du score
    results = vector_store.similarity_search_with_score(test_query, k=1)
    if results:
        score = results[0][1]
        print(f"Score de similarité : {score}\n")
    
    doc_str = format_relevant_documents(documents)
    print("Document le plus pertinent :")
    print(doc_str)
    print("\nTest passed successfully.")