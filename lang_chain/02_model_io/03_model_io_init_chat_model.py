from langchain.chat_models import init_chat_model

from lang_chain.config import OPENAI_API_KEY

# init_chat_model创建一个语言模型， v1.0写法，常用
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com",
    temperature=0.7  # 温度参数，控制生成文本的随机性，范围通常在0到1之间
)

# 调用语言模型
response = llm.invoke("你是谁")
print("response.content", response.content)
