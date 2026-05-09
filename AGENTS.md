# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## 概述

这是一个 Python 学习/参考项目，演示 Python 核心概念。每个文件都是独立的，包含 `if __name__ == '__main__'` 块，可直接运行。

## 运行代码

```bash
python basic_008_file.py
python basic_005_oop.py
python basic_012.py
python UnitTest.py
```

## 文件说明

- **basic_001_data_type.py** - Python 数据结构：列表、集合、字典、条件语句、循环
- **basic_002_container.py** - 超级管理员 API 客户端：登录、节点绑定、数据库/机构创建
- **basic_003_flow.py** - 类定义、构造函数、私有成员、默认参数
- **basic_004_def.py** - 函数定义、参数类型注解、返回值
- **basic_005_oop.py** - 面向对象编程：类、继承、多态、特殊方法
- **basic_006_exp.py** - 异常处理：try/except、自定义异常、finally
- **basic_007_date.py** - 日期时间操作：datetime、timestamp、格式化
- **basic_008_file.py** - 文件/文件夹操作 + JSON/YAML/CSV 文件读写，包含 Student 类映射 json_data
- **basic_012.py** - 迭代器、生成器、上下文管理器
- **UnitTest.py** - 多个示例：计算器、文件读写、OOP（银行账户）、装饰器（`@timer`、`@retry`）、生成器（斐波那契、文件行）
