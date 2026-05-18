from langchain_community.document_loaders import PyPDFLoader

# 加载PDF文件
file_path = "assets/sample.pdf"

pdf = PyPDFLoader(
    file_path=file_path,
    # plain 提取文本
    # layout 按布局提取
    extraction_mode="plain"
).load()

print(pdf)
