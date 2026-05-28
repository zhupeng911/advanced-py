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
# 2.构建提示词：三种方式
# 方式一：直接传入字符串
# messages = "那你是谁"

# 方式二：传入列表，列表中可以包含多个字典，每个字典表示一个消息，字典中必须包含 role 和 content 两个键
# messages = [
#     {"role": "system", "content": "你是一个Python专家"},
#     {"role": "user", "content": "那你是谁"}
# ]

# 方式三：传入 SystemMessage、HumanMessage、AIMessage 等对象
messages = [
    SystemMessage(content="你是Python助手"),
    HumanMessage(content="python简介"),
    AIMessage(content="我是一名大模型助手")
]

# 3.同步调用大模型
response = llm.invoke(messages)
print(f'type(response): {type(response)}')
print("response.content", response.content)
