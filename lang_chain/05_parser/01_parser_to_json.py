from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

from lang_chain.config import OPENAI_API_KEY

# 1. 创建ChatPromptTemplate
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个专业的AI工程师，你的名字是：{name}, 返回json格式的输出"),  # 务必返回json格式
        ("human", "请回答：{user_input}")
    ]
)

# 2.格式化
prompt = chat_prompt_template.format(name='朱鹏', user_input='简述python发展历史')
print(f'prompt: {prompt}')

# 3.调用大模型
llm = init_chat_model(
    model='deepseek-chat',
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
response = llm.invoke(prompt)
print(f'response: {response}')
print(f'response.content: {response.content}')

# 4.输出格式化[默认字段]
parser = JsonOutputParser()
result = parser.invoke(response)
print(f'result: {result}')
