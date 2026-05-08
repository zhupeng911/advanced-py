from langchain.chat_models import init_chat_model

from lang_chain.config import OPENAI_API_KEY

llm = init_chat_model(
    model='deepseek-chat',
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
questions = [
    "什么是redis",
    "python简介",
    "java是什么"
]

# 批量调用大模型
response = llm.batch(questions)
print(f'type(response): {type(response)}')

for q, r in zip(questions, response):
    print(f'问题：{q} \n 回答: {r.content}')
