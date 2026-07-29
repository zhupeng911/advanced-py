from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from lang_graph.llm import init_llm


# 单智能体
# 定义工具
def get_weather(city: str) -> str:
    """查询指定城市的天气情况。"""
    return f'今天{city}的天气是晴天'


# 定义大模型
llm = init_llm()

# 定义Agent
agent = create_agent(
    model=llm, # 添加模型
    tools=[get_weather], # 添加工具
)

# 测试Agent
human_message = HumanMessage(content="今天北京的天气如何？")
response = agent.invoke({"messages": [human_message]})
print(response["messages"][-1].content)