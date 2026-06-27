from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 条件入口点：根据输入内容决定从START节点去往下一个处理节点
# 1. 定义State
class MyState(TypedDict):
    user_input: str
    content: str
    node: str


# 2.定义路由函数-决定从START节点去哪
def route_input(state: MyState) -> str:
    """根据输入内容决定从START节点去往下一个处理节点"""
    text = state["user_input"].lower()
    if "hello" in text:
        return "hello_node"
    elif "bye" in text:
        return "bye_node"
    else:
        return "default_node"


# 3.1 定义hello_node节点
def hello_node(state: MyState) -> dict:
    return {"content": "Hello!你好", "node": "hello_node"}


# 3.2 定义bye_node节点
def bye_node(state: MyState) -> dict:
    return {"content": "Bye!再见", "node": "bye_node"}


# 3.3 定义default_node节点
def default_node(state: MyState) -> dict:
    return {"content": "默认响应。", "node": "default_node"}


# 4.构建图Graph
graph = StateGraph(MyState)
graph.add_node("hello_node", hello_node)
graph.add_node("bye_node", bye_node)
graph.add_node("default_node", default_node)
graph.add_conditional_edges(
    START, # 起始节点
    route_input, # 路由函数
    { # 节点映射
        "hello_node": "hello_node",
        "bye_node": "bye_node",
        "default_node": "default_node"
    })
graph.add_edge("hello_node", END)
graph.add_edge("bye_node", END)
graph.add_edge("default_node", END)

# 5.编译
app = graph.compile()

# 6.运行
result_1 = app.invoke({"user_input": "hello"})
print(f"Result 1: {result_1}")
result_2 = app.invoke({"user_input": "bye"})
print(f"Result 2: {result_2}")
result_3 = app.invoke({"user_input": "hi"})
print(f"Result 3: {result_3}")
