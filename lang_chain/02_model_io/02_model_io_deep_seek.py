from langchain_deepseek import ChatDeepSeek

from lang_chain.config import OPENAI_API_KEY

# 接入纯deepseek
llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=3,
)

print(llm.invoke("那你是谁"))
