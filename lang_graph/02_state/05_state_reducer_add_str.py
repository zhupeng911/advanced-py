import operator
from typing import TypedDict, List, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 需求：add 字符串连接
# 1. 定义State
class AddStrState(TypedDict):
    data: Annotated[str, operator.add]  # 字符串连接


# 2.定义节点Node
def node_1(state: AddStrState) -> dict:
    print(f'node_1: {state["data"]}')
    return {"data": "node_1"}


def node_2(state: AddStrState) -> dict:
    print(f'node_2: {state["data"]}')
    return {"data": " node_2"}


# 3.构建图Graph
graph = StateGraph(AddStrState)
# 3.1 添加节点
graph.add_node("node_1", node_1)
graph.add_node("node_2", node_2)
# 3.2 添加边
graph.add_edge(START, "node_1")
graph.add_edge("node_1", "node_2")
graph.add_edge("node_2", END)

# 4.编译
app = graph.compile()

# 5.运行
result = app.invoke({"data": "node_0 "})
print(result)
