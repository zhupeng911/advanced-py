from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 1. 定义State（可选，但推荐）
# MyState 不是类实例，是"字段说明书"。它告诉 LangGraph：
# - State 里有哪些 key
# - 每个 key 是什么类
# - app.invoke({...}) 传入的 dict 需要符合这个形状
class MyState(TypedDict):
    name: str
    greeting: str


# 2.定义节点Node1：节点就是函数或Runnable对象，负责具体业务功能
# 功能说明：
# 这个节点只返回了 greeting 字段，没有返回 name，但 name 不会丢失。因为 LangGraph 的默认是：
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

# 6.运行：invoke 时自动关联 MyState
# 6.1.LangGraph 内部做了这件事：用 MyState 的字段定义来构造完整 state
# state = {
#   "name": input_dict["name"],      # "朱鹏" — 你传入的
#   "greeting": input_dict.get("greeting", ...)  # 你没传，给默认值留空
#   }
# 6.2.result 就是一个普通的 dict，符合 MyState 的形状
result = app.invoke({"name": "朱鹏"})
print(result)
print(f'result["name"]: {result["name"]}')
print(f'result["greeting"]: {result["greeting"]}')

# 7.打印
print(app.get_graph().print_ascii())
# print(app.get_graph().draw_mermaid())
