from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 需求：定义图的输入、输出模式

# 1. 定义状态
# 1.1 定义输入状态模式
class InputState(TypedDict):
    question: str


# 1.2 定义输出状态模式
class OutputState(TypedDict):
    answer: str


# 1.3 定义图的整体输入、输出状态模式
class OverallState(InputState, OutputState):
    pass


# 2.定义处理节点Node
def node_1(input_state: InputState):
    print(f'node_1节点，输入：{input_state}')
    answer = "再见" if "bye" in input_state["question"] else "你好"
    # 定义输出结果
    result = {"answer": answer, "question": input_state["question"]}
    return result


# 3.构建图Graph
graph = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)

# 3.1 添加节点
graph.add_node("node_1", node_1)
# 3.2 添加边
graph.add_edge(START, "node_1")
graph.add_edge("node_1", END)

# 4.编译
app = graph.compile()

# 5.运行
result = app.invoke({"question": "bye"})
print(result)
