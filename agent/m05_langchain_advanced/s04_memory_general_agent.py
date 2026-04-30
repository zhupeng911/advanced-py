from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from agent.config import OPENAI_API_KEY

# 功能：带记忆的agent


# 1. 配置LLM基本信息与tool
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个聪明的智能助手。当你遇到解决不了的问题时，会调用工具来解决问题。"),
    MessagesPlaceholder(variable_name="history"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
    ("user", "{input}")
])

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)


@tool
def get_weather(location):
    """模拟获得天气信息"""
    return f"{location}当前天气：23℃，晴，风力2级"


tools = [get_weather]

# 2. 创建AgentExecutor(执行器)--负责运行ReAct循环
agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 3.存储记忆，模拟数据库
store = {}


def get_session_history(session_id: str) -> list:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


agent_with_memory = RunnableWithMessageHistory(
    runnable=agent_executor,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# 4.模拟多用户调用agent
current_uid = "default"
while True:
    user_input = input(f"[{current_uid}] 你: ").strip()
    if not user_input:
        continue

    # 切换 session
    if user_input.startswith("/sid "):
        current_uid = user_input.split(maxsplit=1)[1]
        print(f"已切换到会话: {current_uid}\n")
        continue

    # 调用 chain
    result = agent_with_memory.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": current_uid}}
    )
    print(f"AI: {result}\n")
