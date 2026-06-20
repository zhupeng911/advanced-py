from typing import TypedDict, NotRequired

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import END, START
from langgraph.graph import StateGraph


# 定义状态
class StoryState(TypedDict):
    character: NotRequired[str]  # 角色
    setting: NotRequired[str]  # 设置
    plot: NotRequired[str]  # 故事
    ending: NotRequired[str]  # 结局


# 定义节点
def create_character(state: StoryState):
    print("执行节点：create_character")
    mock_character = "一只会说话的猫"
    print(f"创建角色：{mock_character}")
    return {"character": mock_character}


def create_setting(state: StoryState):
    print("执行节点：create_setting")
    mock_setting = "一个充满魔法的森林"
    print(f"创建设置：{mock_setting}")
    return {"setting": mock_setting}


def create_plot(state: StoryState):
    print("执行节点：create_plot")
    character = state.get("character")
    setting = state.get("setting")
    mock_plot = f"{character}在{setting}发现了一个秘密"
    print(f"创建故事：{mock_plot}")
    return {"plot": mock_plot}


def create_ending(state: StoryState):
    print("执行节点：create_ending")
    plot = state.get("plot")
    mock_ending = f"当{plot}时，冒险故事结束了"
    print(f"创建结局：{mock_ending}")
    return {"ending": mock_ending}


# 构建图
def create_graph():
    builder = StateGraph(StoryState)
    builder.add_node("create_character", create_character)
    builder.add_node("create_setting", create_setting)
    builder.add_node("create_plot", create_plot)
    builder.add_node("create_ending", create_ending)
    builder.add_edge(START, "create_character")
    builder.add_edge("create_character", "create_setting")
    builder.add_edge("create_setting", "create_plot")
    builder.add_edge("create_plot", "create_ending")
    builder.add_edge("create_ending", END)
    return builder


if __name__ == "__main__":
    print("时间旅行")
    # 创建图
    graph = create_graph()
    app = graph.compile(checkpointer=InMemorySaver())

    # 第一次运行图
    print("第一个故事...")
    config_1 = {
        "configurable": {"thread_id": "story_1"}
    }
    result_1 = app.invoke({}, config_1)
    print(f"结果: {result_1}")

    # 查看第一个故事的历史状态
    stats_history_1 = list(app.get_state_history(config_1))
    print(f"历史状态: {stats_history_1}")

    # 第二次运行图：从中间状态继续
    print("第二个故事...")
    config_2 = app.update_state(
        stats_history_1[2].config,
        values={"character": "一只会飞的鸟"}
    )
    result_2 = app.invoke(None, config_2)
    print(f"结果: {result_2}")
