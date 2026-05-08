from datetime import datetime

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

from lang_chain.config import OPENAI_API_KEY

# 部分提示词实例化提示词模版
# 1.创建一个PromptTemplate对象，时间变量使用partial_variables预设，其他变量使用input_variables预设
prompt_template = PromptTemplate.from_template(
    "当前时间: {time}, 你是一个专业的{role},请回答我的问题：{question}",
    partial_variables={
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
)

# 写法2
# prompt_template = PromptTemplate(
#     template="当前时间: {time}, 你是一个专业的{role},请回答我的问题：{question}",
#     input_variables=["time", "role", "question"],
#     partial_variables={
#         "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }
# )

# 2.使用format方法格式化生成具体的提示词
prompt = prompt_template.format(
    role='python开发工程师',
    question='今天是周几')
print(f'prompt: {prompt}')

# 3.调用大模型
llm = init_chat_model(
    model='deepseek-chat',
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
response = llm.invoke(prompt)
print(response.content)
