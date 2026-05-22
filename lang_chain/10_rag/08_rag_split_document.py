from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# RecursiveCharacterTextSplitter的split_documents() 方法详解
# 入参： Iterable[Document]，即 Document 对象的可迭代集合（通常是 list）
# 返回值：List[Document]，分割后的 Document 列表
# 使用规则：从 Loader（如 TextLoader、PyPDFLoader）加载来的就是 Document 列表，直接用 split_documents()是最规范的做法
# 优点：为什么 RAG 流程几乎都用 split_documents()
# 1.来源可追溯：metadata 中的 source、页码（PDF）、行号等会被带到向量库，检索时能告诉用户答案来自哪个文件、哪一
# 2.多文档批处理：一次性传入 loader.load() 的所有 Document，无需循环
# 3.过滤检索：向量库（FAISS、Redis、Chroma 等）支持按 metadata 过滤，如 filter={"source": "xx.pdf"}
# 4.start_index：配合 add_start_index=True，可定位原文位置，便于做高亮、上下文扩展


# 1.TXT文档加载器
txt_loader = TextLoader(
    file_path="assets/sample.txt",
    encoding="utf-8",
).load()

# 2.定义递归文本分割器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=10,
    length_function=len
)

# 3.分割文本，执行过程：
# - 取出唯一一个 Document 的 page_content（全文）。
# - 按 chunk_size=100、chunk_overlap=10 递归切分（先按 \n\n → \n →   → ""）。
# - 假设切出 N 块，则返回 N 个新 Document，每个 Document：
# - page_content：约 ≤100 字符的文本块（最后一块可能更短）
# - metadata：{"source": "assets/sample.txt"} ← 完整继承
splitter_documents = text_splitter.split_documents(documents=txt_loader)

print(f"分割文本数量: {len(splitter_documents)}")
for document in splitter_documents:
    print(f'文档片段: {document.page_content}')
    print(f'文档片段大小: {len(document.page_content)}')