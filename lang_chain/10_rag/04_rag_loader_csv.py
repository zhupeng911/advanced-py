from langchain_community.document_loaders import CSVLoader

# 加载CSV文件
file_path = "assets/sample.csv"

csv = CSVLoader(
    file_path=file_path,
).load()

print(csv)
