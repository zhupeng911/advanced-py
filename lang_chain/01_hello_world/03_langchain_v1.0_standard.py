import logging

from langchain.chat_models import init_chat_model
from langchain_core.exceptions import LangChainException

from lang_chain.config import OPENAI_API_KEY

# 1.日志格式化
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# 2.创建一个语言模型
def init_llm_client():
    return init_chat_model(
        model="deepseek-chat",
        model_provider="deepseek",
        api_key=OPENAI_API_KEY,
        base_url="https://api.deepseek.com"
    )


# 3.主函数
def main():
    try:
        llm = init_llm_client()
        user_input = "你是谁"

        # 直接输出
        # response = llm.invoke(user_input)

        # 流式输出
        response = llm.stream(user_input)
        for chunk in response:
            print(chunk.content, end="", flush=True)

    except ValueError as e:
        logger.error(e)
    except LangChainException as e:
        logger.error(e)


if __name__ == "__main__":
    main()
