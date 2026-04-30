from langchain_openai import ChatOpenAI

from agent.config import OPENAI_API_KEY

# 功能：模型调用
# 封装 LLM 实例，实现标准调用流程
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
response = llm.invoke("介绍python")
print(response.content)
