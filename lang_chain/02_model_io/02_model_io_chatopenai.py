from langchain_openai import ChatOpenAI

from lang_chain.config import OPENAI_API_KEY

# ChatOpenAI模型，v0.3的写法，也不常用
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
# LangChain 会自动把 {"role": "...", "content": "..."} 格式的 dict 转换为对应的 SystemMessage、HumanMessage 等对象
messages = [
    {"role": "system", "content": "你是一个Python专家"},
    {"role": "user", "content": "那你是谁"}
]

# 调用语言模型
response = llm.invoke(messages)
print("response.content", response.content)
