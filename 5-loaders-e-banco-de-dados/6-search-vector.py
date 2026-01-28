import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

for k in ("OPENAI_API_KEY", "PGVECTOR_URL", "PGVECTOR_COLLECTION"):
    if not os.getenv(k):   
        raise ValueError(f"Environment variable {k} is not set")    

query = "Quando desenvolvemos um software podemos usar o circuit breaker como um"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = PGVector(
    embeddings=embeddings,
    connection=os.getenv("PGVECTOR_URL"),
    collection_name=os.getenv("PGVECTOR_COLLECTION"),
    use_jsonb=True
)

results = vector_store.similarity_search_with_score(query, k=10)

for i, (doc, score) in enumerate(results, start=1):
    print("=" * 50)
    print(f"Documento {i}:")
    print("=" * 50)
    print(f"Texto do documento:\n{doc.page_content}")    
    print(f"\nSimilaridade: {score:.4f}")
    print("-" * 50)