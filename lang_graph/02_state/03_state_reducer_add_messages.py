from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.constants import START, END
from langgraph.graph import StateGraph, add_messages


# 需求：add_messages，即向state中添加消息(消息列表专用)
# add_messages(LangGraph专用)
# 语法：messages: Annotated[list[BaseMessage],add_messages]
# - 专门为消息设计的Reducer
# - 新旧消息合并时，相同 ID 的消息会覆盖（用新消息替换旧消息），不同 ID 的则追加
# - 支持 LangGraph 的消息管理特性，如 MessageState、消息更新等

# 1. 定义State
class AddMessagesState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# 2.定义节点Node
def node_1(state: AddMessagesState) -> dict:
    print(f'node_1: {state["messages"]}')
    return {"messages": [AIMessage(content="我是AI助手")]}


def node_2(state: AddMessagesState) -> dict:
    print(f'node_2: {state["messages"]}')
    return {"messages": [HumanMessage(content="你好")]}


# 3.构建图Graph
graph = StateGraph(AddMessagesState)
# 3.1 添加节点
graph.add_node("node_1", node_1)
graph.add_node("node_2", node_2)
# 3.2 添加边
graph.add_edge(START, "node_1")
graph.add_edge("node_1", "node_2")
graph.add_edge("node_2", END)

# 4.编译
app = graph.compile()

# 5.运行
result = app.invoke({"messages": [HumanMessage(content="你是谁")]})
print(result)
