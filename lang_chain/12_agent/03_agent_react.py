from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

from lang_chain.config import OPENAI_API_KEY

# 功能：详细追踪Agent ReAct循环过程

# 1.模拟产品数据库
PRODUCT_DATABASE = {
    "无线耳机": [
        {"id": "1", "name": "AirPods", "popularity": "99", "price": 299},
        {"id": "2", "name": "Bose QuietComfort", "popularity": "95", "price": 249},
        {"id": "3", "name": "Samsung Galaxy Buds", "popularity": "90", "price": 199},
        {"id": "4", "name": "Sony WH-1000XM4", "popularity": "85", "price": 399},
        {"id": "5", "name": "Jabra Elite 7t", "popularity": "80", "price": 299},
    ],
    "游戏鼠标": [
        {"id": "6", "name": "罗技", "popularity": "99", "price": 399},
        {"id": "7", "name": "三星 Galaxy Watch 4", "popularity": "95", "price": 299},
        {"id": "8", "name": "苹果 Watch Series 7", "popularity": "90", "price": 399},
    ],
    "笔记本电脑": [
        {"id": "9", "name": "Apple MacBook Air", "popularity": "99", "price": 899},
        {"id": "10", "name": "Dell XPS 13", "popularity": "95", "price": 799},
        {"id": "11", "name": "HP Spectre x360", "popularity": "90", "price": 699},
        {"id": "12", "name": "Lenovo ThinkPad X1 Carbon", "popularity": "85", "price": 599},
        {"id": "13", "name": "Fitbit Versa 3", "popularity": "90", "price": 199},
        {"id": "14", "name": "Garmin Venu 2", "popularity": "85", "price": 399},
        {"id": "15", "name": "Moto 360 Smartwatch", "popularity": "80", "price": 299},
    ]
}

# 2.模拟库存数据库
INVENTORY_DATABASE = {
    "1": {"stock": 10, "location": "A1"},
    "2": {"stock": 5, "location": "A2"},
    "3": {"stock": 20, "location": "B1"},
    "4": {"stock": 15, "location": "B2"},
    "5": {"stock": 10, "location": "C1"},
    "6": {"stock": 12, "location": "C2"},
    "7": {"stock": 8, "location": "D1"},
    "8": {"stock": 18, "location": "D2"},
    "9": {"stock": 14, "location": "E1"},
    "10": {"stock": 22, "location": "E2"},
    "11": {"stock": 10, "location": "F1"},
    "12": {"stock": 12, "location": "F2"},
    "13": {"stock": 14, "location": "G1"},
    "14": {"stock": 22, "location": "G2"},
}


# 3.工具1:搜索产品
@tool
def search_products(prod_name: str) -> str | None:
    """搜索产品并返回接受程度排序的结果"""  # 不要忘记注释
    print(f'[工具调用,search_products({prod_name})]')

    # 定义关键词映射，类似模糊查找
    keyword_mapping = {
        "无线耳机": ["无线耳机", "有线耳机", "蓝牙耳机"],
        "智能手表": ["智能手表", "智能手环", "智能腕表"],
        "智能手环": ["智能手环", "智能手表", "智能腕环"],
    }

    # 匹配类别
    matched_category = None
    for category, keywords in keyword_mapping.items():
        # 遍历所有类别及其关键词
        if any(keyword in prod_name for keyword in keywords):
            # 如果商品名称中包含任意一个关键词，就返回这个类别
            matched_category = category
            break
    return matched_category


# 4.工具2:搜索库存
@tool
def search_inventory(prod_id: str) -> str:
    """搜索库存并返回结果"""  # 不要忘记注释
    print(f'[工具调用,search_inventory({prod_id})]')
    if prod_id in INVENTORY_DATABASE:
        stock_info = INVENTORY_DATABASE[prod_id]
        status = "有库存" if stock_info["stock"] > 0 else "无库存"
        return f"产品{prod_id}: {status}, 库存数量: {stock_info['stock']}, 位置: {stock_info['location']}"
    else:
        return "产品不存在:{prod_id}"


# 5.定义大模型与agent
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
agent = create_agent(
    model=llm,
    tools=[search_products, search_inventory],
    system_prompt="""
        你是一个 helpful的助手.遵循ReAct模式
        1. 理解用户输入
        2. 选择合适的工具执行操作
        3. 基于工具返回的结果进行下一步推理
        4. 重复上述过程，直到得到最终结果
    """,
    response_format=None,
)

# 测试案例1：无线耳机搜索
result1 = agent.invoke({
    "messages": [
        {"role": "user", "content": "查找当前最受欢迎的无线耳机并检查是否还有库存"}
    ]
})


# 详细追踪ReAct循环过程
def tract_react_loop(messages):
    print("ReAct循环步骤分析")
    step = 1
    for i, msg in enumerate(messages):
        msg_type = msg.__class__.__name__
        if msg_type == "AIMessage" and hasattr(msg, "tool_calls") and msg.tool_calls:
            print(f'步骤{step}: Reason + Act')
            for tool_call in msg.tool_calls:
                print(f'工具调用：{tool_call["name"]}')
                step += 1
        elif msg_type == "ToolMessage":
            print(f'观察结果：{msg.content[:80]}...')
        elif msg_type == "AIMessage" and not (hasattr(msg, "tool_calls") and msg.tool_calls):
            print(f'最终结果：{msg.content}')


tract_react_loop(result1["messages"])
