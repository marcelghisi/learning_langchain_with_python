from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()

system = ("system", "Você é um assistente de IA que responde perguntas sobre o Brasil.")
human = ("human", "{question}")

chat_prompt = ChatPromptTemplate.from_messages([system, human])

llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai", temperature=0.5)

chain = chat_prompt | llm

answer = chain.invoke({"question": "Qual é a capital do Brasil?"})

print(answer.content)

#template = ChatPromptTemplate.from_messages([
#    ("system", "Você é um assistente de IA que responde perguntas sobre o Brasil."),#
#    ("human", "{question}")
#])

#prompt = template.invoke({"question": "Qual é a capital do Brasil?"})

#print(prompt.to_string())