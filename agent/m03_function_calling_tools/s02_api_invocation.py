import requests
from openai import OpenAI

from agent.config import OPENAI_API_KEY


# 功能：自定义API 调用
def create_client():
    return OpenAI(api_key=OPENAI_API_KEY, base_url="https://api.deepseek.com")


# 1.自定义API      http://127.0.0.1:8081/api/users
def get_users():
    try:
        res = requests.get("http://127.0.0.1:8081/api/users")
        # 如果响应状态码不是200，就会抛出异常
        res.raise_for_status()
        # 取出json指定字段的数据
        return f'所有用户：{res.json()["data"]["users"]}'
    except requests.RequestException as e:
        return f'请求失败：{e}'


# 2.定义工具元数据
get_users_tool = {
    "name": "get_users",  # 函数名称
    "description": "获取所有学生",
    "parameters": {
        "type": "object",
        "properties": {},  # 参数为空，那么这两个地方也是空的
        "required": []
    }
}

# 3.定义工具集合
tools = [
    {
        "type": "function",
        "function": get_users_tool
    }
]


def happy_chat(agent_client, tools, prompt):
    # 1.第一次调用，让模型生成中间结果
    messages = [
        {
            "role": "system",
            "content": "你是一个善解人意会热心回答人问题的助手。如果你感觉你回答不了当前问题，就会调用函数来回答。"}
        ,
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

    # 2.判断是否调用工具
    if message.tool_calls:
        for tool_call in message.tool_calls:  # ChatCompletionMessageFunctionToolCall(id='call_00_1iGg09mVZNWFcLuNPc7fx0mN', function=Function(arguments='{}', name='get_users'), type='function', index=0)
            if tool_call.function.name == "get_users":
                # 这里无参数，直接调用函数就行
                all_users = get_users()
                messages.append(message) # 添加中间结果
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": all_users
                })

                # 第二次调用，让模型基于工具返回的结果再生成最终答案
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
    happy_chat(client, tools, "获取所有学生")
