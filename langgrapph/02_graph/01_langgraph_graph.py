from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 1. 定义State（可选，但推荐）
class GraphState(TypedDict):
    process_data: dict


# 2.定义节点Node
def input_node(graph_state: GraphState) -> GraphState:
    print(f'input_node: {graph_state["process_data"]}')
    return {"process_data": {"input": "111"}}


def process_node(graph_state: GraphState) -> GraphState:
    print(f'process_node: {graph_state["process_data"]}')
    return {"process_data": {"input": "222"}}


def output_node(graph_state: GraphState) -> GraphState:
    print(f'output_node: {graph_state["process_data"]}')
    return {"process_data": {"output": "333"}}


# 4.构建图Graph
graph = StateGraph(GraphState)
# 4.1 添加节点
graph.add_node("input_node", input_node)
graph.add_node("process_node", process_node)
graph.add_node("output_node", output_node)
graph.add_edge(START, "input_node")
graph.add_edge("input_node", "process_node")
graph.add_edge("process_node", "output_node")
graph.add_edge("output_node", END)

# 5.编译
app = graph.compile()

# 6.运行
result = app.invoke({"process_data": {"input": "xxx"}})
print(result)
