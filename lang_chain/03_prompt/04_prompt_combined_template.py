from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

from lang_chain.config import OPENAI_API_KEY

# 组合提示词实例化提示词模版
# 1.提示词模版1
prompt_template_a = PromptTemplate.from_template("请用一句话介绍：{topic}")

# 2.提示词模版2
prompt_template_b = PromptTemplate.from_template("要求内容不超过{length}个字")

# 3.组合提示词
prompt_template = prompt_template_a + prompt_template_b
prompt = prompt_template.format(topic="python", length="10")
print(f'prompt: {prompt}')

# 4.调用大模型
llm = init_chat_model(
    model='deepseek-chat',
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
response = llm.invoke(prompt)
print(response.content)
