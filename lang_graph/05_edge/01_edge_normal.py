from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 1. 定义State
class MyState(TypedDict):
    name: str


# 2.定义节点Node1
def add_greeting(state: MyState) -> dict:
    return {"name": f"Hello, {state['name']}!"}


# 3.定义节点Node2
def add_emoji(state: MyState) -> dict:
    return {"name": state["name"] + " 😊"}


# 4.构建图Graph
graph = StateGraph(MyState)
# 4.1 添加节点
graph.add_node("add_greeting", add_greeting)
graph.add_node("add_emoji", add_emoji)
# 4.2 添加普通边
graph.add_edge(START, "add_greeting")
graph.add_edge("add_greeting", "add_emoji")
graph.add_edge("add_emoji", END)

# 5.编译
app = graph.compile()

# 6.运行
result = app.invoke({"name": "朱鹏"})
print(result)
