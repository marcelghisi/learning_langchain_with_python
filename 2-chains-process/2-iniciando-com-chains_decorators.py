from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import chain
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()

@chain
def square(x: dict) -> dict:
    return {"x": x["x"], "x_squared": x["x"] * x["x"]}

template = PromptTemplate.from_template("Qual é a capital do {country}?")

template_square = PromptTemplate.from_template("O quadrado de {x} é {x_squared}")

llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai", temperature=0.5)

chain = template | llm
chain2 = square | template_square | llm

answer = chain.invoke({"country": "Brasil"})

answer2 = chain2.invoke({"x": 5})

print(answer2.content)