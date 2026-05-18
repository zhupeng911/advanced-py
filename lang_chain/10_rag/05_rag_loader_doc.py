from langchain_community.document_loaders import UnstructuredWordDocumentLoader

# 加载DOC文件
file_path = "assets/sample.docx"

doc = UnstructuredWordDocumentLoader(
    file_path=file_path,
    # single 返回单个Document对象
    # elements 按标题等元素切分文档
    mode="single",
).load()

print(doc)
