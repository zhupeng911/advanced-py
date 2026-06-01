from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 1. 定义State（可选，但推荐）
# PS：MyState只是一个"形状说明书"，定义有哪些字段、是什么类型，它本身不存数据，真正的数据在运行时由 app.invoke({...}) 注入。
class MyState(TypedDict):
    name: str
    greeting: str


# 2.定义节点Node1：节点就是函数，负责具体业务功能
# 这个节点只返回了 greeting 字段，没有返回 name，但 name 不会丢失。因为 LangGraph 的默认行是：
# 返回字典里 有的 key → 用新值覆盖 State 中同名 key
# 返回字典里 没有的 key → State 中原值保留
def add_greeting(state: MyState) -> dict:
    name = state["name"]
    return {"greeting": f"Hello, {name}!"}


# 3.定义节点Node2
def add_emoji(state: MyState) -> dict:
    greeting = state["greeting"]
    return {"greeting": greeting + " 😊"}


# 4.构建图Graph
graph = StateGraph(MyState)
# 4.1 添加节点
graph.add_node("add_greeting", add_greeting)
graph.add_node("add_emoji", add_emoji)
# 4.2 添加边
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
