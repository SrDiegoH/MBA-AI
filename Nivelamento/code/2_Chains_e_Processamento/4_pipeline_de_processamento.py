from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model(model="gpt-4.1-mini", model_provider="openai", temperature=0)

#Exemplo de pipeline
#Cadeia de execução - Translate: Traduzir de qualquer lingua para o inglês (e ser usado em modelos que trabalham nessa lingua) e transforma o retorno em String
template_translate = ChatPromptTemplate(("initial_text", "Translate the following text to English:\n ```{initial_text}````"))
chain_translate = template_translate | model | StrOutputParser()

#Cadeia de execução - Summarize: Resume uma entrada em 4 palavras. Neste caso recebe de entrada um dict cuja a key é a variável do 'template_summary' e o value é a chain resultado do 'chain_translate', por fim transforma o retorno em String
template_summary = ChatPromptTemplate(("text", "Summarize the following text in 4 words:\n ```{text}```"))
chain_sumary = template_summary | model | StrOutputParser()

#Cadeia de execução - Main: Pipeline principal que chama as outras
prepare_summary_inputs_runner = RunnableLambda(lambda text: { "text": text }) #Runner para converter a saida do 'chain_translate' para ser usado na 'chain_sumary'
chain_pipeline = chain_translate | prepare_summary_inputs_runner | chain_sumary

result = chain_pipeline.invoke({ "initial_text": "LangChain é um framework para desenvolvimento de aplicações de IA" }) #Inicia processamento da 'chain_pipeline', passando a entrada da primeira chain
print(result) #Mostra no terminal o resultado do processo, neste caso não usamos 'content' pois o final da chain é convertido para String