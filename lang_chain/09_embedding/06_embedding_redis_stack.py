# redis stack作为向量存储数据库

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Redis
from langchain_core.documents import Document

from lang_chain.config import DASHSCOPE_API_KEY

# 1.获取专业向量模型，阿里Embedding模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=DASHSCOPE_API_KEY
)

# 2.准备要向量化的文档
texts = [
    "我的名字叫jack",
    "我今年18岁",
    "我毕业于南京大学"
]

documents = [Document(page_content=text) for text in texts]

# 3.连接redis-stack，并存入向量
vector_store = Redis.from_documents(
    documents=documents,
    embedding=embeddings,
    redis_url="redis://localhost:6379",  # 连接redis
    index_name="my_em",  # key-predix
)

# 4.后续直接检索
retriever = vector_store.as_retriever(search_kwargs={"k": 1})
results = retriever.invoke("名字")
for result in results:
    print(result)
