from typing import TypedDict, List, Annotated

from langgraph.constants import START
from langgraph.graph import StateGraph
from langgraph.types import Send


# LangGraph Map-Reduce 模式演示:
# 定义：通过使用 Send 对象，使得我们可以根据运行时状态来决定执行路径，这种模式非常适合处理动态数量的任务
#
# 架构：
#                ┌─ Send("make_joke", {"subject": "猫"}) ─→ make_joke ─┐
#                │                                                       │
#   generate ──→├─ Send("make_joke", {"subject": "狗"}) ─→ make_joke ──┼──→ jokes 自动合并
#                │                                                       │
#                └─ Send("make_joke", {"subject": "程序员"}) → make_joke ┘
#                     ↑ Map 阶段（fan-out）                  ↑ Reduce 阶段（自动归并）
# 步骤：
#   1. Map — 条件边函数返回 List[Send]
#   2. 并行执行 — 同一个节点被多次调用
#   3. Reduce — 自动合并结果

# 1.定义状态
class State(TypedDict):
    subjects: List[str]
    jokes: Annotated[List[str], lambda x, y: x + y]  # 等价于 jokes: Annotated[List[str], add_messages]


# 2.定义节点1:生成需要的主题列表
def generate_subjects(state: State) -> dict:
    print(f"1.生成需要的主题列表")
    return {"subjects": ["猫", "狗", "程序员"]}


# 3.定义条件边函数：根据主题列表生成Send对象列表
# 当 subjects = ["猫", "狗", "程序员"] 时，这行代码生成
# [
#   Send("make_joke", {"subject": "猫"}),
#   Send("make_joke", {"subject": "狗"}),
#   Send("make_joke", {"subject": "程序员"})
# ]
def map_subjects_to_jokes(state: State) -> List[Send]:
    subjects = state.get("subjects", [])
    print(f"2.将主题映射到笑话: {subjects}")
    return [
        Send(
            "make_joke",  # 目标节点
            {"subject": subject}  # 传递参数
        )
        for subject in subjects
    ]


# 4.定义Map节点2：为每个主题创建一个笑话
def make_joke(state: State) -> dict:
    subject = state.get("subject", "其他")  # map_subjects_to_jokes的Send 动态注入
    print(f"3.为{subject}创建一个笑话")

    # 根据主题生成笑话
    jokes_map = {
        "猫": "为什么猫不喜欢在图书馆里借书？因为那里有很多猫书。",
        "狗": "为什么狗不喜欢在图书馆里借书？因为那里有很多狗书。",
        "程序员": "为什么程序员不喜欢在图书馆里借书？因为那里有很多代码书。",
        "其他": "为什么其他不喜欢在图书馆里借书？因为那里有很多其他书。"
    }
    joke = jokes_map.get(subject, f'这是一个关于{subject}的笑话')
    return {"jokes": [joke]}


def main():
    # 创建图
    graph = StateGraph(State)
    # 添加节点
    graph.add_node("generate_subjects", generate_subjects)
    graph.add_node("make_joke", make_joke)
    # 添加边
    graph.add_edge(START, "generate_subjects")
    graph.add_conditional_edges("generate_subjects", map_subjects_to_jokes)
    # 运行图
    app = graph.compile()
    result = app.invoke({"subjects": [], "jokes": []})
    print(result)


if __name__ == "__main__":
    main()
