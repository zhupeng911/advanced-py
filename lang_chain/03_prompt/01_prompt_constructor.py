from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

from lang_chain.config import OPENAI_API_KEY

# 构造方法实例化提示词模版
# 1.创建一个PromptTemplate对象，用于生成格式化的提示词模版
prompt_template = PromptTemplate(
    template="你是一个专业的{role},请回答我的问题：{question}",
    input_variables=["role", "question"] # 输入变量，要与format方法中的参数一致
)

# 2.使用format方法格式化生成具体的提示词
prompt = prompt_template.format(
    role='python开发工程师',
    question='简述python发展历史')
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
