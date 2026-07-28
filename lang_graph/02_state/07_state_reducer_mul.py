import operator
from typing import TypedDict, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 需求 mul数值相乘
# 1. 定义State
class MultiplyIntState(TypedDict):
    data: Annotated[int, operator.mul]  # 新data = 旧data * 节点返回的data


# 2.定义节点Node
def node_1(state: MultiplyIntState) -> dict:
    print("node_1", state["data"])
    return {"data": 2}


def node_2(state: MultiplyIntState) -> dict:
    print("node_2", state["data"])
    return {"data": 3}


# 3.构建图Graph
graph = StateGraph(MultiplyIntState)
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
# 大坑：当初值为0时，结果为0
# 原因：默认乘法的初始值为0，而0乘以任何数都等于0
# 解决方法：自定义策略，将初始值设为1（见08_state_reducer_custom.py）
print(app.invoke({"data": 10}))  # {'data': 60}  10*2*3