from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()

template = PromptTemplate.from_template("Qual é a capital do {country}?")

llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai", temperature=0.5)

chain = template | llm

answer = chain.invoke({"country": "Brasil"})

print(answer.content)