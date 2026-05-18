from langchain_community.embeddings import DashScopeEmbeddings

from lang_chain.config import DASHSCOPE_API_KEY

# DashScopeEmbeddings标准化

# 1.获取专业向量模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=DASHSCOPE_API_KEY,
    max_retries=5
)

# 2.文本向量化
input_text = "我的名字是Jack"
query_result = embeddings.embed_query(input_text)
print(f"文本向量: {query_result}")
print(f"文本向量长度: {len(query_result)}", sep="")  # 文本向量长度: 1024，阿里百炼固定长度

# 3.文档向量化
document_result = embeddings.embed_documents(
    [
        "西游记",
        "红楼梦",
        "三国演义",
        "水浒传"
    ]
)
print(f'文档向量:{document_result}')
print("文档向量数量：", len(document_result))
print("文档向量长度：", len(document_result[0]), sep="")
