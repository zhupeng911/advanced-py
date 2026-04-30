from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from agent.config import OPENAI_API_KEY  # 先导入 config，触发 warnings 过滤

# 功能：链式调用
# 将 Prompt + LLM + Parser 组合成 Chain
# 1. 创建 Prompt 模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个历史老师，你会耐心的教导我有关的事情。同时你的回答会相对精简，在五十字内。"),
    ("user", "{user_input}")  # 用户输入占位符
])

# 2. 初始化大模型
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

# 3.定义解析器，把LLM返回的AIMessage转成字符串
parser = StrOutputParser()
# 没有 parser 时
# response = llm.invoke(...)
# print(response)  # AIMessage(content='你好', ...)
# print(response.content)  # '你好'  ← 需要手动取 .content

# 有 parser 时
# chain = prompt | llm | parser
# result = chain.invoke(...)
# print(result)  # '你好'  ← 直接就是字符串


# 4.链式调用
chain = prompt | llm | parser
# 等价于：
# prompt = prompt.invoke({"question": "..."})  # 生成提示词
# response = llm.invoke(prompt)  # 调用模型
# result = parser.invoke(response)  # 提取字符串

# 5.调用chain
response = chain.invoke({"user_input": "python是什么"})
print(response)
