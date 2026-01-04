from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = WebBaseLoader("https://www.langchain.com/") #Cria crawler que lê o site
documents = loader.load() #Lê o site e transforma em uma lista de documents, com conteúdo da página e metadados
print(documents) #Mostra no terminal os dados do document
print("=" * 60)

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(documents)
for chunk in chunks:
    print(chunk)
    print("-" * 30)