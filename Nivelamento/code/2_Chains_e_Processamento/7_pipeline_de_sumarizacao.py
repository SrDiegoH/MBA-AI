from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chat_models import init_chat_model

load_dotenv()

long_text = """
Dawn threads a pale gold through the alley of glass.
The city yawns in a chorus of brakes and distant sirens.
Windows blink awake, one by one, like sleepy eyes.
Streetcloth of steam curls from manholes, a quiet river.
Coffee steam spirals above a newspaper's pale print.
Pedestrians sketch light on sidewalks, hurried, loud with umbrellas.
Buses swallow the morning with their loud yawns.
A sparrow perches on a steel beam, surveying the grid.
The subway sighs somewhere underground, a heartbeat rising.
Neon still glows in the corners where night refused to retire.
A cyclist cuts through the chorus, bright with chrome and momentum.
The city clears its throat, the air turning a little less electric.
Shoes hiss on concrete, a thousand small verbs of arriving.
Dawn keeps its promises in the quiet rhythm of a waking metropolis.
The morning light cascades through towering windows of steel and glass,
casting geometric shadows on busy streets below.
Traffic flows like rivers of metal and light,
while pedestrians weave through crosswalks with purpose.
Coffee shops exhale warmth and the aroma of fresh bread,
as commuters clutch their cups like talismans against the cold.
Street vendors call out in a symphony of languages,
their voices mixing with the distant hum of construction.
Pigeons dance between the feet of hurried workers,
finding crumbs of breakfast pastries on concrete sidewalks.
The city breathes in rhythm with a million heartbeats,
each person carrying dreams and deadlines in equal measure.
Skyscrapers reach toward clouds that drift like cotton,
while far below, subway trains rumble through tunnels.
This urban orchestra plays from dawn until dusk,
a endless song of ambition, struggle, and hope.
"""

splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.create_documents([long_text])
for chunk in chunks:
    print(chunk.page_content)
    print("-" * 30)
print("=" * 60)

model = init_chat_model(model="gpt-4.1-mini", model_provider="openai", temperature=0)

#Algoritimo de resumo com 'map_reduce'
#Cadeia de execução - Map: Resume cada bloco separadamente
template_map = ChatPromptTemplate.from_template("Write a concise summary of the following text:\n{context}")
chain_map = template_map | model | StrOutputParser()

prepare_map_inputs_runner = RunnableLambda(lambda documents: [ { "context": document.page_content } for document in documents ]) #Runner para converter o Document em uma lsita de entradas para 'chain_map'
chain_map_stage = prepare_map_inputs_runner | chain_map.map() #Cria chain onde cada item da lista retornada pelo 'prepare_map_inputs_runner' seja executado como entrada do 'chain_map'

#Cadeia de execução - Reduce: Combina os resumos em apenas um no final
template_reduce = ChatPromptTemplate.from_template("Combine the following summaries into a single concise summary:\n{context}")
chain_reduce = template_reduce | model | StrOutputParser()

#Cadeia de execução - Main: Pipeline principal que chama as outras
prepare_reduce_inputs_runner = RunnableLambda(lambda summaries: { "context": "\n".join(summaries) }) #Runner para converter a saida do 'chain_map_stage' para ser usado na 'chain_reduce'
chain_pipeline = chain_map_stage | prepare_reduce_inputs_runner | chain_reduce

result = chain_pipeline.invoke(chunks)
print(result)