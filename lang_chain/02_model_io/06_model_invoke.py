from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.messages import SystemMessage

from lang_chain.config import OPENAI_API_KEY

# 1.初始化llm
llm = init_chat_model(
    model='deepseek-chat',
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
# 2.构建提示词
messages = [
    SystemMessage(content="你是Python助手"),
    HumanMessage(content="python简介"),
    AIMessage(content="我是一名大模型助手")
]

# 3.同步调用大模型
response = llm.invoke(messages)
print(f'type(response): {type(response)}')
print("response.content", response.content)
