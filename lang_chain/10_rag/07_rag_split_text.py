from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1.分割文本内容
content = """
    单文本块最大字符数，可通过 length_function 自定义计数，适配模型上下文窗口（如 GPT-3.5 设 3000 左右），相邻块重叠字符数，保留上下文，需小于 chunk_size，建议为其 10%-20%。,
    按优先级拆分，超尺寸则用下一个分隔符，最后强制拆分，可自定义领域分隔符,默认按字符计数，可自定义（如 tiktoken 按 token 计数，适配大模型）。
"""

# 2.定义递归按字符文本分割器
# 遵循“重叠后向前取有效内容，且不生成小碎片”的核心分割逻辑，不会让最后一个片段的有效内容只剩扣除重叠后的少量字符
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,  # 文本块最大长度，是「最大限制」，不是精确值，当文本结构不符合分隔符时，会出现不均匀分割
    chunk_overlap=10,  # 文本块重叠长度
    length_function=len,  # 长度计算函数
)

# 3.分割文本，将原始大文本分割成多个文本块
splitter_texts = text_splitter.split_text(content)

# 4.转换为文档对象
splitter_documents = text_splitter.create_documents(splitter_texts)
print(f'原始文本大小: {len(content)}')
print(f'分割文本数量: {len(splitter_texts)}')
print(f'分割文档数量: {len(splitter_documents)}')
for splitter_document in splitter_documents:
    print(f'文档片段大小: {len(splitter_document.page_content)}, 文档内容: {splitter_document.page_content}')
