from typing import TypedDict

from langgraph.constants import END, START
from langgraph.graph import StateGraph

from lang_graph.llm import init_llm


# stream 流式输出：messages：专门实时输出LLM的每一个字/词
# 定义状态
class State(TypedDict):
    query: str
    answer: str


# 定义节点
def node(state: State):
    print('node开始...')

    model = init_llm()
    result = model.invoke(["user", state["query"]])
    print('node结束...')
    return {"answer": result}


if __name__ == "__main__":
    # 创建图
    app = (
        StateGraph(State)
        .add_node("node", node)
        .add_edge(START, "node")
        .add_edge("node", END)
        .compile()
    )
    inputs = {"query": "写100字介绍LangChain"}

    # 流式运行：LLM
    for chunk, meta_data in app.stream(inputs, stream_mode="messages"):
        # print(chunk, end="")
        print(chunk.content, end="")
