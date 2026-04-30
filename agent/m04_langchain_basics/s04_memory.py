# 功能：记忆功能，添加会话记忆，实现多轮对话
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from agent.config import OPENAI_API_KEY

# 1. 创建 Prompt 模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个历史老师，你会耐心的教导我有关的事情。同时你的回答会相对精简，在五十字内。"),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")  # 用户输入占位符
])

# 2. 初始化大模型
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

# 3.定义解析器，把LLM返回的AIMessage转成字符串
parser = StrOutputParser()

# 4.链式调用
chain = prompt | llm | parser

# 5.模拟存储所有回话
store = {}


def get_session_history(session_id: str) -> list:
    """获取会话历史"""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store.get(session_id, [])


# 包装成带记忆的Runnable
# RunnableWithMessageHistory 是 LangChain 的记忆组件，让 AI 具有多轮对话上下文能力
#   工作原理：
#   - 每次调用时，自动从 get_session_history(session_id) 获取历史消息
#   - 把历史消息注入到 prompt 的 history 变量中
#   - LLM 就能"记住"之前说了什么
runnable_with_memory = RunnableWithMessageHistory(
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
    result = runnable_with_memory.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": current_uid}}
    )
    print(f"AI: {result}\n")
