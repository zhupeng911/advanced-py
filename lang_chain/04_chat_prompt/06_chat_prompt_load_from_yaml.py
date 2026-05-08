from langchain_core.prompts import load_prompt

# 从外部yaml文件加载Prompt
prompt = load_prompt("prompt/prompt.yaml", encoding="utf-8")
print(prompt.format(name="张三", story="一次冒险"))
