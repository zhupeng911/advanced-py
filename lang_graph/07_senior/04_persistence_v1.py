import operator
from typing import TypedDict, Annotated

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import END, START
from langgraph.graph import StateGraph


# LangGraph持久化-内存

# 定义状态
class PersistenceState(TypedDict):
    messages: Annotated[list, operator.add]
    step_count: Annotated[int, operator.add]


# 定义节点
def step_one(state: PersistenceState) -> dict:
    print("Step one")
    return {
        "messages": ["执行了step one"],
        "step_count": 1
    }


def step_two(state: PersistenceState) -> dict:
    print("Step two")
    return {
        "messages": ["执行了step two"],
        "step_count": 1
    }


def step_three(state: PersistenceState) -> dict:
    print("Step three")
    return {
        "messages": ["执行了step three"],
        "step_count": 1
    }


# 构建图
def create_graph():
    builder = StateGraph(PersistenceState)
    builder.add_node("step_one", step_one)
    builder.add_node("step_two", step_two)
    builder.add_node("step_three", step_three)
    builder.add_edge(START, "step_one")
    builder.add_edge("step_one", "step_two")
    builder.add_edge("step_two", "step_three")
    builder.add_edge("step_three", END)
    return builder


if __name__ == "__main__":
    print("内存持久化...")
    # 编译图:使用内存存储
    graph = create_graph()
    app = graph.compile(checkpointer=InMemorySaver())

    # 运行图：配置线程id
    config = {"configurable": {"thread_id": "zhupeng"}}
    result = app.invoke({"messages": ["开始执行"], "step_count": 0}, config)
    print(f'结果: {result}')

    # 检查结果状态
    saved_state = app.get_state(config)
    print(f'保存的状态: {saved_state.values}')
    print(f'下一个节点: {saved_state.next}')

    # 历史过程快照
    history = app.get_state_history(config)
    for state in history:
        print(f'状态: {state.values}')

    # 重点：恢复，直接就是第三步，因为保存了状态
    result_2 = app.invoke(None, config)
    print(f'结果: {result_2}')
