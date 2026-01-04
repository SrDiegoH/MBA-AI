from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import chain
from langchain.chat_models import init_chat_model

load_dotenv()

@chain #Anotação que faz com que a função possa ser usada em uma chain 
def square(input_dict): #Função para fins didáticos, neste caso recebe como entrada um dict, mas pode receber o que for, portanto que seja passado assim na chain
    x = input_dict["x"]
    return { "square_result": x * x }

template = ChatPromptTemplate(("square_result", "Tell me about the number {square_result}"))

model = init_chat_model(model="gpt-4.1-mini", model_provider="openai", temperature=0.5)

chain = square | template | model

result = chain.invoke({ "x": 10 }) #Inicia processamento da chain, começando pelo square recebendo como entrada um dict, passando o retorno para o template, e seu resoltado para o modelo e por fim retorna com a mensagem final
print(result.content)