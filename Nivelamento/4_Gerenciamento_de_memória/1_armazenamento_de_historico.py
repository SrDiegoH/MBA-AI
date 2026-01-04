
'''
Uma vez que as LLMs são stateless, ou seja, eles não guardam informações do estado (histórico), precisamos contornar
essa limitação salvando as mensagens anteriores e de preferência sumarizadas (Visto no Módulo 2 - Chains e Processamento)
na memória RAM, banco, cache dentre outras formas, e passá-las na iteração atual.
'''

from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model(model="gpt-4.1-mini", model_provider="openai", temperature=0.9)

template = ChatPromptTemplate([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"), #Mensagem genérica para receber prompts qualquer com variáveis definidas, é semelhante a fazer "{variable_name}"
    ("human", "{input}")
])

chain = template | model

#Cria uma sessão (com padrão singelton) cuja a chave é um ID qualquer e o valor o dado na memória RAM
session_store: dict[str, InMemoryChatMessageHistory] = {}
def get_session_history(session_id):
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory() #Salva na memória RAM

    return session_store[session_id]

chain_history = RunnableWithMessageHistory(  #Cria um chain que guarda o histórico da conversa usando uma sessão
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

config = { #Configuração extra com a informação do ID da sessão
    "configurable": {
        "session_id": "demo-session"
    }
}

response1 = chain_history.invoke( {"input": "Hello, my name is Diego. How are you?" }, config=config) #Inicia processamento da chain, usando a configuração com informação do ID da session e dessa forma salvando o histórico. Aqui ele recebe informação do nome e salva no histórico
print("Assistant: ", response1.content) #Mostra no terminal o resultado final do processo
print("-" * 30)  #Apenas um separador das próximas chamadas

response2 = chain_history.invoke({ "input": "Can you repeat my name and a say random colour?" }, config=config) #Chama a chain novamente, dessa vez pedindo para mencionar o nome salvo no histórico e salvando uma cor no histórico
print("Assistant: ", response2.content)
print("-" * 30)

response3 = chain_history.invoke({ "input": "Can you repeat my name in a motivation phrase?" }, config=config) #Chama a chain mais uma vez, sem mencionar a cor
print("Assistant: ", response3.content)
print("-" * 30)

response4 = chain_history.invoke({ "input": "Witch colour did you said?" }, config=config) #Chama a chain pela última vez, perguntando sobre a cor salva no histórico
print("Assistant: ", response4.content)