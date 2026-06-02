# ============================================================
# 异步编程：async / asyncio 典型案例
# ============================================================
# 异步编程：在 I/O 等待期间让出控制权，让事件循环去执行其他任务，从而提高并发效率
# 核心：async def 定义协程，await 挂起协程，asyncio.run() 运行事件循环

import asyncio
import time

import aiohttp


# ---------- 案例1：async/await 基本用法 + 串行 vs 并行 ----------
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


# ---------- 案例2：create_task 任务调度 ----------
# 场景：create_task 将协程包装为 Task 立即调度执行，可单独获取结果

async def demo_create_task():
    """create_task vs gather 的区别"""
    print("\n--- create_task 用法 ---")

    # 创建任务后立即开始执行，不需要 await
    task_a = asyncio.create_task(fetch_data("任务A", 3), name="task-A")
    task_b = asyncio.create_task(fetch_data("任务B", 1), name="task-C")

    # 可以在等待期间做其他事情
    print(f"task_a 名称: {task_a.get_name()}")
    print(f"task_a 是否完成: {task_a.done()}")

    # 需要结果时再 await
    result_a = await task_a
    result_b = await task_b
    print(f"结果: {result_a}, {result_b}")


# ---------- 案例3：超时控制 asyncio.wait_for ----------
# 场景：给异步操作设置超时时间，超时抛出 TimeoutError

async def slow_operation(name, seconds):
    """模拟一个可能超时的操作"""
    await asyncio.sleep(seconds)
    return f"{name} 完成"


async def demo_timeout():
    """wait_for：设置超时，超时抛出 TimeoutError"""
    print("\n--- 超时控制 ---")

    # 正常完成
    try:
        result = await asyncio.wait_for(slow_operation("快速任务", 1), timeout=3)
        print(f"完成: {result}")
    except asyncio.TimeoutError:
        print("快速任务超时！")

    # 超时取消
    try:
        result = await asyncio.wait_for(slow_operation("慢速任务", 5), timeout=2)
        print(f"完成: {result}")
    except asyncio.TimeoutError:
        print("慢速任务超时！")


# ---------- 案例4：异步上下文管理器 __aenter__ / __aexit__ ----------
# 场景：自定义异步 with 语句，自动管理资源（如数据库连接、HTTP 会话）

class AsyncTimer:
    """异步计时器：自动记录代码块执行时间"""

    async def __aenter__(self):
        self.start = time.perf_counter()
        print("[进入] 计时开始")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start
        print(f"[退出] 计时结束，耗时 {elapsed:.2f}s")
        if exc_type:
            print(f"[异常] {exc_type.__name__}: {exc_val}")
        return False  # 不吞异常


async def demo_async_context():
    print("\n--- 异步上下文管理器 ---")
    async with AsyncTimer():
        await asyncio.sleep(1)
        print("正在执行任务...")

    # 带异常的情况
    try:
        async with AsyncTimer():
            await asyncio.sleep(0.5)
            raise ValueError("模拟异常")
    except ValueError:
        print("捕获到异常，但计时器已正确退出")


# ---------- 案例5：异步迭代器 __aiter__ / __anext__ ----------
# 场景：逐个异步产出数据，适用于流式读取、分页请求

class AsyncRange:
    """异步迭代器：逐个产出数字，每次间隔 delay 秒"""

    def __init__(self, count, delay=0.5):
        self.count = count
        self.delay = delay
        self.current = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.current >= self.count:
            raise StopAsyncIteration
        await asyncio.sleep(self.delay)
        self.current += 1
        return self.current


async def demo_async_iterator():
    print("\n--- 异步迭代器 ---")
    async for num in AsyncRange(5, delay=0.3):
        print(f"产出: {num}")


# ---------- 案例6：生产者-消费者模式（asyncio.Queue） ----------
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
    print("\n--- 生产者-消费者模式 ---")
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


# ---------- 案例7：异步HTTP请求（aiohttp） ----------
# 场景：并发请求多个URL，收集响应结果

async def fetch_url(session, url: str) -> dict:
    """异步获取单个URL的响应"""
    print(f"[请求] {url}")
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
        status = resp.status
        text = await resp.text()
        print(f"[完成] {url} -> status={status}, length={len(text)}")
        return {"url": url, "status": status, "length": len(text)}


async def demo_async_http():
    """并发请求多个HTTP接口"""
    try:
        import aiohttp
    except ImportError:
        print("请先安装 aiohttp: pip install aiohttp")
        return

    print("\n--- 异步HTTP请求 ---")
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


# ---------- 案例8：TaskGroup（Python 3.11+） ----------
# 场景：更优雅的并发任务管理，自动捕获异常、自动取消

async def demo_task_group():
    """TaskGroup：结构化并发，任一任务异常则全部取消"""
    print("\n--- TaskGroup（Python 3.11+） ---")

    async def worker(name, seconds):
        print(f"[{name}] 开始")
        await asyncio.sleep(seconds)
        if name == "任务B":
            raise RuntimeError(f"{name} 出错了！")
        print(f"[{name}] 完成")
        return f"{name} 的结果"

    try:
        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(worker("任务A", 2))
            t2 = tg.create_task(worker("任务B", 1))
            t3 = tg.create_task(worker("任务C", 3))
    except ExceptionGroup as eg:
        for exc in eg.exceptions:
            print(f"捕获异常: {exc}")


# ---------- 入口 ----------
if __name__ == "__main__":
    # 案例1：基本 async/await + 串行 vs 并行
    asyncio.run(demo_async_basic())

    # 案例2：create_task 任务调度
    asyncio.run(demo_create_task())

    # 案例3：超时控制
    asyncio.run(demo_timeout())

    # 案例4：异步上下文管理器
    asyncio.run(demo_async_context())

    # 案例5：异步迭代器
    asyncio.run(demo_async_iterator())

    # 案例6：生产者-消费者模式
    asyncio.run(demo_producer_consumer())

    # 案例7：异步HTTP请求
    asyncio.run(demo_async_http())

    # 案例8：TaskGroup（Python 3.11+）
    asyncio.run(demo_task_group())
