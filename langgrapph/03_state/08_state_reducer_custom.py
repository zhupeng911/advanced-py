from typing import TypedDict, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 需求 mul数值相乘
# 0. 自定义策略
def custom_strategy(current: int, update: int) -> int:
    """自定义策略： 处理乘法测略初始值为1"""
    if current == 0:
        return 1.0 * update
    return current * update


# 1. 定义State
class MultiplyIntState(TypedDict):
    data: Annotated[int, custom_strategy]


# 2.定义节点Node
def node_1(state: MultiplyIntState) -> dict:
    return {"data": 2}


def node_2(state: MultiplyIntState) -> dict:
    return {"data": 3}


# 4.构建图Graph
graph = StateGraph(MultiplyIntState)
# 4.1 添加节点
graph.add_node("node_1", node_1)
graph.add_node("node_2", node_2)
graph.add_edge(START, "node_1")
graph.add_edge("node_1", "node_2")
graph.add_edge("node_2", END)

# 5.编译
app = graph.compile()

# 6.运行
result = app.invoke({"data": 10})
print(result)
