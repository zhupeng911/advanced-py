import time

from langgraph.cache.memory import InMemoryCache
from langgraph.graph import StateGraph
from langgraph.types import CachePolicy
from typing_extensions import TypedDict


# 1.定义状态
class State(TypedDict):
    x: int
    result: int


# 2.定义节点
def node_1(state: State) -> dict[str, int]:
    time.sleep(3)
    return {"result": state["x"] * 2}


# 3.构建图
graph = StateGraph(State)
graph.add_node(node="node1", action=node_1, cache_policy=CachePolicy(ttl=8))
graph.set_entry_point("node1")
graph.set_finish_point("node1")

# 4.编译，指定内存缓存
app = graph.compile(cache=InMemoryCache())

# 5.第一次运行，无缓存：3s返回结果
print("第一次开始运行:无缓存")
result = app.invoke({"x": 2})
print(f'第一次运行结果: {result}')

# 6.第二次运行，有缓存： 0.1s返回结果
print("第二次开始运行:有缓存")
result = app.invoke({"x": 2})
print(f'第二次运行结果: {result}')

# 6.第三次运行，无缓存： 3s返回结果
print("第三次开始运行:无缓存")
result = app.invoke({"x": 3})
print(f'第三次运行结果: {result}')

# 7.第四次运行，等待缓存过期
time.sleep(5)
print("第四次开始运行:缓存过期")
result = app.invoke({"x": 2})
print(f'第四次运行结果: {result}')
