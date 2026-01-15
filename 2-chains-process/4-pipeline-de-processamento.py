from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()

llm = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai", temperature=0.5)

template = PromptTemplate.from_template(
    input_variables=["initial_value"],
    template="Sumarise following text: {initial_value}"
)

template_translate = PromptTemplate.from_template(
    input_variables=["initial_value"],
    template="Translate following text to English: {initial_value}"
)

chain = template | llm | template_translate | llm | StrOutputParser()
runnable = RunnableLambda(square)