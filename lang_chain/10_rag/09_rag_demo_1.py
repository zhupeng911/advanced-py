from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Redis
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lang_chain.config import DASHSCOPE_API_KEY

# 1. 初始化Embedding模型
embedding_model = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=DASHSCOPE_API_KEY
)

# 2.待处理文本分割
pdf_document = PyPDFLoader(
    file_path="assets/sample.pdf",
    extraction_mode="plain"
).load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=10,
    length_function=len
)

splitter_documents = splitter.split_documents(documents=pdf_document)

# 3.文本向量化
embeddings = embedding_model.embed_documents(
    [doc.page_content for doc in splitter_documents]
)
for idx, text in enumerate(embeddings, start=1):
    print(f'文本{idx}：{splitter_documents[idx - 1].page_content}')
    print(f'向量长度: {len(text)}')

# 4.连接redis-stack
vector_store = Redis.from_documents(
    documents=splitter_documents,
    embedding=embedding_model,
    index_name="idx",
    redis_url="redis://localhost:6379",
)