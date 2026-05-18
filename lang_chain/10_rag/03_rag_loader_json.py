from langchain_community.document_loaders import JSONLoader

# 加载JSON文件
file_path = "assets/sample.json"

json = JSONLoader(
    file_path=file_path,
    jq_schema=".",  # 提取所有字段
    text_content=False  # 提取内容是否是字符串格式
).load()

print(json)
