from dataclasses import dataclass
from typing import TypedDict, Annotated

from langchain_core.messages import AIMessage
from langgraph.constants import END, START
from langgraph.graph import StateGraph, add_messages
from langgraph.runtime import Runtime


# 定义状态
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    response: str


# 1.定义上下文结构，类似于yml文件
@dataclass
class ContextSchema:
    model_name: str
    db_conn: str
    api_key: str


# 2.定义节点函数：处理用户信息
def process_message(state: AgentState, runtime: Runtime[ContextSchema]) -> dict:
    print("1.Processing message...")
    # 获取用户最新的信息
    last_message = state["messages"][-1].content if state["messages"] else ("")
    print(f"2.Latest message: {last_message}")
    # 获取RuntimeContex信息
    model_name = runtime.context.model_name
    db_conn = runtime.context.db_conn
    api_key = runtime.context.api_key
    print(f"Model name: {model_name}, DB connection: {db_conn}, API key: {api_key}")
    return {
        "messages": [AIMessage(content="Processed message.")],
        "response": "Processed message."
    }


# 3.定义节点函数：生成最终响应
def generate_response(state: AgentState, runtime: Runtime[ContextSchema]) -> dict:
    print("Generating response...")

    pre_response = state["response"]
    final_response = "最终结果" + pre_response + runtime.context.model_name

    return {
        "messages": [AIMessage(content=final_response)],
        "response": final_response
    }


if __name__ == "__main__":
    # 创建图
    graph = StateGraph(AgentState, context_schema=ContextSchema)
    graph.add_node("process_message", process_message)
    graph.add_node("generate_response", generate_response)

    graph.add_edge(START, "process_message")
    graph.add_edge("process_message", "generate_response")
    graph.add_edge("generate_response", END)

    app = graph.compile()

    # 运行
    # 定义上下文
    context = ContextSchema(
        model_name="gpt-3.5-turbo",
        db_conn="localhost:5432",
        api_key="123456"
    )
    result = app.invoke({"messages": [], "response": ""}, context=context)
    print("result:", result)
