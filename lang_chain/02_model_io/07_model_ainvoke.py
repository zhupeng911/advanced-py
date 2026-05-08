import asyncio

from langchain.chat_models import init_chat_model

from lang_chain.config import OPENAI_API_KEY

# 1.初始化llm
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)


# 2.声明异步接口，调用大模型
async def main():
    response = await llm.ainvoke("Python简介")
    print(f'响应类型:{type(response)}')
    print(response.content)


# 运行异步函数
if __name__ == '__main__':
    asyncio.run(main())
