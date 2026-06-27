from operator import add
from typing import TypedDict, Annotated

from langgraph.constants import END, START
from langgraph.graph import StateGraph


# 定义状态
class State(TypedDict):
    messages: Annotated[list[str], add]


def sub_node(state: State):
    return {"messages": ["子图sub_node"]}


# 构建子图
sub_graph = StateGraph(State)
sub_graph.add_node("sub_node", sub_node)
sub_graph.add_edge(START, "sub_node")
sub_graph.add_edge("sub_node", END)
# 编译子图
sub_app = sub_graph.compile()

# 构建主图，添加子图(传入编译后的子图)
main_graph = StateGraph(State)
main_graph.add_node("sub_graph", sub_app)
main_graph.add_edge(START, "sub_graph")
main_graph.add_edge("sub_graph", END)
main_app = main_graph.compile()

# 运行
result = main_app.invoke({"messages": ["主图启动"]})
print(result)
# 问题 {'messages': ['主图启动', '主图启动', '子图sub_node']} 为什么结果会多出一个"主图启动"？
# 回答：因为子图的输入状态和输出状态都包含"messages"，所以子图的输出状态会覆盖主图的输入状态，导致结果多出一个"主图启动"。
