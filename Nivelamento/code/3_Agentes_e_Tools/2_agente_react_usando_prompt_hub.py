from dotenv import load_dotenv
from langchain_classic import hub
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
load_dotenv()

model = init_chat_model(model="gpt-4.1-mini", model_provider="openai", temperature=0.5)

@tool("calculator", return_direct=True)
def calculator(expression):
    """Evaluate a simple mathematical expression and return the result as a string."""
    try:
        result = eval(expression)
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

tools = [ calculator, web_search_mock ]

#Prompt obtido no hub, que funciona como um github de prompts. Mais detalhes sobre o hub: https://smith.lanchain.com/hub. Obs: Diferentes modelos tem resultados diferentes para um mesmo prompt, sempre que mudar o modelo precisamos testar tudo novamente
prompt = hub.pull("hwchase17/react")

chain_agent = create_react_agent(model, tools, prompt, stop_sequence=False)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=chain_agent,
    tools=tools,
    verbose=True,
    max_iterations=3
)

print(agent_executor.invoke({"input": "What is the capital of Brazil?"}))
print(agent_executor.invoke({"input": "What is the capital of Iran?"}))
print(agent_executor.invoke({"input": "How much is 10 + 10?"}))