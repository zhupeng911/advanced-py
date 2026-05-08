from typing import TypedDict, Annotated, List

from langchain.chat_models import init_chat_model

from lang_chain.config import OPENAI_API_KEY


# 1.自定义输出字段
class Animal(TypedDict):
    animal: Annotated[str, "动物名称"]
    emoji: Annotated[str, "动物表情"]


class AnimalList(TypedDict):
    animals: Annotated[List[Animal], "动物列表"]


# 2. 格式化Prompt
prompt = [{"role": "user", "content": "请输出三种动物列表以及表情"}]

# 3.调用大模型并格式化
llm = init_chat_model(
    model='deepseek-chat',
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
response = llm.with_structured_output(AnimalList).invoke(prompt)
print(response)
