from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template("Olá, {name}! Como você está?")

prompt = template.invoke({"name": "João"})

print(prompt.to_string())