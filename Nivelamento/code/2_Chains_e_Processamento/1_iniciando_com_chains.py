from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

load_dotenv()

template = ChatPromptTemplate(("name", "Hi, I'm {name}! Tell me a joke with my name!"))

model = init_chat_model(model="gpt-4.1-mini", model_provider="openai", temperature=0.5)

chain = template | model #Cria uma cadeia de execução (chain) onde o resultado do primeiro é passado como entrada para o próximo e assim por diante, neste caso template é passado como entrada para o modelo

result = chain.invoke({ "name": "Diego" }) #Inicia processamento da chain (com iteração com o modelo), começando pelo template recebendo como entrada um dict, passando o retorno do template para o modelo e por último o modelo retorna com a mensagem final salva em content
print(result.content) #Mostra no terminal o resultado final do processo