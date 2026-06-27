from typing import TypedDict

from langgraph.constants import END, START
from langgraph.graph import StateGraph


# 定义状态
class State(TypedDict):
    topic: str
    joke: str


# 定义节点
def refine_topic(state: State):
    return {"topic": state["topic"] + " and cats"}


def generate_joke(state: State):
    return {"joke": f'this is a joke about {state["topic"]}'}


if __name__ == "__main__":
    # 创建图
    graph = (
        StateGraph(State)
        .add_node("refine_topic", refine_topic)
        .add_node("generate_joke", generate_joke)
        .add_edge(START, "refine_topic")
        .add_edge("refine_topic", "generate_joke")
        .add_edge("generate_joke", END)
        .compile()
    )
    # 流式运行：updates
    for chunk in graph.stream({"topic": "dogs"}, stream_mode="updates"):
        print(chunk)
    print("--------------------------------")

    # 流式运行：values
    for chunk in graph.stream({"topic": "dogs"}, stream_mode="values"):
        print(chunk)
    print("--------------------------------")

    # 流式运行：debug
    for chunk in graph.stream({"topic": "dogs"}, stream_mode="debug"):
        print(chunk)
    print("--------------------------------")

    # 流式运行【混合】：updates + values
    for chunk in graph.stream({"topic": "dogs"}, stream_mode=["updates", "values"]):
        print(chunk)
    print("--------------------------------")
