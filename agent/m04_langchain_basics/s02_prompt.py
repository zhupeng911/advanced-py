from langchain_core.prompts import ChatPromptTemplate

# 功能：构建可复用的 Prompt 模板
# 使用 ChatPromptTemplate 构建可复用的 Prompt 模板
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个历史老师，你会耐心的教导我有关的事情。同时你的回答会相对精简，在五十字内。"),
        ("user", "{user_input}")  # 用户输入占位符
    ]
)
response = prompt.invoke({"user_input": "你叫什么名字"})
print(response)
