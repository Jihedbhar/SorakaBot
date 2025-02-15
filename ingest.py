import os
from dotenv import load_dotenv
from langchain_google_cloud_sql_pg import PostgresEngine, PostgresVectorStore
from langchain_google_vertexai import VertexAIEmbeddings

# Configuration
PROJECT_ID = "projet-gcp-450616"
INSTANCE = "soraka-instance"
REGION = "europe-west1"
DATABASE = "health_db"
DB_USER = "postgres"

# Chargement du mot de passe
load_dotenv()
DB_PASSWORD = os.environ["DB_PASSWORD"]

def create_cloud_sql_database_connection() -> PostgresEngine:
    """
    Établit une connexion à Cloud SQL PostgreSQL
    """
    engine = PostgresEngine.from_instance(
        project_id=PROJECT_ID,
        instance=INSTANCE,
        region=REGION,
        database=DATABASE,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    return engine

def get_embeddings() -> VertexAIEmbeddings:
    """
    Récupère une instance de VertexAIEmbeddings
    """
    embeddings = VertexAIEmbeddings(
        model_name="textembedding-gecko@latest",
        project=PROJECT_ID
    )
    return embeddings

def get_vector_store(engine: PostgresEngine, table_name: str, embedding: VertexAIEmbeddings) -> PostgresVectorStore:
    """
    Récupère le vector store
    """
    vector_store = PostgresVectorStore.create_sync(
        engine=engine,
        table_name=table_name,
        embedding_service=embedding,
    )
    return vector_store

if __name__ == '__main__':
        try:
            print("Testing database connection...")
            engine = create_cloud_sql_database_connection()
            print("✓ Database connection successful")

            print("\nTesting embeddings configuration...")
            embeddings = get_embeddings()
            print("✓ Embeddings configuration successful")

            print("\nTesting vector store access...")
            vector_store = get_vector_store(engine, "medical_qa", embeddings)
            
            # Test simple query to verify everything works
            test_query = "What is glaucoma?"
            results = vector_store.similarity_search_with_score(test_query, k=1)
            if len(results) > 0:
                print("✓ Vector store access successful")
                print(f"✓ Successfully retrieved {len(results)} result(s)")
                doc, score = results[0]
                print("\nSample result:")
                print(f"Question: {doc.page_content}")
                print(f"Score: {score}")
            else:
                print("! No results found in vector store")

            print("\nAll tests completed successfully!")

        except Exception as e:
            print(f"\n❌ Error during testing: {str(e)}")