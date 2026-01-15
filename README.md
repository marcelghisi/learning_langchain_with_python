# Curso LangChain - Aluno

Projeto de aprendizado sobre LangChain, incluindo fundamentos, chains, processamento e agentes com tools.

## Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

## Configuração do Ambiente

### 1. Criar o ambiente virtual (venv)

```bash
python3 -m venv venv
```

### 2. Ativar o ambiente virtual

**No macOS/Linux:**
```bash
source venv/bin/activate
```

**No Windows:**
```bash
venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install langchain-core langchain langchain-openai python-dotenv
```

Ou, se você tiver um arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com suas credenciais:

```env
OPENAI_API_KEY=sua_chave_api_aqui
```

## Estrutura do Projeto

```
curso-lang-chain-aluno/
├── 1-fundamentos/          # Conceitos básicos do LangChain
├── 2-chains-process/       # Chains e processamento
├── 3-agentes-e-tools/      # Agentes e ferramentas
├── venv/                   # Ambiente virtual (não versionado)
├── .env                    # Variáveis de ambiente (não versionado)
└── README.md              # Este arquivo
```

## Executando os Exemplos

### Exemplo: Agente ReAct com Tools

```bash
python3 3-agentes-e-tools/1-agente-react-tools.py
```

## Desativar o Ambiente Virtual

Quando terminar de trabalhar, você pode desativar o ambiente virtual:

```bash
deactivate
```

## Notas Importantes

- O diretório `venv/` está no `.gitignore` e não deve ser versionado
- O arquivo `.env` também está no `.gitignore` por segurança
- Sempre ative o ambiente virtual antes de executar os scripts

## Dependências Principais

- `langchain-core`: Core do LangChain
- `langchain`: Framework principal
- `langchain-openai`: Integração com OpenAI
- `python-dotenv`: Gerenciamento de variáveis de ambiente
