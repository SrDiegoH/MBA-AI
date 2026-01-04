from langchain_core.runnables import RunnableLambda

def parse_number(text): #Função para fins didáticos, neste caso recebe como entrada um text
    return int(text.strip())

runnable = RunnableLambda(parse_number) #Outra forma de fazer a função ser usada em uma chain usando 'RunnableLambda' passando como paâametro a função desejada

result = runnable.invoke("10") #Inicia o processamento do runnable. Neste caso não foi usado em uma chain, mas pode ser
print(result) #Mostra no terminal o resultado do processo