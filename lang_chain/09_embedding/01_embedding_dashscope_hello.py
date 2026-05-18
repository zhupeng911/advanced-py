# 直连阿里百炼版本
# 提前配置环境变量 DASHSCOPE_API_KEY
from http import HTTPStatus

import dashscope

from lang_chain.config import DASHSCOPE_API_KEY

input_text = "我的名字是Jack"
resp = dashscope.TextEmbedding.call(
    model="text-embedding-v4",
    input=input_text,
    api_key=DASHSCOPE_API_KEY  # 默认，提前配好
)
if resp.status_code == HTTPStatus.OK:
    print(f'resp: {resp}')
    print(f'status code: {resp.status_code}')
    print(f'request_id: {resp.request_id}')
    print(f'code: {resp.code}')
    print(f'message: {resp.message}')
    print(f'usage: {resp.usage}')
    print(f'output.embeddings.embedding: {resp.output["embeddings"][0]["embedding"]}')
