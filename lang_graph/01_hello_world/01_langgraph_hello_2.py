from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 需求：在不接入LLM的情况下构建一个加减法图工作流
# 节点1: x+1
# 节点2: x-2


# 1. 定义State【非必须】

# 2.定义节点Node1
def addition(state):
    print(f'addition节点：{state}')
    return {"x": state["x"] + 1}


# 3.定义节点Node2
def subtraction(state):
    print(f'subtraction节点：{state}')
    return {"x": state["x"] - 2}


# 4.构建图Graph
graph = StateGraph(dict)
# 4.1 添加节点
graph.add_node("addition", addition)
graph.add_node("subtraction", subtraction)
# 4.1 添加边
graph.add_edge(START, "addition")
graph.add_edge("addition", "subtraction")
graph.add_edge("subtraction", END)

# 5.编译
app = graph.compile()

# 6.运行
result = app.invoke({"x": 20})
print(result)
print(f'result["x"]: {result["x"]}')
