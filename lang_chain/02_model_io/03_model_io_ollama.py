from langchain_ollama import ChatOllama

# 接入本地Ollama
llm = ChatOllama(
    base_url="http://127.0.0.1:11434",
    model="deepseek-r1:7b",
    reasoning=False
)
print(llm.invoke("简介python"))
