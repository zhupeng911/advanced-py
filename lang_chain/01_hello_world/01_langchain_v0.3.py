from langchain_openai import ChatOpenAI

from lang_chain.config import OPENAI_API_KEY

# 1.v0.3版本写法：通过ChatOpenAI创建语言模型实例
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

print("AI 对话 Demo（输入 quit 退出）")

while True:
    user_input = input("你: ").strip()
    if user_input.lower() in ("quit", "exit", "q"):
        print("再见!")
        break
    if not user_input:
        continue

    # 2.直接输出
    # response = llm.invoke(user_input)

    # 3.流式输出
    print("AI: ", end="")
    for chunk in llm.stream(user_input):
        print(chunk.content, end="", flush=True)
    print()
