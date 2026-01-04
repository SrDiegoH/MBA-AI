from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

load_dotenv()

template = ChatPromptTemplate.from_template("Translate the following text to English:\n ```{initial_text}````") #Cria um template de mensagens a serem passadas na iteração de forma automatica entendendo o que é mensagem e o que é variável. Obs: Usa por padrão o tipo 'human'

messages = template.format_messages(initial_text="LangChain é um framework para desenvolvimento de aplicações de IA")  #Insere as variáveis na mensagem do template
for message in messages:
    print(f"{message.type}: {message.content}")

model = init_chat_model(model="gpt-4.1-mini", model_provider="openai", temperature=0.5)

chat_iterations = model.invoke(messages)
print(chat_iterations.content)