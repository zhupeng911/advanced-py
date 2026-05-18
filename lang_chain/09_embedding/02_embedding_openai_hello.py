import json

from openai import OpenAI

from lang_chain.config import DASHSCOPE_API_KEY

# 兼容OpenAI版本

input_text = "我的名字是Jack"
client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
res = client.embeddings.create(
    model="text-embedding-v4",
    input=input_text,
)

# 返回值解析
print(f'res: {res}')
res_json = json.loads(res.model_dump_json())
print(f'res_json: {res_json}')
print(f'model: {res_json["model"]}')
print(f'usage: {res_json["usage"]}')
print(f'id: {res_json["id"]}')
print(f'data.embedding: {res_json["data"][0]["embedding"]}')
