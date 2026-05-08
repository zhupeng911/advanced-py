from openai import OpenAI

from lang_chain.config import OPENAI_API_KEY

# 原生OpenAI模型，不常用
# 等价于 = LangChain: llm.invoke() / llm.stream()，返回对象可直接.content，见agent-demo.py
llm = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

response = llm.chat.completions.create(  # type: ignore
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个Python专家"},  # 系统提示词
        {"role": "user", "content": "你是谁"}  # 用户提示词
    ],
    stream=False  # 非流式输出, 只会等语句全部生成才返回
)

print(response.choices[0].message.content)
