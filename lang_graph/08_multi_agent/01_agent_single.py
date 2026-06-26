from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

from lang_chain.config import OPENAI_API_KEY


# 单智能体
# 定义工具
def get_weather(city: str) -> str:
    """查询指定城市的天气情况。"""
    return f'今天{city}的天气是晴天'


# 定义大模型
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

# 使用LangGraph创建Agent
agent = create_agent(
    model=llm, # 添加模型
    tools=[get_weather], # 添加工具
)
human_message = HumanMessage(content="今天北京的天气如何？")
response = agent.invoke({"messages": [human_message]})
print(response["messages"][-1].content)