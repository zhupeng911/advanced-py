import operator
from typing import TypedDict, List, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 需求：add 列表追加
# 1. 定义State
class AddListState(TypedDict):
    data: Annotated[List[int], operator.add]  # 列表追加


# 2.定义节点Node
def node_1(state: AddListState) -> dict:
    return {"data": [1, 2]}


def node_2(state: AddListState) -> dict:
    return {"data": [3, 4]}


# 3.构建图Graph
graph = StateGraph(AddListState)
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
result = app.invoke({"data": [0]})
print(result)
