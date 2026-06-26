from langchain_classic.agents import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor

from lang_chain.config import OPENAI_API_KEY


# 定义大模型 v0.3版本
# 版本冲突，后面不要用了
def init_llm():
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=OPENAI_API_KEY,
        base_url="https://api.deepseek.com",
        temperature=0.1,
        max_tokens=1024,
    )


def book_hotel(hotel_name: str):
    """预订指定名称的酒店。"""
    print(f'成功预定{hotel_name}的住宿')
    return f'成功预定{hotel_name}的住宿'


def book_flight(from_airport: str, to_airport: str):
    """预订从出发地到目的地的航班。"""
    print(f'成功预定从{from_airport}到{to_airport}的航班')
    return f'成功预定从{from_airport}到{to_airport}的航班'


flight_assistant = create_react_agent(  # 现在已经不推荐使用
    llm=init_llm(),
    tools=[book_flight],
    prompt=ChatPromptTemplate.from_messages([
        ("system",
         "你是一个专业的航班预订助手，帮助用户预订航班。"
         "工作流程："
         "1.分析用户需求提取出发地和目的地\n"
         "2.调用工具book_flight预订航班\n"
         "3.返回预订结果，向主管汇报结果\n"
         "注意：每次处理一个请求，完成后立即结束，不要重复调用工具"
         ),
        ("placeholder", "{messages}"),
        ("placeholder", "\n\n{tools}\n\n可用的工具：{tool_names}\n\n{agent_scratchpad}"),
    ]),
)

hotel_assistant = create_react_agent(
    llm=init_llm(),
    tools=[book_hotel],
    prompt=ChatPromptTemplate.from_messages([
        ("system",
         "你是一个专业的酒店预订助手，帮助用户预订酒店。"
         "工作流程："
         "1.分析用户需求提取酒店名称\n"
         "2.调用工具book_hotel预订酒店\n"
         "3.返回预订结果，向主管汇报结果\n"
         "注意：每次处理一个请求，完成后立即结束，不要重复调用工具"
         ),
        ("placeholder", "{messages}"),
        ("placeholder", "\n\n{tools}\n\n可用的工具：{tool_names}\n\n{agent_scratchpad}"),
    ]),
)

# 主agent
supervisor = create_supervisor(
    agents=[flight_assistant, hotel_assistant],
    llm=init_llm(),
    prompt=ChatPromptTemplate.from_messages([
        ("system",
         "你是一个智能任务调度主管，负责调度多个智能助手完成用户请求。"
         "工作流程："
         "1.分析用户需求提取任务\n"
         "2.调用工具flight_assistant和hotel_assistant完成任务\n"
         "3.返回结果，向用户汇报结果\n"
         "注意：每次处理一个请求，完成后立即结束，不要重复调用工具"
         ),
        ("placeholder", "{messages}"),
    ]),
).compile()

if __name__ == "__main__":
    # 调用主agent
    for chunk in supervisor.stream({
        "messages": [
            {"role": "user", "content": "我想从北京去上海出差，预定一间标准间，价格不要超过500元，预定明天的"}
        ]
    }):
        print(chunk)
