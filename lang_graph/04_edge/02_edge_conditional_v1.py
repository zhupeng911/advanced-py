from typing import TypedDict, Optional

from langgraph.constants import START
from langgraph.graph import StateGraph


# 条件边：add_conditional_edges 2个分支

# 1. 定义State
class MyState(TypedDict):
    x: int
    result: Optional[str]


# 2.定义节点：检查输入状态的节点函数
def check_x(state: MyState) -> dict:
    print(f'Checking x: {state["x"]}')
    return {}


# 2.定义偶数节点
def handle_even(state: MyState) -> dict:
    print(f'Handling even x: {state["x"]}')
    return {"result": "Even"}


# 3.定义奇数节点
def handle_odd(state: MyState) -> dict:
    print(f'Handling odd x: {state["x"]}')
    return {"result": "Odd"}


# 条件边的路由函数：判断 x 是否为偶数的条件函数
def is_even_route(state: MyState) -> bool:
    return state["x"] % 2 == 0


# 4.构建图Graph
graph = StateGraph(MyState)
graph.add_node("check_x", check_x)
graph.add_node("handle_even", handle_even)
graph.add_node("handle_odd", handle_odd)
# 4.1 添加普通边
graph.add_edge(START, "check_x")
# 4.2 添加条件边
graph.add_conditional_edges("check_x", is_even_route, {
    True: "handle_even",
    False: "handle_odd"
})

# 5.编译
app = graph.compile()

# 6.运行
# result = app.invoke({"x": 3})
result = app.invoke({"x": 4})
print(result)
print(app.get_graph().print_ascii())
