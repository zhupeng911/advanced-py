import operator
from typing import TypedDict, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 需求 mul数值相乘
# 1. 定义State
# Annotated 是 Python 给类型注解开的"扩展槽"——类型系统看不见这些元数据，但你的框架（LangGraph、Pydantic、FastAPI…）能读到，并据此决定字段的校验、合并、解析等额外行为
class MultiplyIntState(TypedDict):
    data: Annotated[int, operator.mul]  # 新data = 旧data * 节点返回的data


# 2.定义节点Node
def node_1(state: MultiplyIntState) -> dict:
    print("node_1", state["data"])
    return {"data": 2}


def node_2(state: MultiplyIntState) -> dict:
    print("node_2", state["data"])
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
# 大坑：结果为0
# 原因：默认乘法的初始值为0，而0乘以任何数都等于0
# 解决方法：自定义策略，将初始值设为1
result = app.invoke({"data": 10})
print(result)  #
