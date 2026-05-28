from langchain.chat_models import init_chat_model

from lang_chain.config import OPENAI_API_KEY

# init_chat_model创建一个语言模型， v1.0写法，常用
# PS：api_key、base_url、temperature 都不在显式参数中，它们被 **kwargs 收集，然后透传给底层模型构造函数，init_chat_model只是个工厂函数，自身不关心这些参数，全部原样转交。
# 流程：
# init_chat_model(model="deepseek-chat", model_provider="deepseek", api_key=..., base_url=..., temperature=0.7)
#       ↓
# 提取剩余参数：**kwargs = {"api_key": ..., "base_url": ..., "temperature": 0.7}
#       ↓
# 依据 model_provider="deepseek" 映射并加载对应的类：ChatDeepSeek
#       ↓
# 实例化目标类：ChatDeepSeek(model="deepseek-chat", **kwargs)
# ChatDeepSeek 之所以能够准确接收并校验这些参数，依赖于底层的 Pydantic 模型和如下的类继承关系：
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com",
    temperature=0.7  # 温度参数，控制生成文本的随机性，范围通常在0到1之间
)

# 调用语言模型
response = llm.invoke("你是谁")
print("response.content", response.content)
