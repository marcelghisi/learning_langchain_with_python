from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.messages import trim_messages
from langchain_core.runnables import RunnableLambda

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that can answer short joke when possible."),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}"),
])

llm = ChatOpenAI(model="gpt-5-mini", temperature=0.9, disable_streaming=True)


def prepare_inputs(payload: dict) -> dict:
    raw_history = payload.get("raw_history", [])
    trimmed_history = trim_messages(
        raw_history, 
        max_tokens=2,
        token_counter=len, 
        strategy="last",
        start_on="human",
        include_system=True,
        allow_partial=False)
    
    return {
        "input": payload.get("input", ""),
        "history": trimmed_history,
    }

prepare_inputs_lambda = RunnableLambda(prepare_inputs)

chain = prepare_inputs_lambda | prompt | llm

session_store : dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]

conversation = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="raw_history",
)

config = {"configurable": {
    "session_id": "demo-session",}}

#Interactions
response1 = conversation.invoke({"input": "Olá, Meu nome é Marcel nao mencione meu nome?"}, config=config)
print(response1.content)
print("-"*30)

response2 = conversation.invoke({"input": "Me diga uma coisa engracada nao mencione meu nome"}, config=config)
print(response2.content)
print("-"*30)

response3 = conversation.invoke({"input": "Qual e o meu nome?"}, config=config)
print(response3.content)
print("-"*30)