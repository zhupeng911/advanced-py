from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Redis
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lang_chain.config import OPENAI_API_KEY, DASHSCOPE_API_KEY

# 需求：完整RAG相似性搜索案例-AI智能运维助手
# 技术栈：LangChain + text-embedding-v4 + redis-stack + Deepseek

# 1.创建大语言模型 DeepSeek
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com",
    temperature=0.7
)

# 2.提示词模版
# context: 文档内容，后续会传入
# question: 用户问题
prompt = PromptTemplate(
    template="你是一个助手，请根据给定的文档内容回答问题。文档内容：{context}。问题：{question}",
    input_variables=["context", "question"]
)

# 3. 文档向量化
# 3.1 文档加载
documents = Docx2txtLoader("assets/alibaba-java.docx").load()
# 3.2 文档分割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0,
    length_function=len
)
split_documents = text_splitter.split_documents(documents)
print(f'文档数量：{len(split_documents)}')
# 3.3 文档向量化，存到Redis-Stack
embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=DASHSCOPE_API_KEY
)
vector_store = Redis.from_documents(
    documents=split_documents,
    embedding=embeddings,
    redis_url="redis://localhost:6379",
    index_name="alibaba-java"
)

# 4. 创建Runnable链式调用，进行提问
rag_chain = (
        {
            "context": vector_store.as_retriever(search_kwargs={"k": 1}),  # 相似性搜索
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
)
question = "502什么意思？"
response = rag_chain.invoke(question)
print(f'问题：{question}')
print(f'回答：{response}')
