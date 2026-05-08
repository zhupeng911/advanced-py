from langchain.chat_models import init_chat_model
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

from lang_chain.config import OPENAI_API_KEY

# 可持续记忆（RunnableWithMessageHistory）：保存到内存

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

# 2.根据会话ID获取历史记录，如果不存在则创建，保存到内存
store = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """获取会话历史"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# 包装成带记忆的Runnable
# RunnableWithMessageHistory 是 LangChain 的记忆组件，让 AI 具有多轮对话上下文能力
#   工作原理：
#   - 每次调用时，自动从 get_session_history(session_id) 获取历史消息
#   - 把历史消息注入到 prompt 的 history 变量中
#   - LLM 就能"记住"之前说了什么
runnable_with_history = RunnableWithMessageHistory(
    runnable=chain,  # 被增强的 chain（你的 prompt | llm | parser）
    get_session_history=get_session_history,  # 获取会话历史的函数，会被调用，返回该 session_id 的聊天历史，自动拼接进 prompt
    input_messages_key="input",  # 输入变量名，对应 prompt 中的 key
    history_messages_key="history"  # 历史消息的变量名，会被拼进 prompt
)

# 6.模拟多用户调用大模型
current_uid = "default"

while True:
    user_input = input(f"[{current_uid}] 你: ").strip()
    if not user_input:
        continue

    # 切换 session
    if user_input.startswith("/sid "):
        current_uid = user_input.split(maxsplit=1)[1]
        print(f"已切换到会话: {current_uid}\n")
        continue

    # 调用 chain
    result = runnable_with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": current_uid}}
    )
    print(f"AI: {result}\n")
