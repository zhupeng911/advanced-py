import requests
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

from lang_chain.config import OPENAI_API_KEY


# 1.定义tool：获取所有用户
def get_users():
    try:
        res = requests.get("http://127.0.0.1:8081/api/users")
        # 如果响应状态码不是200，就会抛出异常
        res.raise_for_status()
        # 取出json指定字段的数据
        return f'所有用户：{res.json()["data"]["users"]}'
    except requests.RequestException as e:
        return f'请求失败：{e}'


# 2.llm导入工具
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个 helpful的助手。"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "请回答，{question}"),
    ]
)
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
llm.bind_tools([get_users])

# 3.chain
parser = StrOutputParser()
chain = prompt | llm | parser
print(chain.invoke({"question": "获取所有用户"}))
