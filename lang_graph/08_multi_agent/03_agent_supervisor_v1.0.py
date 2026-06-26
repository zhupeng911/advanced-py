from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langgraph_supervisor import create_supervisor

from lang_chain.config import OPENAI_API_KEY

# 1.初始化大语言模型
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com",
)


# 2.定义工具
def book_flight(from_airport: str, to_airport: str):
    """预订从出发地到目的地的航班。"""
    return f'成功预定从{from_airport}到{to_airport}的航班'


def book_hotel(hotel_name: str):
    """预订指定名称的酒店。"""
    return f'成功预定{hotel_name}的住宿'


# 3.创建子agent
flight_assistant = create_agent(
    model=llm,
    tools=[book_flight],
    name="flight_assistant"
)

hotel_assistant = create_agent(
    model=llm,
    tools=[book_hotel],
    name="hotel_assistant",
)

# 4.主agent：调度主管
supervisor = create_supervisor(
    agents=[flight_assistant, hotel_assistant],
    model=llm,
    prompt=(
        "你是一个智能任务调度主管，负责调度多个智能助手完成用户请求。\n"
        "工作流程：\n"
        "1.分析用户需求提取任务\n"
        "2.先调用工具flight_assistant完成航班预订任务\n"
        "3.再调用工具hotel_assistant完成酒店预订任务\n"
        "4.返回结果，向用户汇报结果\n"
        "注意："
        "每个助手只能调用1次，不要重复内容"
        "只能使用中文，不要输出任何原文"
    ),
).compile()

if __name__ == "__main__":
    print("智能旅行调度系统")
    # mock输入数据
    input_data = {
        "messages": [
            HumanMessage(content="我想从北京去上海出差，在希尔顿酒店预定一间标准间，价格不要超过500元")
        ]
    }
    for chunk in supervisor.stream(input_data):
        for agent_name, output in chunk.items():
            if output is None:
                continue
            for msg in output.get("messages", []):
                if isinstance(msg, AIMessage) and msg.content:
                    print(f"[{agent_name}]: {msg.content}")
                    print("-" * 50)