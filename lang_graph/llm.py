from langchain.chat_models import init_chat_model

from lang_chain.config import OPENAI_API_KEY


# 全局初始化LLM
def init_llm():
    llm = init_chat_model(
        model="deepseek-chat",
        model_provider="deepseek",
        api_key=OPENAI_API_KEY,
        base_url="https://api.deepseek.com"
    )
    return llm
