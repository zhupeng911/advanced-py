from langchain_community.embeddings import DashScopeEmbeddings
from langchain_redis import RedisConfig

from lang_chain.config import DASHSCOPE_API_KEY

# 1. 初始化Embedding模型
embedding_model = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=DASHSCOPE_API_KEY
)

# 2.待处理文本
texts = [
    "我的名字叫jack",
    "我今年18岁",
    "我毕业于南京大学"
]

# 3.文本向量化
embeddings = embedding_model.embed_documents(texts)
for idx, text in enumerate(embeddings, start=1):
    print(f'文本{idx}：{texts[idx - 1]}')
    print(f'向量长度: {len(text)}')

# 4.【可选】定义元数据
metadata = [{"segment_id": 1}, {"segment_id": 2}, {"segment_id": 3}]

# 5.连接redis-stack
vector_store = RedisConfig(
    embedding=embedding_model,
    index_name="idx",
    redis_url="redis://localhost:6379",
)
