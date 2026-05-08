from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from lang_chain.config import OPENAI_API_KEY

# 串行链：多个子链叠加串行，而顺序链只只有一个链式结构

# 1.子链1
prompt_1 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个计算机专家，请用中文简单回答"),
        ("human", "请介绍，{question}"),
    ]
)
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
parser_1 = StrOutputParser()
chain_1 = prompt_1 | llm | parser_1

# 2.子链2
prompt_2 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个英语翻译专家"),
        ("human", "请翻译，{question}"),
    ]
)
parser_2 = StrOutputParser()
chain_2 = prompt_2 | llm | parser_2

# 3.串行链（将子链1和子链2串联起来，并将子链1的结果作为子链2的输入）
full_chain = chain_1 | (lambda content: {"question": content}) | chain_2
result = full_chain.invoke({"question": "什么是LangChain"})
print(f'结果: {result}')
