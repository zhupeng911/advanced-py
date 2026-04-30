# 综合实践：整合所有组件，搭建一个带记忆的 AI 对话机器人
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from agent.config import OPENAI_API_KEY


# 1.创建带记忆的机器人
def create_bot(llm, sys_prompt):
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}")
    ])
    parser = StrOutputParser()
    chain = prompt | llm | parser

    # 内存存储，模拟数据库
    store = {}

    def get_session_history(session_id):
        return store.setdefault(session_id, ChatMessageHistory())  # 不存在就创建，存在就返回

    return RunnableWithMessageHistory(
        runnable=chain,
        get_session_history=get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )


# 2.统一调用
def happy_chat():
    # 1.创建机器人
    llm = ChatOpenAI(
        model="deepseek-chat",
        api_key=OPENAI_API_KEY,
        base_url="https://api.deepseek.com"
    )
    sys_prompt = "你是出色的软件工程师"
    bot = create_bot(llm, sys_prompt)

    # 2.多用户调用机器人
    current_uid = "默认用户"
    while True:
        # 切换 session
        user_input = input(f"[{current_uid}] 你: ").strip()
        if user_input.startswith("/uid "):
            current_uid = user_input.split(maxsplit=1)[1]
            print(f"已切换到会话: {current_uid}\n")
            continue

        # 调用 chain
        result = bot.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": current_uid}}
        )
        print(f"AI: {result}\n")
