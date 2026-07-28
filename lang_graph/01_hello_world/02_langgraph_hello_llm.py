from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.constants import START, END
from langgraph.graph import StateGraph, add_messages

from lang_graph.llm import init_llm


# 需求：接入LLM START -> 大模型节点 -> END


# 1. 定义State
class MyState(TypedDict):
    # 语法：Annotated[真实类型, 额外说明]
    # 功能：Annotated[list[BaseMessage], add_messages]：表示支持自动追加消息
    messages: Annotated[list[BaseMessage], add_messages]


# 2.定义节点Node1：支持大模型
def node_1(state: MyState):
    reply = init_llm().invoke(state["messages"])
    return {"messages": reply}  # 返回信息，自动添加到消息列表


# 3.构建图Graph
graph = StateGraph(MyState)
graph.add_node("node_1", node_1)
graph.add_edge(START, "node_1")
graph.add_edge("node_1", END)

# 4.编译
app = graph.compile()

# 5.运行
result = app.invoke({"messages": [HumanMessage(content="LangGraph简介")]})
print(result)
# result["messages"][-1]：取出状态中的 messages 字段的最后一条消息（即最新的一条，通常是 AI 的回复）
# .content： 取该消息对象的文本内容
print(f'result["messages"]: {result["messages"][-1].content}')
