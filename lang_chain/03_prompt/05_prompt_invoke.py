from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

from lang_chain.config import OPENAI_API_KEY

# 提示词格式化方法invoke
# 入参：支持dict或消息对象，format仅支持dict
# 返回值：PromptValue对象，format返回str
# LCEL： 支持，format不支持

# 1.提示词模版
prompt_template = PromptTemplate.from_template("你是专业的{role}，请用一句话介绍：{topic}")

# 2.invoke
prompt = prompt_template.invoke(role="python开发工程师", topic="python")
print(f'prompt: {prompt}')
print(f'type: {type(prompt)}')
print(f'prompt.to_string(): {prompt.to_string()}')
print(f'prompt.to_json(): {prompt.to_json()}')
print(f'prompt.to_messages(): {prompt.to_messages()}')

# 4.调用大模型
llm = init_chat_model(
    model='deepseek-chat',
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
response = llm.invoke(prompt.to_messages())
print(response.content)
