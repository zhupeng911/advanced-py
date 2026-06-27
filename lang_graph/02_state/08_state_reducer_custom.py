from typing import TypedDict, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 需求 mul数值相乘
# 0. 自定义策略
# LangGraph 框架的硬约定：reducer 函数签名固定为 (current_value, new_update) -> merged_value。
# current： State 中 data 的当前值，LangGraph 从内部 state 读取
# update： 节点 return 的新值，LangGraph 从节点返回值取
def custom_strategy(current: int, update: int) -> int:
    """自定义策略：处理乘法策略初始值为0的问题"""
    if current == 0:
        return update  # 初值为0时，直接使用update作为起点
    return current * update


# 1. 定义State
class MultiplyIntState(TypedDict):
    data: Annotated[int, custom_strategy]


# 2.定义节点Node
def node_1(state: MultiplyIntState) -> dict:
    return {"data": 2}


def node_2(state: MultiplyIntState) -> dict:
    return {"data": 3}


# 3.构建图Graph
graph = StateGraph(MultiplyIntState)
# 3.1 添加节点
graph.add_node("node_1", node_1)
graph.add_node("node_2", node_2)
graph.add_edge(START, "node_1")
graph.add_edge("node_1", "node_2")
graph.add_edge("node_2", END)

# 4.编译
app = graph.compile()

# 5.运行
result = app.invoke({"data": 10})
print(result)
