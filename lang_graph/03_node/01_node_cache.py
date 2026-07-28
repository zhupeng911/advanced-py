import time

from langgraph.cache.memory import InMemoryCache
from langgraph.graph import StateGraph
from langgraph.types import CachePolicy
from typing_extensions import TypedDict


# 1.节点缓存策略：CachePolicy() 决定"查什么"和"存多久"，节点级（每个 node 可不同）
# 语法：graph.add_node(node="node1", action=node_1, cache_policy=CachePolicy(ttl=8))
# 案例：
# 1.1 CachePolicy()              — 默认，永不过期 + 默认 key 函数，输入相同就直接返回缓存，适合确定性节点（如文本格式化）
# 1.2 CachePolicy(ttl=30)        — TTL 过期，如你例子中 ttl=8，适合"结果会随时间变化"的节点（如 API 查询、数据库读取）
# 1.3 CachePolicy(key_func=custom_key)       — 自定义 key 函数，适合只关心输入中某些字段的场景，比如：
#     CachePolicy(key_func=lambda state: state["user_id"])  # 只按 user_id缓存，忽略其他字段
# 1.4 CachePolicy(ttl=60, key_func=custom_key) — TTL + 自定义 key 组合

# 2.图缓存策略：BaseCache() 决定"存哪里"，图级（整个 graph 共用一个）
# 语法：app = graph.compile(cache=InMemoryCache())
# 2.1 RedisCache()               — Redis 缓存，需要安装 redis 模块
# 2.2 InMemoryCache()            — 内存缓存，默认，无过期时间
# 2.3SqliteCache()              — SQLite 缓存，需要安装 sqlite3 模块


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

# 4.编译，配合内存缓存
app = graph.compile(cache=InMemoryCache())

# 5.第一次运行，无缓存：3s返回结果
print("第一次开始运行:无缓存")
result = app.invoke({"x": 2})
print(f'第一次运行结果: {result}')

# 6.第二次运行，有缓存： 0.1s返回结果
print("第二次开始运行:有缓存")
result = app.invoke({"x": 2})
print(f'第二次运行结果: {result}')

# 6.第三次运行，无x=3的缓存： 3s返回结果
print("第三次开始运行:无缓存")
result = app.invoke({"x": 3})
print(f'第三次运行结果: {result}')

# 7.第四次运行，等待缓存过期
time.sleep(5)
print("第四次开始运行:缓存过期")
result = app.invoke({"x": 2})
print(f'第四次运行结果: {result}')
