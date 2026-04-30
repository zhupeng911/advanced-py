import json

from openai import OpenAI

from agent.config import OPENAI_API_KEY


# 功能：自定义函数调用

def create_client():
    return OpenAI(api_key=OPENAI_API_KEY, base_url="https://api.deepseek.com")


# 1.定义函数
def get_weather(location):
    # 模拟获得天气信息
    return f"{location}当前天气：23℃，晴，风力2级"


# 2.定义函数的元信息，固定写法，一般仅需改description与name
get_weather_tool = {
    "name": "get_weather",  # 函数名称
    "description": "获取指定城市的天气情况",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",  # 该参数类型
                "description": "城市名称，如北京、上海等"  # 对该参数的描述
            }
        },
        "required": ["location"]  # 声明必填
    }
}

# 3.定义工具，固定写法，有多少个tool就往里追加多少个
tools = [
    {
        "type": "function",
        "function": get_weather_tool
    }
]


def happy_chat(agent_client, tools, prompt):
    # 1.先调用模型，看看是否能直接回答，是否需要调用工具
    messages = [
        {
            "role": "system",
            "content": "你是一个善解人意会热心回答人问题的助手。如果你感觉你回答不了当前问题，就会调用函数来回答。"
        },
        {
            "role": "user", "content": prompt
        }
    ]
    response = agent_client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    message = response.choices[0].message

    # 2.如果有该参数，证明ai调用了工具
    if message.tool_calls:
        for tool_call in message.tool_calls:  # Function(arguments='{"location": "苏州"}', name='get_weather'), type='function', index=0)])
            if tool_call.function.name == "get_weather":
                # 解析参数
                args = json.loads(tool_call.function.arguments)  # 获取用户关键词的参数
                location = args.get("location", "未知地点")

                # 调用真实参数
                weather_info = get_weather(location)

                # 将函数执行结果以"tool"角色传给模型，等待后面二次调用
                messages.append(message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": weather_info
                })

        # 3.第二次调用，让模型基于工具返回的结果再生成最终答案
        final_res = agent_client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        print('已调用工具...')
        print(f'回答:{final_res.choices[0].message.content}')
    else:
        print('未调用工具...')
        print(f'回答:{response.choices[0].message.content}')


if __name__ == '__main__':
    client = create_client()
    happy_chat(client, tools, "苏州今天的天气怎么样")  # 调用工具
    happy_chat(client, tools, "苏州")  # 不调用工具
