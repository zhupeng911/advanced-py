import json

# 1.JSON 格式化
# json.dumps()参数说明
# 功能：用于将 Python 对象序列化为 JSON 字符串
# indent = 2 表示缩进为2个空格
# ensure_ascii=False 表示显示中文（不转义 Unicode）
# sort_keys=True  表示 按 key 排序
stu = {"name": "张三", "age": 30, "city": "北京"}
print(f'stu: {stu}')
print(f'stu.name: {stu["name"]}')
print(f'json.dumps(stu): {json.dumps(stu)}')
print(f'json.dumps(stu, indent=2, ensure_ascii=False): {json.dumps(stu, indent=2, ensure_ascii=False)}')

# 2.取值：字典嵌套列表（字典中包含列表，列表中包含字典）
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
print(f'PRODUCT_DATABASE: {PRODUCT_DATABASE}')
print(f'PRODUCT_DATABASE["无线耳机"]:{PRODUCT_DATABASE["无线耳机"]}')
print(f'PRODUCT_DATABASE["无线耳机"][0]:{PRODUCT_DATABASE["无线耳机"][0]}')
print(f'PRODUCT_DATABASE["无线耳机"][0]["id"]:{PRODUCT_DATABASE["无线耳机"][0]["id"]}')
print(f'PRODUCT_DATABASE["无线耳机"][0]["name"]:{PRODUCT_DATABASE["无线耳机"][0]["name"]}')

# 3. any()/all() + 生成器表达式：匹配到第一个就停止遍历，不会继续检查后面的类别
# 基础模式：any(item in container for item in items)：container中是否存在任意一个items中的元素
# 1. 检查字符串是否包含任意一个敏感词
text = "这个手机很好用"
banned = ["骗子", "假货", "垃圾"]
print(f'any(bad in text for bad in banned): {any(bad in text for bad in banned)}')  # False

# 2. 检查列表中是否有偶数
numbers = [1, 2, 3, 4]
print(f'any(n % 2 == 0 for n in numbers): {any(n % 2 == 0 for n in numbers)}')  # True

# 3. 检查用户是否有任意一个权限
allowed_roles = ["guest", "viewer"]
user_roles = ["admin", "user", "guest"]
print(f'any(role in allowed_roles for role in user_roles): {any(role in allowed_roles for role in user_roles)}')  # True


# ============================================================
# 4. 异步编程：async / asyncio 典型案例
# ============================================================

import asyncio
import time
import aiohttp


# ---------- 案例1：asyncio.run + async/await 基本用法 ----------
# 场景：模拟3个耗时任务串行 vs 并行执行，对比耗时

async def fetch_data(name: str, seconds: float) -> str:
    """模拟耗时IO操作（如网络请求、数据库查询）"""
    print(f"[{name}] 开始请求，预计耗时 {seconds}s")
    await asyncio.sleep(seconds)  # 非阻塞等待，交出控制权给事件循环
    print(f"[{name}] 请求完成")
    return f"{name}的数据"


async def demo_async_basic():
    """基本用法：串行 vs 并行"""
    print("\n--- 串行执行 ---")
    start = time.perf_counter()
    r1 = await fetch_data("任务A", 2)
    r2 = await fetch_data("任务B", 2)
    r3 = await fetch_data("任务C", 2)
    print(f"串行结果: {[r1, r2, r3]}")
    print(f"串行耗时: {time.perf_counter() - start:.2f}s")  # 约6s

    print("\n--- 并行执行 (asyncio.gather) ---")
    start = time.perf_counter()
    results = await asyncio.gather(
        fetch_data("任务A", 2),
        fetch_data("任务B", 2),
        fetch_data("任务C", 2),
    )
    print(f"并行结果: {list(results)}")
    print(f"并行耗时: {time.perf_counter() - start:.2f}s")  # 约2s


# ---------- 案例2：异步HTTP请求（aiohttp） ----------
# 场景：并发请求多个URL，收集响应结果

async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    """异步获取单个URL的响应"""
    print(f"[请求] {url}")
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
        status = resp.status
        text = await resp.text()
        print(f"[完成] {url} -> status={status}, length={len(text)}")
        return {"url": url, "status": status, "length": len(text)}


async def demo_async_http():
    """并发请求多个HTTP接口"""
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/ip",
        "https://httpbin.org/headers",
    ]

    start = time.perf_counter()
    async with aiohttp.ClientSession() as session:
        # 并发发起所有请求
        results = await asyncio.gather(
            *[fetch_url(session, url) for url in urls],
            return_exceptions=True  # 单个请求失败不影响其他请求
        )

    for r in results:
        if isinstance(r, Exception):
            print(f"请求失败: {r}")
        else:
            print(f"  {r['url']} -> status={r['status']}, body长度={r['length']}")
    print(f"总耗时: {time.perf_counter() - start:.2f}s")


# ---------- 案例3：生产者-消费者模式（asyncio.Queue） ----------
# 场景：生产者生成任务，消费者并发处理，适用于爬虫、消息处理等

async def producer(queue: asyncio.Queue, items: list[str]):
    """生产者：往队列中放入任务"""
    for item in items:
        await queue.put(item)
        print(f"[生产者] 放入: {item}")
    # 放入结束信号（None表示没有更多任务）
    for _ in range(3):  # 3个消费者，各发一个结束信号
        await queue.put(None)


async def consumer(queue: asyncio.Queue, cid: int):
    """消费者：从队列中取出任务并处理"""
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break  # 收到结束信号，退出
        print(f"[消费者{cid}] 处理: {item}")
        await asyncio.sleep(1)  # 模拟处理耗时
        print(f"[消费者{cid}] 完成: {item}")
        queue.task_done()


async def demo_producer_consumer():
    """生产者-消费者并发模型"""
    queue = asyncio.Queue(maxsize=5)
    items = [f"任务-{i}" for i in range(1, 8)]  # 7个任务

    start = time.perf_counter()
    # 启动1个生产者 + 3个消费者
    await asyncio.gather(
        producer(queue, items),
        consumer(queue, 1),
        consumer(queue, 2),
        consumer(queue, 3),
    )
    print(f"生产者-消费者总耗时: {time.perf_counter() - start:.2f}s")  # 约3s（7任务/3消费者≈3轮）


# ---------- 入口 ----------
if __name__ == "__main__":
    # 案例1：基本 async/await + asyncio.gather
    asyncio.run(demo_async_basic())

    # 案例2：异步HTTP请求
    asyncio.run(demo_async_http())

    # 案例3：生产者-消费者模式
    asyncio.run(demo_producer_consumer())
