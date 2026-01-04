from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai") #Carrega o modelo de forma genérica, neste caso passando o modelo do Google

chat_iterations = model.invoke("Hello World")
print(chat_iterations.content)