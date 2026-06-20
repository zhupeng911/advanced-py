from typing import TypedDict

from langchain.chat_models import init_chat_model
from langgraph.constants import END, START
from langgraph.graph import StateGraph

from lang_chain.config import OPENAI_API_KEY


# 定义状态
class State(TypedDict):
    query: str
    answer: str


# 定义节点
def node(state: State):
    print('node开始...')

    model = init_chat_model(
        model="deepseek-chat",
        model_provider="deepseek",
        api_key=OPENAI_API_KEY,
        base_url="https://api.deepseek.com"
    )
    result = model.invoke(["user", state["query"]])
    print('node结束...')
    return {"answer": result}


if __name__ == "__main__":
    # 创建图
    graph = (
        StateGraph(State)
        .add_node("node", node)
        .add_edge(START, "node")
        .add_edge("node", END)
        .compile()
    )
    inputs = {"query": "写100字介绍LangChain"}

    # 流式运行：LLM
    for chunk, meta_data in graph.stream(inputs, stream_mode="messages"):
        # print(chunk, end="")
        print(chunk.content, end="")
