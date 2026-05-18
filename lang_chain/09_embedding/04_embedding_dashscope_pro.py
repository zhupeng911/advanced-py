from http import HTTPStatus

import dashscope
from dashscope.embeddings.multimodal_embedding import MultiModalEmbeddingItemBase
from streamlit import json

from lang_chain.config import DASHSCOPE_API_KEY

# 阿里百炼多模态向量化

# 1. 获取多模态向量化模型，支持文本、图片、视频的向量化
resp = dashscope.MultiModalEmbedding.call(
    model="tongyi-embedding-vision-plus-2026-03-06",  # 提前开启服务
    dashscope_api_key=DASHSCOPE_API_KEY,
    input=[MultiModalEmbeddingItemBase(text="我的名字是Jack")]
)

format_resp = ""

# 2.处理模型结果，格式化输出
if resp.status_code == HTTPStatus.OK:
    format_resp = {
        "status_code": resp.status_code,
        "request_id": getattr(resp, "request_id", ""),
        "code": getattr(resp, "code", ""),
        "message": getattr(resp, "message", ""),
        "output": resp.output,
        "usage": resp.usage,
    }
    print(json.dumps(format_resp))
