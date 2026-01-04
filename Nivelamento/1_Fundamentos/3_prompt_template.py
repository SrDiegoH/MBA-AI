from langchain_core.prompts import PromptTemplate

template = PromptTemplate( #Cria um template de mensagens a serem passadas na iteração
    input_variables=["name"],
    template="Hi, I'm {name}! Tell me a joke with my name!"
)

message = template.format(name="Diego") #Insere as variáveis na mensagem do template
print(message) #Mostra no terminal a mensagem do template formatada com as variáveis