from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

load_dotenv()

system = ("system", "you are an assistant that answers questions in a {style} style") #Mensagem inicial do sistema, dando as configurações de como a LLM deve agir
user = ("user", "{question}") #Mensagens do usuario

template = ChatPromptTemplate([ system, user ]) #Cria um template de mensagens a serem passadas na iteração. Recebe tuplas onde o primeiro valor é o tipo da mensagem e o segundo, o conteúdo

messages = template.format_messages(style="funny", question="Who is Alan Turing?")  #Insere as variáveis na mensagem do template
for message in messages: #Mostra no terminal as mensagems do template em detalhes e formatadas com as variáveis
    print(f"{message.type}: {message.content}")

model = init_chat_model(model="gpt-4.1-mini", model_provider="openai", temperature=0.5)

chat_iterations = model.invoke(messages)
print(chat_iterations.content)