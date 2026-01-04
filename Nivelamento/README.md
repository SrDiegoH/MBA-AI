# Introdução ao LangChain

O MBA tem um mini curso para Nivelamento da turma para ter o primeiro contato com o LangChain

---

## Configuração do ambiente

1. **Criar um ambiente virtual (`venv`):** 

   ```bash
   python -m venv "$env:USERPROFILE\Workspace\MBA-IA\Nivelamento\venv"
   ```

2. **Ativar o ambiente virtual (`venv`):** 

   ```bash
   cd "$env:USERPROFILE\Workspace\MBA-IA\Nivelamento\venv\Scripts"; .\Activate.ps1 ; cd "..\..\code"
   ```
**Obs: Docs sobre python venv [aqui](https://docs.python.org/pt-br/3/library/venv.html)**

3. **Instalar as dependências a partir do `requirements.txt`:**

   ```bash
   pip install -r "$env:USERPROFILE\Workspace\MBA-IA\Nivelamento\code\requirements.txt"
   ```

**Obs: Caso seja isntalada uma nova lib, gerar um novo `requirements.txt` com o comando:**

   ```bash
   pip freeze > "$env:USERPROFILE\Workspace\MBA-IA\Nivelamento\code\requirements.txt"
   ```

4. **Configurar as variáveis de ambiente:**

   - Duplique o arquivo `.env.example` e renomeie para `.env`
   - Abra o arquivo `.env` e substitua os valores pelas suas chaves de API reais obtidas conforme instruções abaixo na sessão **Criando uma API Key na OpenAI**

## Principais tópicos abordados no curso 

### Fundamentos básicos
- **Introdução ao LangChain:** Conceitos básicos e primeira integração com modelos de linguagem
- **Integração com OpenAI:** Como usar o ChatOpenAI para interações básicas
- **Integração com Google Gemini:** Configuração e uso do modelo Gemini via Google GenAI
- **Templates de Prompt:** Criação de templates simples e avançados para prompts
- **Chat Prompts:** Implementação de sistemas de conversação com templates estruturados

### Chains e Processamento avançado
- **LCEL (LangChain Expression Language):** Sintaxe de pipe (|) para conectar componentes
- **Chains Básicas:** Criação de pipelines simples de pergunta e resposta
- **Chains Complexas:** Pipelines multi-etapas com tradução e sumarização
- **Runnables Customizados:** Decorador @chain e RunnableLambda para funções personalizadas
- **Text Splitters:** Divisão de textos longos em chunks para processamento
- **Summarization Chains:** Técnicas "stuff" e "map_reduce" para sumarização de documentos
- **Structured Output:** Extração de dados estruturados usando Pydantic models

### Agentes e Tools
- **Custom Tools:** Criação de ferramentas personalizadas com decorador @tool
- **ReAct Agents:** Implementação de agentes que raciocinam e agem
- **Agent Executors:** Orquestração de agentes com múltiplas ferramentas
- **Prompt Hub:** Uso de prompts pré-definidos da comunidade LangChain

### Gerenciamento de memória
- **Chat History:** Implementação de histórico de conversação persistente
- **Message Memory:** Armazenamento e recuperação de mensagens em sessões
- **Memory Trimming:** Técnicas de janela deslizante para gerenciar contexto limitado
- **Session Management:** Gerenciamento de múltiplas sessões de conversa

### Document Loaders e RAG
- **Web Loaders:** Carregamento de conteúdo de páginas web
- **PDF Loaders:** Processamento e extração de texto de documentos PDF
- **Document Chunking:** Estratégias de divisão de documentos para processamento eficiente
- **RAG Foundations:** Conceitos básicos para Retrieval-Augmented Generation

## Requisitos para Execução dos Códigos

Para executar os códigos fornecidos no curso, é necessário:

1. Ter instalado:
- Python
- Docker e Docker compose

2. Criar chaves de API (API Keys) para os serviços da OpenAI e do Google Gemini. Abaixo tem as instruções de como obtê-las.

### Criando uma API Key na OpenAI

1. **Acesse o site da OpenAI:**

   [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

2. **Faça login ou crie uma conta:**

   - Se já possuir uma conta, clique em "Log in" e insira suas credenciais.
   - Caso contrário, clique em "Sign up" para criar uma nova conta.

3. **Navegue até a seção de API Keys:**

   - Após o login, clique em "API Keys" no menu lateral esquerdo.

4. **Crie uma nova API Key:**

   - Clique no botão "Create new secret key".
   - Dê um nome para a chave que a identifique facilmente.
   - Clique em "Create secret key".

5. **Copie e armazene sua API Key:**

   - A chave será exibida uma única vez. Copie-a e cole no arquivo `.env` na variável `OPENAI_API_KEY`.

Para mais detalhes, consulte o tutorial completo: [Como Gerar uma API Key na OpenAI?](https://hub.asimov.academy/tutorial/como-gerar-uma-api-key-na-openai/)

### Criando uma API Key no Google Gemini

1. **Acesse o Google AI Studio:**

   [https://aistudio.google.com/api-keys](https://aistudio.google.com/api-keys)

2. **Faça login com sua conta Google:**

   - Utilize sua conta Google para acessar o AI Studio.

3. **Navegue até a seção de chaves de API:**

   - No painel de controle, clique em "API Keys" ou "Chaves de API".

4. **Crie uma nova API Key:**

   - Clique em "Create API Key" ou "Criar chave de API".
   - Dê um nome para a chave que a identifique facilmente.
   - A chave será gerada e exibida na tela.

5. **Copie e armazene sua API Key:**

   - Copie a chave gerada e cole no arquivo `.env` na variável `GOOGLE_API_KEY`.

Para mais informações, consulte a documentação oficial: [Como usar chaves da API Gemini](https://ai.google.dev/gemini-api/docs/api-key?hl=pt-BR)

**Nota:** Certifique-se de não compartilhar suas chaves de API publicamente e de armazená-las em locais seguros, pois elas concedem acesso aos serviços correspondentes.
