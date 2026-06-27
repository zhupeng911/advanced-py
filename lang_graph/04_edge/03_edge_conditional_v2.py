from typing import TypedDict, Optional

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 条件边：add_conditional_edges 3个分支
# 条件入口点：根据输入内容决定从START节点去往下一个处理节点

# 1. 定义State
class MyState(TypedDict):
    x: int
    result: Optional[str]


# 2.1定义节点1
def add_1(state: MyState) -> MyState:
    print(f'Adding 1: {state["x"]}')
    return MyState(x=state["x"] + 1)


# 2.2定义节点2
def add_2(state: MyState) -> MyState:
    print(f'Adding 2: {state["x"]}')
    return MyState(x=state["x"] + 2)


# 2.3定义节点3
def add_3(state: MyState) -> MyState:
    print(f'Adding 3: {state["x"]}')
    return MyState(x=state["x"] + 3)


# 3.定义路由函数
def route_by_sentiment(state: MyState) -> str:
    flag = state["x"]
    if flag == 1:
        return "add_1"
    elif flag == 2:
        return "add_2"
    else:
        return "add_3"


# 4.构建图Graph
graph = StateGraph(MyState)
graph.add_node("add_1", add_1)
graph.add_node("add_2", add_2)
graph.add_node("add_3", add_3)
# 4.1 添加条件边
graph.add_conditional_edges(
    START,  # 起始节点
    route_by_sentiment,  # 路由函数
    {  # 路由表
        "add_1": "add_1",
        "add_2": "add_2",
        "add_3": "add_3"
    })
graph.add_edge("add_1", END)
graph.add_edge("add_2", END)
graph.add_edge("add_3", END)

# 5.编译
app = graph.compile()

# 6.运行
result_1 = app.invoke({"x": 1})
print(f"Result 1: {result_1}")
result_2 = app.invoke({"x": 2})
print(f"Result 2: {result_2}")
result_3 = app.invoke({"x": 3})
print(f"Result 3: {result_3}")
