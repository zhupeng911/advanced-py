from typing import TypedDict, List, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph, add_messages


# 需求：add_messages，即向state中添加消息(消息列表专用)
# 1. 定义State
class AddMessagesState(TypedDict):
    messages: Annotated[List, add_messages]


# 2.定义节点Node
def node_1(state: AddMessagesState) -> dict:
    print(f'node_1: {state["messages"]}')
    return {"messages": ["node_1"]}


def node_2(state: AddMessagesState) -> dict:
    print(f'node_2: {state["messages"]}')
    return {"messages": ["node_2"]}


# 4.构建图Graph
graph = StateGraph(AddMessagesState)
# 4.1 添加节点
graph.add_node("node_1", node_1)
graph.add_node("node_2", node_2)
graph.add_edge(START, "node_1") # 并行
graph.add_edge(START, "node_2") # 并行
graph.add_edge("node_1", END) # 并行
graph.add_edge("node_2", END)

# 5.编译
app = graph.compile()

# 6.运行
result = app.invoke({"messages": ["你是谁"]})
print(result)
