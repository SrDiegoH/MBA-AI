from dotenv import load_dotenv
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain.tools import tool

load_dotenv()

model = init_chat_model(model="gpt-4.1-mini", model_provider="openai", disable_streaming=False) #Por padrão o 'disable_streaming' vem True, usar streaming pode causar erros em outros modelos

@tool("calculator", return_direct=True) #Anotação informando que essa função pode ser usada como ferramenta pelo modelo duranto o processamento
def calculator(expression):
    """Evaluate a simple mathematical expression and return the result as a string.""" #Usa doc block como prompt para dizer ao modelo o que a função faz e como ele pode usar
    try:
        result = eval(expression) #Eval pode ser um risco de segurança para a IA pois recebe qualquer texto de entrada, não apenas um texto matemático
    except Exception as e:
        return f"Error: {e}"

    return str(result)

@tool("web_search_mock")
def web_search_mock(query):
    """Return the capital of a given country if it exists in the mock data."""
    data = {
        "Brazil": "Brasília",
        "France": "Paris",
        "Germany": "Berlin",
        "Italy": "Rome",
        "Spain": "Madrid",
        "United States": "Washington, D.C."
    }

    for country, capital in data.items():
        if country.lower() in query.lower():
            return f"The capital of {country} is {capital}."

    return "I don't know the capital of that country."

tools = [ calculator, web_search_mock ] #Lista de ferramental a ser usado pelo modelo

#Exemplo de prompt informando as tools a serem usadas, formato de resposta, regras e entradas. Nota-se que as regras dizem para evitar usar a internet a fim de usar o 'web_search_mock'
template = ChatPromptTemplate.from_template("""
Answer the following questions as best you can. You have access to the following tools.
Only use the information you get from the tools, even if you know the answer.
If the information is not provided by the tools, say you don't know.

{tools}

Use the following format:

Question: The input question you must answer
Thought: You should always think about what to do
Action: The action to take, should be one of [{tool_names}]
Action Input: The input to the action
Observation: The result of the action

... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: The final answer to the original input question

Rules:
- If you choose an Action, do NOT include Final Answer in the same step.
- After Action and Action Input, stop and wait for Observation.
- Never search the internet. Only use the tools provided.

Begin!

Question: {input}
Thought:{agent_scratchpad}
""")

chain_agent = create_react_agent(model, tools, template, stop_sequence=False) #Cria um chain que aceita ferramentas

agent_executor = AgentExecutor.from_agent_and_tools( #Cria agente de execução que usa a chain, tools, prompt e formato de erro
    agent=chain_agent,
    tools=tools,
    verbose=True, #Informa o pensamento do modelo durante o processamento
    handle_parsing_errors="Invalid format. Either provide an Action with Action Input, or a Final Answer only.", #Este prompt evita tentar resolver os inputs que ele não sabe usando os dados pré-carregado no modelo (durante o treinamento)
    max_iterations=5 #Máximo de iterações para evitar que o modelo trave em loop
)

print(agent_executor.invoke({"input": "What is the capital of Brazil?"})) #Mostra no terminal o resultado da execução do agente
print(agent_executor.invoke({"input": "What is the capital of Iran?"}))
print(agent_executor.invoke({"input": "How much is 10 + 10?"}))