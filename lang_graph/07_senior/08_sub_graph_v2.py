from typing import TypedDict

from langgraph.constants import END, START
from langgraph.graph import StateGraph


# 将子图作为节点添加到父图

# 定义父图状态
class ParentState(TypedDict):
    parent_messages: list  # 与子图共享数据


# 定义子图状态
class SubState(TypedDict):
    parent_messages: list  # 与父图共享数据
    sub_message: str  # 子图私有数据


# 定义子图节点
def sub_node(state: SubState) -> SubState:
    state["parent_messages"].append("子图共享数据")
    state["sub_message"] = "子图私有数据"
    return state


# 定义父图节点
def parent_node(state: ParentState) -> ParentState:
    if not state.get("parent_messages"):
        state["parent_messages"] = []
    state["parent_messages"].append("父图共享数据")
    return state


# 构建子图
def build_sub_graph() -> StateGraph:
    sub_graph = StateGraph(SubState)
    sub_graph.add_node("sub_node", sub_node)
    sub_graph.add_edge(START, "sub_node")
    sub_graph.add_edge("sub_node", END)
    return sub_graph.compile()

# 构建父图
def build_parent_graph(compiled_sub_graph) -> StateGraph:
    parent_graph = StateGraph(ParentState)
    parent_graph.add_node("parent_node", parent_node)
    parent_graph.add_node("sub_graph", compiled_sub_graph)

    parent_graph.add_edge(START, "parent_node")
    parent_graph.add_edge("parent_node", "sub_graph")
    parent_graph.add_edge("sub_graph", END)
    return parent_graph.compile()


if __name__ == "__main__":
    # 构建子图
    compiled_sub_graph = build_sub_graph()
    # 构建父图
    parent_graph = build_parent_graph(compiled_sub_graph)
    # 运行父图
    result = parent_graph.invoke({"parent_messages": ["父图启动"]})
    print(result)

