from langchain_core.runnables import RunnableLambda

def square(x: dict) -> dict:
    return {"x": x["x"], "x_squared": x["x"] * x["x"]}

runnable = RunnableLambda(square)

answer = runnable.invoke({"x": 5})

print(answer["x_squared"])