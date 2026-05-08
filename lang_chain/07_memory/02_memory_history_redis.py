import redis
from langchain.chat_models import init_chat_model
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig

from lang_chain.config import OPENAI_API_KEY

# 可持续记忆（RunnableWithMessageHistory）：保存到redis

# 1.chain
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个 helpful的助手。"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "请回答，{question}"),
    ]
)
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
parser = StrOutputParser()
chain = prompt | llm | parser

# 2.根据会话ID获取历史记录，如果不存在则创建，保存到redis
REDIS_URL = "redis://127.0.0.1:6379"
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def get_session_history(session_id: str) -> RedisChatMessageHistory:
    history = RedisChatMessageHistory(
        session_id=session_id,
        url=REDIS_URL
    )
    return history


runnable_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history=get_session_history,
    # 不需要声明参数。LangChain 内部会在运行时自动从 config["configurable"]["session_id"] 获取值，然后传递给 get_session_history(session_id)
    input_messages_key="question",  # 输入消息的键
    history_messages_key="history",  # 历史消息的键
)

# 3.运行
config = RunnableConfig(configurable={"session_id": "user_001"})
print(runnable_with_history.invoke({"question": "我叫朱鹏，我喜欢python"}, config))
print(runnable_with_history.invoke({"question": "我是谁"}, config))

config2 = RunnableConfig(configurable={"session_id": "user_002"})
print(runnable_with_history.invoke({"question": "我叫张三，我喜欢java"}, config2))
print(runnable_with_history.invoke({"question": "我是谁"}, config2))
