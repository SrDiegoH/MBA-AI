from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv() #Carrega as variáveis de ambiente com as keys do Google e OpenAPI

model = ChatOpenAI(model="gpt-4.1-mini", temperature=0.5) #Carrega o modelo especificamente da OpenAPI. Mais informações sobre 'temperature': https://stackoverflow.com/questions/79480448/what-is-the-default-value-of-temperature-parameter-in-chatopenai-in-langchain. OBS: Usando gpt-4.1-mini para evitar erro de 'insufficient_quota'

chat_iterations = model.invoke("Hello World") #Inicia iteração com o modelo
print(chat_iterations.content) #Mostra no terminal as mensagens da iteração