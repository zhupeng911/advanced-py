from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

from lang_chain.config import OPENAI_API_KEY

# 提示词方法partial
# 1.提示词模版
prompt_template = PromptTemplate.from_template("你是专业的{role}，请用一句话介绍：{topic}")

# 2.partial固定部分参数
prompt = prompt_template.partial(role="python开发工程师")
print(f'prompt: {prompt}')
print(f'type: {type(prompt)}')

# 3.partial固定剩余参数
prompt = prompt.format(topic="python")
print(f'prompt: {prompt}')
print(f'type: {type(prompt)}')

# 4.调用大模型
llm = init_chat_model(
    model='deepseek-chat',
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
response = llm.invoke(prompt)
print(response.content)
