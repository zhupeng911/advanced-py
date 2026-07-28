from typing import TypedDict, List, Annotated

from langgraph.constants import END, START
from langgraph.graph import StateGraph, add_messages
from langgraph.types import Command


# LangGraph Command
# 功能：Command 把状态更新 + 路由跳转合二为一，让节点函数的返回值同时决定"改什么"和"去哪"
# 语法：
#   @dataclass
#   class Command(Generic[N]):
#       graph: str | None = None      # 发到哪个图（None=当前图，PARENT=父图）
#       update: Any | None = None     # 状态更新（替代原来的 dict 返回）
#       resume: Any | None = None     # 中断后恢复的值（配合 interrupt()）
#       goto: Send | Sequence[Send] | str = ()  # 下一步去哪

# 定义状态
class AgentState(TypedDict):
    messages: Annotated[List[str], add_messages]
    current_agent: str
    task_completed: bool


# 定义节点：决策代理核心路由节点
def decision_agent(state: AgentState) -> Command[AgentState]:
    # 检查任务是否完成
    if state["task_completed"]:
        print("任务完成，流程正常结束.")
        return Command(
            update={"messages": [("system", "任务完成，流程正常结束")]},  # 更新状态
            goto=END  # 指定节点
        )

    # 提取消息文本
    last_message = state["messages"][-1] if state["messages"] else ("", "")
    last_msg_content = last_message[1]
    print(f"最新消息文本: {last_msg_content}")

    # 动态路由
    if "数学" in last_msg_content:
        return Command(
            update={"messages": [("system", "路由到数学代理")], "current_agent": "math_agent"},
            goto="math_agent"
        )
    elif "历史" in last_msg_content:
        return Command(
            update={"messages": [("system", "路由到历史代理")], "current_agent": "history_agent"},
            goto="history_agent"
        )
    else:
        return Command(
            update={"messages": [("system", "任务完成")], "task_completed": True},
            goto=END
        )


# 定义数学代理
def math_agent(state: AgentState) -> Command[AgentState]:
    print("数学代理 processing...")
    result = "2+2=4"
    return Command(
        update={
            "messages": [("assistant", f"Math result: {result}")],
            "current_agent": "decision_agent",
            "task_completed": True
        },
        goto="decision_agent"
    )


# 定义历史代理
def history_agent(state: AgentState) -> Command[AgentState]:
    print("历史代理 processing...")
    result = "历史代理处理结果"
    return Command(
        update={
            "messages": [("assistant", f"History result: {result}")],
            "current_agent": "decision_agent",
            "task_completed": True
        },
        goto="decision_agent"
    )


if __name__ == "__main__":
    graph = StateGraph(AgentState)
    graph.add_node("decision_agent", decision_agent)
    graph.add_node("math_agent", math_agent)
    graph.add_node("history_agent", history_agent)

    graph.add_edge(START, "decision_agent")
    graph.add_edge("math_agent", "decision_agent")
    graph.add_edge("history_agent", "decision_agent")
    graph.add_edge("decision_agent", END)

    app = graph.compile()

    # 测试1
    initial_state = {"messages": [("user", "计算数学")], "current_agent": "user", "task_completed": False}
    result = app.invoke(initial_state)
    print("Test 1 result:", result)
