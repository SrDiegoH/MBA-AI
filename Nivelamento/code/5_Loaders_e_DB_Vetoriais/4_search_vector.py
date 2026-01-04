from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
import os

load_dotenv()
for item in ("OPENAI_API_KEY", "PGVECTOR_URL","PGVECTOR_COLLECTION"):
    if not os.getenv(item):
        raise RuntimeError(f"Environment variable {item} is not set")

embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-large"))

store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PGVECTOR_COLLECTION"),
    connection=os.getenv("PGVECTOR_URL"),
    use_jsonb=True
)

query = "Tell me more about the gpt-5 thinking evaluation and performance results comparing to gpt-4"

response = store.similarity_search_with_score(query, k=3) #Busca no DB usando a query, retornando os vetores com maior similiaridade e seu score

for i, (document, score) in enumerate(response, start=1):
    print(f"Resultado {i} (score: {score:.2f}):") #Mostra no terminal o indice e a pontuação da resposta
    print("=" * 60)

    print("\nTexto:\n")
    print(document.page_content.strip()) #Mostra no terminal o texto da resposta

    print("\nMetadados:\n")
    for key, value in document.metadata.items(): #Mostra no terminal os metadados da resposta
        print(f"{key}: {value}")

    print("=" * 60)