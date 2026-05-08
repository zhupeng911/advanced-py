from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel

from lang_chain.config import OPENAI_API_KEY

# 并行链：多个子链并行执行，结果合并

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
        ("system", "你是一个计算机专家，请用英文简单回答"),
        ("human", "请翻译，{question}"),
    ]
)
parser_2 = StrOutputParser()
chain_2 = prompt_2 | llm | parser_2

# 3.并行链
parallel_chain = RunnableParallel({
    "chain_1": chain_1,
    "chain_2": chain_2,
})

result = parallel_chain.invoke({"question": "什么是LangChain"})
print(f'结果1: {result["chain_1"]}')
print(f'结果2: {result["chain_2"]}')
