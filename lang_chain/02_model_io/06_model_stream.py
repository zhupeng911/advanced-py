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

# 流式调用语言模型
response = llm.stream(messages)
print(f'type(response): {type(response)}')
for chunk in response:
    print(chunk.content, end='', flush=True)
