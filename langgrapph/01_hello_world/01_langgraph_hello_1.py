from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 1. 定义State（可选，但推荐）
class HelloState(TypedDict):
    name: str
    greeting: str


# 2.定义节点Node1
# 节点就是函数，负责具体业务功能
def add_greeting(hello_state: HelloState) -> dict:
    name = hello_state["name"]
    return {"greeting": f"Hello, {name}!"}  # 因为返回的key和hello_state中的key相同，会更新hello_state中的greeting字段


# 3.定义节点Node2
def add_emoji(hello_state: HelloState) -> dict:
    greeting = hello_state["greeting"]
    return {"greeting": greeting + " 😊"}


# 4.构建图Graph
graph = StateGraph(HelloState)
# 4.1 添加节点
graph.add_node("add_greeting", add_greeting)
graph.add_node("add_emoji", add_emoji)
# 4.1 添加边
graph.add_edge(START, "add_greeting")
graph.add_edge("add_greeting", "add_emoji")
graph.add_edge("add_emoji", END)

# 5.编译
app = graph.compile()

# 6.运行
result = app.invoke({"name": "朱鹏"})
print(result)
print(f'result["name"]: {result["name"]}')
print(f'result["greeting"]: {result["greeting"]}')

# 7.打印
print(app.get_graph().print_ascii())
# print(app.get_graph().draw_mermaid())