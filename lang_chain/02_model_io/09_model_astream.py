import asyncio

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage

from lang_chain.config import OPENAI_API_KEY

llm = init_chat_model(
    model='deepseek-chat',
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
messages = [
    SystemMessage(content="你是Python助手"),
    HumanMessage(content="python简介"),
]


# 异步流式调用
async def async_stream_call():
    # astream返回一个异步生成器 无需await修饰    
    response = llm.astream(messages)
    print(f'type(response) = {type(response)}')

    # 异步迭代生成器必须使用await修饰
    async for chunk in response:
        print(chunk.content, end='', flush=True)


if __name__ == "__main__":
    asyncio.run(async_stream_call())
