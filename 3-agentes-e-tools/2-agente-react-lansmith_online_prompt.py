from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dotenv import load_dotenv
from langsmith import Client
import os

load_dotenv()
@tool("calculator", return_direct=True)
def calculator(expression: str) -> str:
    """Evaluate a simple mathematical expression and returns the result."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"
    return str(result)

@tool("web_search_mock")
def web_search_mock(query: str) -> str:
    """Simulates a web search."""
    data = {"Brasil": "Brasilia", "Argentina": "Buenos Aires", "Chile": "Santiago"}
    for country, capital in data.items():
        if country.lower() in query.lower():
            return f"The capital of {country} is {capital}."    
    return f"I do not know the capital"

llm = ChatOpenAI(model="gpt-5-mini", temperature=0,disable_streaming=True)
tools = [calculator, web_search_mock]
tool_descriptions = "\n".join(
    f"{tool.name}: {tool.description}" for tool in tools
)
tool_names = ", ".join(tool.name for tool in tools)

# Buscar o prompt do LangSmith Hub
# O Client() busca automaticamente LANGSMITH_API_KEY nas variáveis de ambiente
# 
# NOTA: Se receber erro 403, pode ser necessário:
# 1. Verificar se a Service Key é "organization-scoped" e adicionar o cabeçalho X-Tenant-Id:
#    client = Client(headers={"X-Tenant-Id": "seu_workspace_id"})
# 2. Verificar se o prompt "hwchase17/react" está público no LangSmith Hub
# 3. O prompt pode ter sido movido ou renomeado
api_key = os.getenv("LANGSMITH_API_KEY")
if api_key:
    key_type = 'Service Key' if api_key.startswith('lsv2_sk_') else 'Personal Token' if api_key.startswith('lsv2_pt_') else 'Desconhecido'
    print(f"✓ Chave carregada do .env: {api_key[:20]}... (tipo: {key_type})")
else:
    print("⚠ Aviso: LANGSMITH_API_KEY não encontrada no .env")

client = Client()  # Usa automaticamente LANGSMITH_API_KEY do ambiente

# Tentar buscar o prompt do LangSmith Hub
try:
    print("🔍 Tentando buscar prompt 'hwchase17/react' do LangSmith Hub...")
    prompt = client.pull_prompt("hwchase17/react")
    print("✓ Prompt carregado do LangSmith Hub com sucesso!")
except Exception as e:
    print(f"⚠ Não foi possível carregar o prompt do LangSmith Hub: {e}")
    print("📝 Usando prompt local como fallback...")
    
    # Fallback: usar o prompt ReAct local (mesmo formato do arquivo 1-agente-react-tools.py)
    prompt = f"""
Answer the following questions as best you can. You have access to the following tools:
Only information you get from these tools can be used to answer the questions.
If information is not found in the tools, you must respond with "I do not know".
{tool_descriptions}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Rules:
- If you choose an Action, do not include final answers in same step.
- After Action and Action Input, stop and wait for the observation.
- Never search the web directly, always use the web_search_mock tool.

Begin!
"""
    print("✓ Prompt local carregado")

agent = create_agent(llm, tools, system_prompt=prompt)

#result = agent.invoke({"messages": [("user", "Qual a capital do Brasil?")]})
#print(result["messages"][-1].content)

import json

# ... resto do código ...

#result = agent.invoke({"messages": [("user", "Qual a capital da Argentina?")]})
result = agent.invoke({"messages": [("user", "Qual a capital da africa?")]})
print(json.dumps(result, indent=2, default=str, ensure_ascii=False))