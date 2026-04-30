# 构建通用 Agent
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from agent.config import OPENAI_API_KEY

# 1. 配置LLM基本信息
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个聪明的智能助手。当你遇到解决不了的问题时，会调用工具来解决问题。"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),  # 必加，Agent的思考过程
    ("user", "{input}")  # 用户输入占位符
])

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)


# 2.tool定义与配置
@tool
def get_weather(location):
    """模拟获得天气信息"""
    return f"{location}当前天气：23℃，晴，风力2级"


@tool
def get_user_name(user):
    """模拟获得用户名字"""
    return f'用户名字是:{user}'


tools = [get_weather, get_user_name]

# 3.创建Agent
agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)

# 4. 创建AgentExecutor(执行器)--负责运行ReAct循环
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  # 开启verbose以看到ai思考链

# 5. 运行Agent
response = agent_executor.invoke({
    "input": "今天苏州怎么样"  # LLM会决定是否使用工具tool
})
print(response)
print()
print(response["output"])
