from langgraph.constants import END
from langgraph.constants import START
from langgraph.graph import StateGraph
from langgraph.types import RetryPolicy
from typing_extensions import TypedDict, Any


# 节点重试策略：默认重试策略、自定义重试策略、不可重试策略
# 1.定义状态类
class State(TypedDict):
    result: int


global_counter = 0  # 全局计数器：记录API重试次数


# 工具函数：生成图的编译
def build_retry_graph(node_name: str, node_func, retry_policy: RetryPolicy):
    graph = StateGraph(State)
    graph.add_node(node_name, node_func, retry_policy=retry_policy)
    graph.add_edge(START, node_name)
    graph.add_edge(node_name, END)
    return graph.compile()


# 2.定义节点：模拟不稳定的API调用
def unstable_api_call(state: State) -> dict[str, Any]:
    """模拟不稳定的API调用：前2次调用失败，第三次调用成功"""
    global global_counter
    global_counter += 1
    print(f'第 {global_counter} 次调用unstable_api_call')
    if global_counter < 3:
        raise Exception("模拟API调用失败")
    return {"result": f'API调用成功，经过了 {global_counter} 次尝试'}


# 3.定义节点：模拟抛出ValueError异常
def value_error_call(state: State) -> dict[str, int]:
    raise ValueError("模拟抛出ValueError异常")


# 测试1:默认重试策略
def test_default_retry_strategy():
    global global_counter
    print("1.默认重试策略：对除了特定异常的所有异常进行重试")
    print("不会重试的异常：ValueError、TypeError、ImportError")
    global_counter = 0
    app = build_retry_graph(
        node_name="unstable_api_call",
        node_func=unstable_api_call,
        retry_policy=RetryPolicy(max_attempts=5)
    )
    try:
        result = app.invoke({"result": ""})
        print(f'result: {result}')
    except Exception as e:
        print(e)


# 测试2:自定义重试策略（输出完全匹配异常）
# 自定义重试条件判断
def custom_retry_on(exception: Exception) -> bool:
    """自定义重试条件判断：只对包含【模拟API调用失败】的异常重试"""
    err_msg = str(exception)
    if "模拟API调用失败" in err_msg:
        return True
    return False

def test_custom_retry_strategy():
    global global_counter
    print("2.自定义重试策略：只对包含【模拟API调用失败】的异常进行重试")
    global_counter = 0
    app = build_retry_graph(
        node_name="unstable_api_call",
        node_func=unstable_api_call,
        retry_policy=RetryPolicy(max_attempts=5, retry_on=custom_retry_on)
    )
    try:
        result = app.invoke({"result": ""})
        print(f'result: {result}')
    except Exception as e:
        print(e)


# 测试3:不可重试策略
def test_no_retry_strategy():
    print("3.不可重试策略：对ValueError异常不进行重试")
    app = build_retry_graph(
        node_name="value_error_call",
        node_func=value_error_call,
        retry_policy=RetryPolicy(max_attempts=5)
    )
    try:
        result = app.invoke({"result": ""})
        print(f'result: {result}')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # test_default_retry_strategy()
    # test_custom_retry_strategy()
    test_no_retry_strategy()
