from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch

from lang_chain.config import OPENAI_API_KEY

# 分支链：RunnableBranch条件判断，根据不同输入采取不同处理逻辑


# 1.提示词
english_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个英语翻译专家"),
        ("human", "请翻译，{query}"),
    ]
)
japanese_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个日语翻译专家"),
        ("human", "请翻译，{query}"),
    ]
)
korean_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个韩语翻译专家"),
        ("human", "请翻译，{query}"),
    ]
)


# 2.判断用户输入是哪种语言
def determine_language(inputs):
    query = inputs["query"]
    if "英语" in query:
        return "english"
    elif "日语" in query:
        return "japanese"
    else:
        return "korean"


# 3.大模型
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

# 4.解析器
parser = StrOutputParser()

# 5.分支链
chain = RunnableBranch(
    (lambda x: determine_language(x) == 'japanese', japanese_prompt | llm | parser),
    (lambda x: determine_language(x) == 'english', english_prompt | llm | parser),
    (korean_prompt | llm | parser),
)
test_queries = [
    {"query": "请用日语翻译，什么是LangChain"},
    {"query": "请用英语翻译，什么是LangChain"},
    {"query": "请用韩语翻译，什么是LangChain"},
]
for query in test_queries:
    result = chain.invoke(query)
    print(f'结果: {result}')
