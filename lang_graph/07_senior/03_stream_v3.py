from typing import TypedDict

from langgraph.config import get_stream_writer
from langgraph.constants import END, START
from langgraph.graph import StateGraph


# 定义状态
class State(TypedDict):
    query: str
    answer: str


# 定义节点
def node(state: State):
    print('node开始...')
    writer = get_stream_writer()
    writer({"custom_key": "朱鹏"})
    return {"answer": "最终结果"}


if __name__ == "__main__":
    # 创建图
    graph = (
        StateGraph(State)
        .add_node("node", node)
        .add_edge(START, "node")
        .add_edge("node", END)
        .compile()
    )
    inputs = {"query": "写100字介绍LangChain"}

    # 流式运行：自定义custom，会忽略其他模式，一般与其他模式混合使用
    # for chunk in graph.stream(inputs, stream_mode=["custom"]):
    #     print(chunk, end="")

    for chunk in graph.stream(inputs, stream_mode=["custom", "values"]):
        print(chunk, end="")
