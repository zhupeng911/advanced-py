from langchain_community.document_loaders import JSONLoader

# 加载JSON文件
file_path = "assets/sample.json"

json = JSONLoader(
    file_path=file_path,
    jq_schema=".",  # jq 查询表达式，用于从 JSON 中提取数据。"." 表示提取整个 JSON 根对象（所有字段）
    text_content=False  # 提取的内容是否必须为字符串类型。True（默认）要求提取结果是字符串；False 允许提取非字符串类型（如 dict、list、数字等），适用于结构化 JSON   
).load()

print(json)
