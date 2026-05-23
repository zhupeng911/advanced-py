import asyncio
import json
from typing import Any, Dict

from langchain.chat_models import init_chat_model
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mcp_adapters.client import MultiServerMCPClient

from lang_chain.config import OPENAI_API_KEY


# 1.加载mcp配置文件
def load_mcp_config(file_path: str = "mcp.json") -> Dict[str, Any]:
    with open(file_path, "r") as f:
        config = json.load(f)
        return config.get("mcpServers", {})


# 2.异步聊天客户端
async def chat() -> None:
    # 1.加载服务器
    servers_cfg = load_mcp_config()

    # 2.初始化MCP客户端
    mcp_client = MultiServerMCPClient(servers_cfg)
    tools = await mcp_client.get_tools()
    print(f'tools: {tools}, num: {len(tools)}')

    # 3.初始化LLM
    llm = init_chat_model(
        model="deepseek-chat",
        model_provider="deepseek",
        api_key=OPENAI_API_KEY,
        base_url="https://api.deepseek.com"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个 helpful的助手.需要使用提供的工具来完成用户请求"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    # 使用 tool-calling agent 调用 MCP tools
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors="解析用户请求失败，重新输入"
    )

    # 4.开始对话
    print("MCP Agent已启动，输入quit推出")
    while True:
        user_input = input(">>> 你 ").strip()
        if user_input.lower() == "quit":
            break
        try:
            result = await agent_executor.ainvoke({"input": user_input})
            print(f'AI: {result["output"]}')
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(chat())
