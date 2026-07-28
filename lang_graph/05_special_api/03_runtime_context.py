from dataclasses import dataclass
from typing import TypedDict, Annotated

from langchain_core.messages import AIMessage
from langgraph.constants import END, START
from langgraph.graph import StateGraph, add_messages
from langgraph.runtime import Runtime


# Context
# 定义： Context是只读运行时配置机制，用于向所有节点注入不可变的共享配置（模型名、数据库连接、API Key等），与可变的 State 分离。
# 使用场景：模型名、数据库连接、API Key等
# 步骤：
# 1.定义 Context 结构，类似于yml文件
# 2.注册到图 + 节点声明
#   图层面注册   graph = StateGraph(AgentState, context_schema=ContextSchema)
#   节点声明     def process_message(state: AgentState, runtime: Runtime[ContextSchema]) -> dict:
# 3.调用时注入
#  ctx = ContextSchema(model_name="gpt-4", db_conn="localhost", api_key="sk-xxx")
#  app.invoke({"messages": []}, context=ctx)

# Context vs State
#
#   ┌──────────┬───────────────────────┬────────────────────────┐
#   │          │         State         │        Context         │
#   ├──────────┼───────────────────────┼────────────────────────┤
#   │ 可变性    │ 节点可写，reduce 合并   │ 只读，不可修改         │
#   ├──────────┼───────────────────────┼────────────────────────┤
#   │ 生命周期  │ 每次 invoke 变化       │ 跨调用稳定             │
#   ├──────────┼───────────────────────┼────────────────────────┤
#   │ 用途      │ 对话历史、计算结果      │ 配置、资源、运行时环境 │
#   ├──────────┼───────────────────────┼────────────────────────┤
#   │ 传递方式  │ 自动流转               │ Runtime 注入           │
#   ├──────────┼───────────────────────┼────────────────────────┤
#   │ 持久化    │ checkpoint 保存       │ 不保存                 │
#   └──────────┴───────────────────────┴────────────────────────┘

# 定义状态
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    response: str


# 1.定义 Context 结构，类似于yml文件
@dataclass
class MyContextSchema:
    model_name: str
    db_conn: str
    api_key: str


# 2.定义节点函数：处理用户信息
def process_message(state: AgentState, runtime: Runtime[MyContextSchema]) -> dict:
    # 获取RuntimeContex信息
    model_name = runtime.context.model_name
    db_conn = runtime.context.db_conn
    api_key = runtime.context.api_key
    print(f"Model name: {model_name}, DB connection: {db_conn}, API key: {api_key}")

    # 处理用户信息
    return {
        "messages": [AIMessage(content="Processed message.")],
        "response": "Processed message."
    }


# 3.定义节点函数：生成最终响应
def generate_response(state: AgentState, runtime: Runtime[MyContextSchema]) -> dict:
    pre_response = state["response"]
    final_response = "最终结果" + pre_response + runtime.context.model_name

    return {
        "messages": [AIMessage(content=final_response)],
        "response": final_response
    }


if __name__ == "__main__":
    # 创建图
    graph = StateGraph(AgentState, context_schema=MyContextSchema)
    graph.add_node("process_message", process_message)
    graph.add_node("generate_response", generate_response)

    graph.add_edge(START, "process_message")
    graph.add_edge("process_message", "generate_response")
    graph.add_edge("generate_response", END)

    app = graph.compile()

    # 运行
    context = MyContextSchema(
        model_name="gpt-3.5-turbo",
        db_conn="localhost:5432",
        api_key="123456"
    )
    result = app.invoke({"messages": [], "response": ""}, context=context)
    print("result:", result)
