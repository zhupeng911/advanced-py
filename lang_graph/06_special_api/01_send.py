from typing import TypedDict, List, Annotated

from langgraph.constants import START
from langgraph.graph import StateGraph
from langgraph.types import Send


# LangGraph Map-Reduce 模式演示:
# 通过使用 Send 对象，LangGraph 提供了一种优雅的方式来实现这种动态图结构，
# 使得我们可以根据运行时状态来决定执行路径。
# 解释:
# (1)首先执行 generate_subjects主题列表:['猫’，‘狗’，‘程序员']
# (2)然后通过条件边函数 map_subjects_to_kokes为每个主题创建一个Send 对象
# (3)make_joke 节点被并行执行3次，每次处理一个主题
# (4)最终将所有生成的笑话合并到一个列表中
# 这种模式非常适合处理动态数量的任务

# 定义状态
class State(TypedDict):
    subjects: List[str]
    jokes: Annotated[List[str], lambda x, y: x + y]


# 定义节点1:生成需要的主题列表
def generate_subjects(state: State) -> dict:
    print(f"1.Generating subjects")
    subjects = ["猫", "狗", "程序员"]
    return {"subjects": subjects}


# 定义条件边函数：根据主题列表生成Send对象列表
def map_subjects_to_jokes(state: State) -> List[Send]:
    subjects = state.get("subjects", [])
    print(f"2.Mapping subjects to jokes: {subjects}")
    send_list = [Send("make_joke", {"subject": subject}) for subject in subjects]
    return send_list


# 定义Map节点2：为每个主题创建一个笑话
def make_joke(state: State) -> dict:
    subject = state.get("subject", "其他")  # map_subjects_to_jokes的Send 动态注入
    print(f"3.Making joke for {subject}")

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
