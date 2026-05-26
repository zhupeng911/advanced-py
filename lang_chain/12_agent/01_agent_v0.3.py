from langchain.chat_models import init_chat_model
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

from lang_chain.config import OPENAI_API_KEY


# 多工具并行调用：一次问题->多次工具调用->聚合回答

# 1.定义普通工具
@tool
def get_weather(city: str) -> str:
    """根据城市名称查询天气信息。"""
    if city == "上海":
        return "上海的天气为:{'weather': 'sunny', 'temperature': '20摄氏度'}"
    elif city == "北京":
        return "北京的天气为:{'weather': 'sunny', 'temperature': '25摄氏度'}"
    else:
        return "其他城市的天气为:{'weather': 'sunny', 'temperature': '30摄氏度'}"


tools = [get_weather]

# 2.定义大模型
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

# 3.提示词模版
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个 helpful的天气助手.需要使用提供的工具来完成用户请求"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# 4.创建Agent v0.3版本与AgentExecutor
# Agent：负责根据用户问题调用相应的工具类
# AgentExecutor：负责协调Agent与工具类的执行过程
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,  # 要执行的Agent实例
    tools=tools,  # Agent可调用的工具类
    verbose=True,  # 是否显示详细信息
    handle_parsing_errors="解析用户请求失败，重新输入"
)

# 5.执行Agent
# 入参：input 由提示词模版确定好了("human", "{input}"),
result = agent_executor.invoke({"input": "请问北京和上海的天气，哪个城市更热"})
print(f'AgentExecutor输出: {result["output"]}')
