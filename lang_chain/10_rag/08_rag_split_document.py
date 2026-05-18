from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

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

# 3.分割文本
splitter_documents = text_splitter.split_documents(documents=txt_loader)

print(f"分割文本数量: {len(splitter_documents)}")
for document in splitter_documents:
    print(f'文档片段: {document.page_content}')
    print(f'文档片段大小: {len(document.page_content)}')