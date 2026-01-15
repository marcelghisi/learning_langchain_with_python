from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5-nano", temperature=0.5)

result = llm.invoke("Hello, world!")

print(result)