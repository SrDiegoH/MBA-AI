from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

#Gera o caminho para o arquivo PDF
current_dir = Path(__file__).parent
pdf_path = current_dir / "gpt5.pdf"

loader = PyPDFLoader(pdf_path) #Cria crawler que lê o site
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(documents)
print(len(chunks)) #Mostra no terminal a quantidade de partes divididas. Obs: Como o PDF é grande, não vou mostrar no terminal