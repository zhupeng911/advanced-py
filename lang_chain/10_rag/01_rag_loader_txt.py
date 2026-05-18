from langchain_community.document_loaders import TextLoader

# 加载TXT文件
file_path = "assets/sample.txt"

txt = TextLoader(
    file_path=file_path,
    encoding="utf-8",
).load()

print(txt)  # [Document(metadata={'source': 'assets/sample.txt'}, page_content='Hello world!追加内容.')]
