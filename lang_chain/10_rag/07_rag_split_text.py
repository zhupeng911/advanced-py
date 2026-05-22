from langchain_text_splitters import RecursiveCharacterTextSplitter

# RecursiveCharacterTextSplitter
# 功能： LangChain 中最常用、最推荐的文本分割器，按字符递归分割长文本，尽量保留语义完整性。
# 原理：遵循“重叠后向前取有效内容，且不生成小碎片”的核心分割逻辑，不会让最后一个片段的有效内容只剩扣除重叠后的少量字符
# 按照分隔符优先级列表依次尝试切分文本：
# 1. 先用第一个分隔符（如 "\n\n" 段落）切分
# 2. 如果切出的块仍超过 chunk_size，再用下一个分隔符（如 "\n" 行）继续切
# 3. 依次递归，直到所有块都 ≤ chunk_size
# 默认分隔符顺序：["\n\n", "\n", " ", ""]（段落 → 行 → 空格 → 字符）
# 核心方法：
# split_text 		输入字符串，返回 List[str]
# split_documents 输入 Document 列表，返回切分后的 Document 列表（保留 metadata）
# create_documents(texts, metadatas=None) 	从字符串列表创建 Document 列表
# from_tiktoken_encoder 类方法，用 tiktoken 	按 token 计数分割（适合 OpenAI 模型）
# from_huggingface_tokenizer 					类方法，用 HuggingFace tokenizer 分割

# 1.分割文本内容
content = """
    单文本块最大字符数，可通过 length_function 自定义计数，适配模型上下文窗口（如 GPT-3.5 设 3000 左右），相邻块重叠字符数，保留上下文，需小于 chunk_size，建议为其 10%-20%。,
    按优先级拆分，超尺寸则用下一个分隔符，最后强制拆分，可自定义领域分隔符,默认按字符计数，可自定义（如 tiktoken 按 token 计数，适配大模型）。
"""

# 2.定义递归按字符文本分割器，下面参数均为默认值
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=4000,  # 文本块最大长度，是「最大限制」，不是精确值，当文本结构不符合分隔符时，会出现不均匀分割
    chunk_overlap=200,  # 文本块重叠长度，相邻块之间的重叠长度，用于保留上下文连贯性
    separators=["\n\n", "\n", " ", ""],  # 分隔符优先级列表，递归尝试
    length_function=len,  # 长度计算函数，可改为 token 计数器
    keep_separator=True,  # 是否保留分隔符，默认为 True，可选 "start" / "end" 指定位置
    is_separator_regex=False,  # separators 是否按正则表达式解析
    add_start_index=False,  # 是否在 metadata 中记录每块在原文中的起始位置
    strip_whitespace=True  # 是否去除文本块首尾空格
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
