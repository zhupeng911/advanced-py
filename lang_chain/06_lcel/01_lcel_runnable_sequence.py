from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from lang_chain.config import OPENAI_API_KEY

# 顺序链：RunnableSequence

# 未使用chain格式
# 1.提示词
# chat_prompt_template = ChatPromptTemplate.from_messages(
#     [
#         ("system", "你是一个{role}. 请简短回答我的问题"),
#         ("human", "请回答，{question}"),
#     ]
# )
# chat_prompt = chat_prompt_template.invoke({"role": "AI助手", "question": "什么是LangChain,100字以内"})
# print(f'chat_prompt: {chat_prompt}')
#
# # 2.大模型
# llm = init_chat_model(
#     model="deepseek-chat",
#     model_provider="deepseek",
#     api_key=OPENAI_API_KEY,
#     base_url="https://api.deepseek.com"
# )
# response = llm.invoke(chat_prompt)
# print(f'未解析结果: {response}')
#
# # 3.解析器
# parser = StrOutputParser()
# result = parser.invoke(response)
# print(f'解析结果: {result}')


# 使用chain格式
# 1.提示词
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个{role}. 请简短回答我的问题"),
        ("human", "请回答，{question}"),
    ]
)

# 2.大模型
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

# 3.解析器，把LLM返回的AIMessage转成字符串
parser = StrOutputParser()

# 4.顺序链
chain = prompt | llm | parser
result = chain.invoke({"role": "AI助手", "question": "什么是LangChain,100字以内"})
print(f'type(chain): {type(chain)}')
print(f'解析结果: {result}')
