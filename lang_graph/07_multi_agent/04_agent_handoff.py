from typing import Annotated

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.constants import START
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import InjectedState
from langgraph.types import Command, Send

from lang_chain.config import OPENAI_API_KEY

# 1.初始化大语言模型
model = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com",
)


# 2.定义Handoff工具工厂
def create_agent_handoff_tool(*, agent_name: str, description: str | None = None):
    name = f"transfer_to_{agent_name}"
    description = description or f"移交给 {agent_name}"

    @tool(name, description=description)
    def handoff_tool(
            task_description: Annotated[str, "描述下一个Agent应该做什么"],
            state: Annotated[MessagesState, InjectedState]
    ) -> Command:
        task_description_message = {
            "role": "user",
            "content": task_description
        }
        agent_input = {
            **state,
            "messages": [task_description_message]
        }
        return Command(
            goto=[Send(agent_name, agent_input)],
            graph=Command.PARENT
        )

    return handoff_tool


# 3.定义工具
@tool("book_flight")
def book_flight(from_airport: str, to_airport: str):
    """预订从出发地到目的地的航班。"""
    return f'成功预定从{from_airport}到{to_airport}的航班'


@tool("book_hotel")
def book_hotel(hotel_name: str):
    """预订指定名称的酒店。"""
    return f'成功预定{hotel_name}的住宿'


# 4.定义Handoff工具
transfer_to_flight_assistant = create_agent_handoff_tool(
    agent_name="flight_assistant",
    description="将任务移交给航班助手"
)

transfer_to_hotel_assistant = create_agent_handoff_tool(
    agent_name="hotel_assistant",
    description="将任务移交给酒店助手"
)

# 5.定义Agent
flight_assistant = create_agent(
    model=model,
    tools=[book_flight, transfer_to_hotel_assistant],
    name="flight_assistant"
)
hotel_assistant = create_agent(
    model=model,
    tools=[book_hotel, transfer_to_flight_assistant],
    name="hotel_assistant"
)

# 6.构建多Agent图
multi_agent_graph = (
    StateGraph(MessagesState)
    .add_node(flight_assistant)
    .add_node(hotel_assistant)
    .add_edge(START, "flight_assistant")
    .compile()
)

if __name__ == "__main__":
    result = multi_agent_graph.invoke({
        "messages": [
            {"role": "user", "content": "预订从北京到上海的航班，并住在喜来登酒店"}
        ]
    })

    for msg in result["messages"]:
        if msg.type in ["human", "ai"]:
            print(msg.content)