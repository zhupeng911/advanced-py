import json
from typing import TypedDict

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

from lang_chain.config import OPENAI_API_KEY


# 1.定义普通工具
@tool
def get_weather(city: str) -> str:
    """根据城市名称查询天气信息。"""
    if city == "上海":
        return "上海的天气为:{{'weather': 'sunny', 'temperature': '20摄氏度'}}"
    elif city == "北京":
        return "北京的天气为:{{'weather': 'sunny', 'temperature': '25摄氏度'}}"
    else:
        return "其他城市的天气为:{{'weather': 'sunny', 'temperature': '30摄氏度'}}"


tools = [get_weather]

# 2.定义大模型
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)


# PS：结构化输出
class WeatherCompareOutput(TypedDict):
    beijing_temp: float
    shanghai_temp: float
    hotter_city: str
    summary: str


# 3.创建Agent v1.0版本
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "你是一个 helpful的天气助手.需要使用提供的工具来完成用户请求"
        "当用户询问多个城市天气时，请使用多个工具分别查询每个城市天气，然后将结果进行比较，并返回最热的城市。"
    ),
    response_format=WeatherCompareOutput
)

# 4.执行Agent
result = agent.invoke(
    {"input": "请问北京和上海的天气，哪个城市更热"}
)
print(result)
print(f'Agent结构化结果: {json.dumps(result["structured_response"], ensure_ascii=False, indent=2)}')
