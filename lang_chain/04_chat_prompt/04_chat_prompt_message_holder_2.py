from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from lang_chain.config import OPENAI_API_KEY

# 功能：MessageHolder隐式调用
# 1.from_messages方法实例化提示词模版
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("placeholder", "{07_memory}"),
        ("system", "你是一个专业的AI工程师，你的名字是：{name}"),
        ("human", "请回答：{user_input}")
    ]
)

# 2.使用format_messages方法格式化生成具体的提示词
chat_prompt = chat_prompt_template.invoke({
    "07_memory": [
        ("human", "你叫什么名字"),
        ("ai", "我叫朱鹏")
    ],
    "name": "朱鹏",
    "user_input": "简述python发展历史"
})

print(f'chat_prompt: {chat_prompt}')

# 3.调用大模型
llm = init_chat_model(
    model='deepseek-chat',
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
response = llm.invoke(chat_prompt)
print(response.content)
