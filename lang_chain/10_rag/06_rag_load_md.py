from langchain_community.document_loaders import UnstructuredMarkdownLoader

# 加载MarkDown文件
file_path = "assets/sample.md"

md = UnstructuredMarkdownLoader(
    file_path=file_path,
    mode="single",
).load()

print(md)
