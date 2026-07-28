from typing import TypedDict, Optional

from langgraph.constants import START
from langgraph.graph import StateGraph


# 条件边：add_conditional_edges 2个分支
# 语法：add_conditional_edges(source, path, path_map=None)
# source:    起始节点
# path:      路由函数，接收 state，返回下一节点名（或节点名列表
# path_map:  路由映射表，{返回值: 节点名}；省略时 path 直接返回节点名

# 1. 定义State
class MyState(TypedDict):
    x: int
    result: Optional[str]


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
graph.add_node("handle_even", handle_even)
graph.add_node("handle_odd", handle_odd)
# 添加条件边
graph.add_conditional_edges(START, is_even_route, {
    True: "handle_even",
    False: "handle_odd"
})

# 5.编译
app = graph.compile()

# 6.运行
result = app.invoke({"x": 3})
# result = app.invoke({"x": 4})
print(result)
print(app.get_graph().print_ascii())
