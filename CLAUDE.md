# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 概述

这是一个 Python 学习/参考项目，演示 Python 核心概念。每个文件都是独立的，包含 `if __name__ == '__main__'` 块，可直接运行。

## 运行代码

```bash
python basic_01.py
python basic_02.py
python basic_04.py
python UnitTest.py
```

注意：`basic_02.py` 需要本地服务器 `127.0.0.1:8080` 和 `configs.json` 文件。

## 文件说明

- **basic_01.py** - Python 数据结构：列表、集合、字典、条件语句、循环
- **basic_02.py** - 超级管理员 API 客户端：登录、节点绑定、数据库/机构创建
- **basic_03.py** - 类定义、构造函数、私有成员、默认参数
- **UnitTest.py** - 多个示例：计算器、文件读写、OOP（银行账户）、装饰器（`@timer`、`@retry`）、生成器（斐波那契、文件行）
