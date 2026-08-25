from langchain.chat_models import init_chat_model

from lang_chain.config import OPENAI_API_KEY


# 1.创建一个语言模型
def init_llm_client():
    return init_chat_model(
        model="deepseek-chat",
        model_provider="deepseek",
        api_key=OPENAI_API_KEY,
        base_url="https://api.deepseek.com"
    )


# 2.主函数
def main():
    llm = init_llm_client()
    user_input = "你是谁"

    # 2.1 直接输出
    # response = llm.invoke(user_input)

    # 2.2 流式输出
    response = llm.stream(user_input)
    for chunk in response:
        print(chunk.content, end="", flush=True)


if __name__ == "__main__":
    main()
