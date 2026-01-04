from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import os

#Carrega as variáveis de ambiente, para rodar este programa é preciso ter 'OPENAI_API_KEY', 'PGVECTOR_URL', 'PGVECTOR_COLLECTION'
load_dotenv()
for item in ("OPENAI_API_KEY", "PGVECTOR_URL","PGVECTOR_COLLECTION"):
    if not os.getenv(item):
        raise RuntimeError(f"Environment variable {item} is not set")

current_dir = Path(__file__).parent
pdf_path = current_dir / "gpt5.pdf"

loader = PyPDFLoader(pdf_path)
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150, add_start_index=False)
chunks = splitter.split_documents(documents)
if not chunks: #Se não conseguir separar o arquivo vai lançar um erro
    raise SystemExit(0)

enriched = [ #Cria um único documento novo enriquecido com as partes separadas
    Document(
        page_content=document.page_content,
        metadata={ k: v for k, v in document.metadata.items() if v not in ("", None) }
    ) for document in chunks
]    

embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-large")) #Cria um embedding com base no modelo da OpenAI, para vetorizar os dados do document

store = PGVector( #Cria uma collection no PG Vector (DB vetorial com base postgres)
    embeddings=embeddings,                            #Modelo de vetorização
    collection_name=os.getenv("PGVECTOR_COLLECTION"), #Nome da collection que será usada
    connection=os.getenv("PGVECTOR_URL"),             #Link da DB do docker
    use_jsonb=True                                    #Usando JSON Blob para armazenar
)

ids = [ f"doc-{i}" for i in range(len(enriched)) ] #Gera IDs de cada documento para salvar no DB

store.add_documents(documents=enriched, ids=ids) #Salva no DB usando os IDs gerados previamente