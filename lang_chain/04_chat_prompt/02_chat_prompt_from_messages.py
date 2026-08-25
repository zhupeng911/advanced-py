from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from lang_chain.config import OPENAI_API_KEY

# 功能：3种入参、3种方法
# from_messages方法实例化提示词模版
# 1.rom_messages方法实例化提示词模版1：元组
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个专业的AI工程师，你的名字是：{name}"),
        ("human", "请回答：{user_input}")
    ]
)

# 2.rom_messages方法实例化提示词模版2：字典
# chat_prompt_template = ChatPromptTemplate.from_messages(
#     [
#         {"role": "system", "content": "你是一个专业的AI工程师，你的名字是：{name}"},
#         {"role": "human", "content": "请回答：{user_input}"}
#     ]
# )

# 3.rom_messages方法实例化提示词模版3：Message
# chat_prompt_template = ChatPromptTemplate.from_messages(
#     [
#         SystemMessage(content="你是一个专业的AI工程师，你的名字是：{name}"),
#         HumanMessage(content="请回答：{user_input}")
#     ]
# )

# 1.使用format_messages方法格式化生成具体的提示词
# 2.使用invoke方法格式化生成具体的提示词
# 3.使用format方法格式化生成具体的提示词
# chat_prompt = chat_prompt_template.format_messages(name='朱鹏', user_input='简述python发展历史')  # 关键字占位传参
# chat_prompt = chat_prompt_template.invoke({"name": "朱鹏", "user_input": "简述python发展历史"})
chat_prompt = chat_prompt_template.format(name='朱鹏', user_input='简述python发展历史')
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
