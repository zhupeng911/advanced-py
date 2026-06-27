from typing import TypedDict

from langgraph.constants import END, START
from langgraph.graph import StateGraph


# 跨图状态交互

# 定义父图状态
class ParentState(TypedDict):
    user_query: str  # 父图独有：用户查询
    final_answer: str  # 父图独有：子图处理后的最终答案


# 定义子图状态
class SubgraphState(TypedDict):
    analysis_input: str  # 子图独有：分析输入
    analysis_result: str  # 子图独有：分析输出
    intermediate_step: list  # 子图独有：中间结果


# 定义子图节点
def subgraph_analysis_node(state: SubgraphState) -> SubgraphState:
    query = state["analysis_input"]
    state["intermediate_step"] = [f"解析查询:{query}", "执行分析逻辑", "生成结果"]
    state["analysis_result"] = f'针对{query}的分析结果：子图返回的最终结果'
    return state


# 构建子图
def build_sub_graph() -> SubgraphState:
    sub_builder = StateGraph(SubgraphState)
    sub_builder.add_node("subgraph_analysis_node", subgraph_analysis_node)
    sub_builder.add_edge(START, "subgraph_analysis_node")
    sub_builder.add_edge("subgraph_analysis_node", END)
    return sub_builder.compile()


# 编译子图
compiled_sub_graph = build_sub_graph()


# 定义主图代理
def call_sub_graph_proxy(state: ParentState) -> ParentState:
    # 步骤1
    subgraph_input = {
        "analysis_input": state["user_query"],
        "intermediate_step": [],
        "analysis_result": ""
    }
    # 步骤2：调用子图
    subgraph_response = compiled_sub_graph.invoke(subgraph_input)

    # 步骤3
    return {
        "user_query": state["user_query"],
        "final_answer": subgraph_response["analysis_result"]
    }


# 构建父图
def build_parent_graph() -> StateGraph:
    parent_builder = StateGraph(ParentState)
    parent_builder.add_node("call_sub_graph_proxy", call_sub_graph_proxy)
    parent_builder.add_edge(START, "call_sub_graph_proxy")
    parent_builder.add_edge("call_sub_graph_proxy", END)
    return parent_builder.compile()


if __name__ == "__main__":
    parent_graph = build_parent_graph()
    result = parent_graph.invoke({"user_query": "用户查询"})
    print(result)
