"""
把文本转为向量最核心的作用是可以通过向量之间的计算，来分析文本之间的相似度
常见方法：
    1. 向量余弦相似度（python提供sklearn）
    2. 欧式距离
    3. 点积
"""
from http import HTTPStatus

import dashscope
import numpy as np

from lang_chain.config import DASHSCOPE_API_KEY

# 1.准备数据
texts = [
    "我喜欢吃苹果",
    "苹果是我最喜欢的水果",
    "我喜欢用苹果手机"
]

# 2.依次向量化
embeddings = []
for text in texts:
    resp = dashscope.TextEmbedding.call(
        model="text-embedding-v4",
        input=text,
        api_key=DASHSCOPE_API_KEY
    )
    if resp.status_code == HTTPStatus.OK:
        embeddings.append(resp.output['embeddings'][0]['embedding'])


# 3.计算向量余弦相似度
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


# 4.比较不同文本之间的相似度
print(cosine_similarity(embeddings[0], embeddings[1]))
print(cosine_similarity(embeddings[0], embeddings[2]))
print(cosine_similarity(embeddings[1], embeddings[2]))
