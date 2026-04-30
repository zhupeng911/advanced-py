from openai import OpenAI

from agent.config import OPENAI_API_KEY

# 功能：LLM 原生SDK 模型调用
# 等价于 = LangChain: llm.invoke() / llm.stream()，返回对象可直接.content，见agent-demo.py

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com")

response = client.chat.completions.create(  # type: ignore
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},  # 提示词角色
        {"role": "user", "content": "python简介"},  # 用户输入的对话
    ],
    stream=False  # 非流式输出, 只会等语句全部生成才返回
)

content = response.choices[0].message.content
print(f'Content: {content}')
