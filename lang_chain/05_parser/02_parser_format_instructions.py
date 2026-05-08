from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from openai import BaseModel
from pydantic import Field

from lang_chain.config import OPENAI_API_KEY


# 借助JsonOutputParser的get_format_instructions方法
# 1.自定义输出字段
class Person(BaseModel):
    name: str = Field(description="姓名", min_length=1, max_length=10)
    age: int = Field(description="年龄", ge=0, le=120)
    is_student: bool = Field(description="是否是学生")


# 2.获取格式化指令，用于提示大模型输出json格式
parser = JsonOutputParser(pydantic_object=Person)
format_instructions = parser.get_format_instructions()

# 3.格式化Prompt
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个专业的AI工程师，你的名字是：{name}, 返回json格式的输出"),
        ("human", "请回答：{user_input}, 输出格式: {format_instructions}")
    ]
)
prompt = chat_prompt_template.format(name='朱鹏', user_input='朱鹏是个男生，今天20岁',
                                     format_instructions=format_instructions)

# 4.调用大模型并格式化
llm = init_chat_model(
    model='deepseek-chat',
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
response = llm.invoke(prompt)
result = parser.invoke(response)
print(f'result: {result}')
