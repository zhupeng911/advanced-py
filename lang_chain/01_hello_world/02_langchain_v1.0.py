from langchain.chat_models import init_chat_model

from lang_chain.config import OPENAI_API_KEY

# V1.0创建一个语言模型
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

# 调用语言模型
response = llm.invoke("你是谁")
print("response", response)
print("response.response_metadata", response.response_metadata)
print("response.content", response.content)
