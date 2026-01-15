from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dotenv import load_dotenv
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

agent = create_agent(llm, tools, system_prompt=prompt)

#result = agent.invoke({"messages": [("user", "Qual a capital do Brasil?")]})
#print(result["messages"][-1].content)

import json

# ... resto do código ...

#result = agent.invoke({"messages": [("user", "Qual a capital da Argentina?")]})
result = agent.invoke({"messages": [("user", "Quanto e 10 mais 10?")]})
print(json.dumps(result, indent=2, default=str, ensure_ascii=False))