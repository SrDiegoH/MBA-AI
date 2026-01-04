from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model(model="gpt-4.1-mini", model_provider="openai", temperature=0.9)

template = ChatPromptTemplate([
    ("system", "You're a helpful assistant that answers with a short joke when possible."),
    MessagesPlaceholder("history"),
    ("human", "{input}")
])

#Função configurando slide window
def prepare_inputs(payload):
    raw_history = payload.get("raw_history", [])

    trimmed = trim_messages(
        raw_history,
        token_counter=len,   #Usando 'len' faz o modelo trabalhar com mensagens invéz de quantidade de tokens
        max_tokens=2,        #Slide Window de 2 mensagens
        strategy="last",     #Trabalha com as últimas mensagens para evitar seja perdida a última iteração com o usuário
        start_on="human",
        include_system=True, #O prompt inicial de sistema (ln 14) sempre vai aparecer, evitando que a instrução incial se perca
        allow_partial=False  #Pega uma de cada vez
    )

    return {
        "input": payload.get("input",""),
        "history": trimmed
    }
prepare = RunnableLambda(prepare_inputs) #Transforma o slide window para ser usado na chain

chain = prepare | template | model #Cria chain com slide window de 2 úlimas mensagens sem perder a instrução incial

session_store: dict[str, InMemoryChatMessageHistory] = {}
def get_session_history(session_id):
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()

    return session_store[session_id]

conversational_chain = RunnableWithMessageHistory( #Criando um chain que usa historico de mensagens
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="raw_history"
)

config = {
    "configurable": {
        "session_id": "demo-session" 
    }
}

response1 = conversational_chain.invoke({ "input": "My name is Diego. Reply only with 'OK' and do not mention my name." }, config=config)
print("Assistant:", response1.content)

response2 = conversational_chain.invoke({ "input": "Tell me a one-sentence fun fact. Do not mention my name." }, config=config) 
print("Assistant:", response2.content)

response3 = conversational_chain.invoke({ "input": "What is my name?" }, config=config) #Chama a chain pela terceira vez, como o slide window é de 2 mensagens a primeira é jogada fora perdendo a informação do nome
print("Assistant:", response3.content)