from typing import TypedDict, List

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 需求：如果未指定reducer函数，默认对该字段进行覆盖行为
# 1. 定义State
# 未指定合并策略reducer，默认覆盖
class DefaultReducerState(TypedDict):
    name: str
    hobby: List[str]


# 2.定义节点Node
def node_1(state: DefaultReducerState) -> dict:
    print(f'node_1: {state["name"]}')
    print(f'node_1: {state["hobby"]}')
    return {"name": "Alice", "hobby": ["篮球"]}


def node_2(state: DefaultReducerState) -> dict:
    print(f'node_2: {state["name"]}')
    print(f'node_2: {state["hobby"]}')
    return {"name": "Bob", "hobby": ["足球", "乒乓球"]}


# 3.构建图Graph
graph = StateGraph(DefaultReducerState)
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
result = app.invoke({"name": "张三", "hobby": ["nothing"]})
print(result)
