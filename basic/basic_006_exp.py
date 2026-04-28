# 异常处理 - 常见技术点
import json
import os
import random
import sys
import traceback
from contextlib import suppress


# ============================================================
# 1. 基本结构: try / except / else / finally
# ============================================================
def basic_structure():
    """try-except-else-finally 完整结构"""
    try:
        x = 1 / 0
    except ZeroDivisionError:
        print("[1] 除零错误")
    except Exception as e:
        print(f"[1] 其他错误: {e}")
    else:
        # else 只在 try 中没有异常时执行
        print("[1] 没有错误")
    finally:
        # finally 无论如何都会执行（即使有 return / 异常未捕获）
        print("[1] 执行完毕")


# ============================================================
# 2. 捕获多个异常类型
# ============================================================
def catch_multiple_types():
    """一个 except 捕获多种异常"""
    errors = [ZeroDivisionError, ValueError, TypeError]
    for err in errors:
        try:
            if err == ZeroDivisionError:
                print("除零错误 1/0")
            elif err == ValueError:
                print("值错误 int('abc')")
            elif err == TypeError:
                print("类型错误 '2' + 2")
        except (ZeroDivisionError, ValueError) as e:  # 用元组捕获多种异常，共享同一处理逻辑
            print(f"[2] 数据错误 ({type(e).__name__}): {e}")
        except TypeError as e:
            print(f"[2] 类型错误 ({type(e).__name__}): {e}")


# ============================================================
# 3. 异常链: raise ... from ...
# ============================================================
def exception_chaining():
    """用 from 保留原始异常的追溯信息"""
    try:
        try:
            data = json.loads('{"key": invalid}')  # noqa
        except NameError as e:
            # from None: 抑制原始异常（不想暴露内部细节）
            raise ValueError("配置解析失败") from None
    except ValueError as e:
        print(f"[3] 捕获: {e}")
        print(f"[3] 原因: {e.__cause__}")  # None，因为用了 from None

    try:
        try:
            with open("nonexistent.txt") as f:
                f.read()
        except FileNotFoundError as e:
            # from e: 显式链接，保留原始异常
            raise RuntimeError("初始化失败: 配置文件缺失") from e
    except RuntimeError as e:
        print(f"[3] 捕获: {e}")
        print(f"[3] 原因: {e.__cause__}")  # FileNotFoundError 实例


# ============================================================
# 4. 自定义异常
# ============================================================
class AppError(Exception):
    """应用基础异常"""
    pass


class ValidationError(AppError):
    """校验异常，附带字段信息"""

    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")


class NotFoundError(AppError):
    """资源未找到"""

    def __init__(self, resource, resource_id):
        self.resource = resource
        self.resource_id = resource_id
        super().__init__(f"{resource} [{resource_id}] 未找到")


def custom_exception():
    """自定义异常层级，按基类统一捕获"""
    try:
        raise ValidationError("email", "格式不合法")
    except ValidationError as e:
        print(f"[4] 校验失败 - 字段: {e.field}, 原因: {e.message}")

    try:
        raise NotFoundError("用户", 42)
    except AppError as e:
        # 用基类 AppError 统一捕获所有子类异常
        print(f"[4] 应用错误 ({type(e).__name__}): {e}")

# 运行方法
custom_exception()

# ============================================================
# 5. 上下文管理器与异常: suppress
# ============================================================
def contextlib_suppress():
    """contextlib.suppress: 静默忽略指定异常（替代 try/except pass）"""

    # 写法1: 传统的 try/except pass
    try:
        os.remove("nonexistent.tmp")  # noqa
    except FileNotFoundError:
        pass

    # 写法2: suppress 更简洁
    with suppress(FileNotFoundError):
        os.remove("nonexistent.tmp")  # noqa

    print("[6] suppress: 文件不存在时静默忽略，不会报错")


# ============================================================
# 6. assert 断言
# ============================================================
def assertion():
    """assert 用于开发期调试检查，生产环境可用 -O 禁用"""

    def calculate_average(numbers):
        assert len(numbers) > 0, "列表不能为空"  # 条件为 False 时抛 AssertionError
        return sum(numbers) / len(numbers)

    print(f"[7] 平均值: {calculate_average([1, 2, 3])}")

    try:
        calculate_average([])
    except AssertionError as e:
        print(f"[7] 断言失败: {e}")

    # 注意: assert 可被 python -O 禁用，不要用 assert 做业务校验
    # 业务校验应使用 if + raise


# ============================================================
# 7. 获取异常详细信息: traceback / sys.exc_info
# ============================================================
def exception_details():
    """获取完整的异常追踪信息"""
    try:
        result = 1 / 0
    except ZeroDivisionError:
        # 方式1: traceback.format_exc() 获取格式化堆栈
        tb_str = traceback.format_exc()
        print(f"[8a] traceback:\n{tb_str}")

        # 方式2: sys.exc_info() 获取异常三元组
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(f"[8b] 类型: {exc_type}, 值: {exc_value}")

        # 方式3: 异常对象的 args 和 __traceback__
        print(f"[8c] args: {exc_value.args}")
        print(f"[8c] traceback 对象: {exc_value.__traceback__}")


# ============================================================
# 8. 异常中的循环重试模式
# ============================================================
def retry_pattern():
    """常见重试模式: 捕获异常后重试，最多 N 次"""

    def unstable_operation():
        """模拟不稳定操作（70% 概率失败）"""
        if random.random() < 0.7:
            raise ConnectionError("连接超时")
        return "成功"

    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            result = unstable_operation()
            print(f"[9] 第 {attempt} 次尝试: {result}")
            break
        except ConnectionError as e:
            print(f"[9] 第 {attempt} 次失败: {e}")
            if attempt == max_retries:
                print(f"[9] 已达最大重试次数 {max_retries}，放弃（演示用，不向上传播）")
                # raise  # 生产环境中应 raise，这里演示用所以注释掉


# ============================================================
# 9. 万能异常捕获的最佳实践
# ============================================================
def best_practices():
    """异常处理的常见最佳实践"""

    # 反模式: 裸 except（会捕获 KeyboardInterrupt / SystemExit）
    # except:  # 不要这样写！
    # except BaseException:  # 也不要这样写！

    # 正确: 至少用 Exception
    # except Exception as e:  # 最低限度

    # 最好: 捕获具体类型
    value = "abc"
    try:
        number = int(value)
    except ValueError:
        print(f"[10] '{value}' 不是有效数字，使用默认值 0")
        number = 0
    print(f"[10] 结果: {number}")

    # 反模式: 吞掉异常（让调试变得困难）
    # try:
    #     risky_operation()
    # except Exception:
    #     pass  # 不要静默吞掉异常！

    # 正确: 至少记录日志
    # except Exception as e:
    #     logging.exception("操作失败")
