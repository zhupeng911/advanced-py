from typing import TypedDict, Annotated, List

from langchain.chat_models import init_chat_model
from langgraph.constants import START, END
from langgraph.graph import StateGraph, add_messages

from lang_chain.config import OPENAI_API_KEY


# 需求：接入LLM START -> 大模型节点 -> END


# 1. 定义State
class MyState(TypedDict):
    # messages：消息列表
    # Annotated[List, add_messages]：表示支持自动追加消息
    messages: Annotated[List, add_messages]


# 2.定义节点Node1：支持大模型
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)


def node_1(my_state: MyState):
    reply = llm.invoke(my_state["messages"])
    return {"messages": reply}  # 返回信息，自动添加到消息列表


# 3.构建图Graph
graph = StateGraph(MyState)
# 4.1 添加节点
graph.add_node("node_1", node_1)
# 4.1 添加边
graph.add_edge(START, "node_1")
graph.add_edge("node_1", END)

# 5.编译
app = graph.compile()

# 6.运行
result = app.invoke({"messages": ["LangGraph简介"]})
print(result)
# result["messages"][-1]：取出状态中的 messages 字段的最后一条消息（即最新的一条，通常是 AI 的回复）
# .content： 取该消息对象的文本内容
print(f'result["messages"]: {result["messages"][-1].content}')
