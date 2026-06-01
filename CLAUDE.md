# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 概述

这是一个 Python 学习/参考项目，演示 Python 核心概念和 LangGraph 框架。每个文件都是独立的，包含 `if __name__ == '__main__'` 块，可直接运行。

## 运行代码

```bash
# Python 基础
python basic_008_file.py
python basic_005_oop.py
python basic_012.py
python UnitTest.py

# LangGraph
python lang_graph/01_hello_world/01_langgraph_hello_1.py
python lang_graph/02_graph/01_langgraph_graph.py
python lang_graph/03_state/01_state_schema.py
```

## 编码规范

- LangGraph 步骤编号统一：`1.定义State → 2.定义节点 → 3.构建图(3.1添加节点 3.2添加边) → 4.编译 → 5.运行`
- `add_messages` 应配合 `list[BaseMessage]` 和 `HumanMessage`/`AIMessage` 使用，而非纯字符串列表
- 节点函数参数必须带类型注解（`state: XxxState` 或 `state: dict`）
- 自定义 reducer 函数返回类型必须与 `Annotated` 中声明的类型一致

## 文件说明

### Python 基础（根目录）

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

### LangGraph 教程（lang_graph/）

- **01_hello_world/** - 入门：StateGraph 基本用法、无 LLM 工作流、接入 LLM
  - `01_langgraph_hello_1.py` - TypedDict 定义 State，两节点链式工作流
  - `02_langgraph_hello_2.py` - 使用 `dict` 作为 StateSchema，加减法工作流
  - `03_langgraph_hello_llm.py` - 接入 DeepSeek LLM，`add_messages` 消息追加
- **02_graph/** - 图构建：节点添加、边连接、StateGraph 完整流程
  - `01_langgraph_graph.py` - 输入/处理/输出三节点，覆盖式 State 更新
- **03_state/** - State 机制：Schema、Reducer 策略
  - `01_state_schema.py` - 输入/输出/整体 State 模式
  - `02_state_reducer_default.py` - 默认 Reducer：覆盖式更新
  - `03_state_reducer_add_messages.py` - `add_messages`：消息列表追加
  - `04_state_reducer_add_list.py` - `operator.add`：列表追加
  - `05_state_reducer_add_str.py` - `operator.add`：字符串连接
  - `06_state_reducer_add_int.py` - `operator.add`：整数累加
  - `07_state_reducer_mul.py` - `operator.mul`：整数相乘（含初值为0的坑）
  - `08_state_reducer_custom.py` - 自定义 Reducer：解决乘法初值问题
- **04_node/** - 节点高级用法（待补充）
- **05_edge/** - 边高级用法（待补充）
- **06_senior/** - 高级特性（待补充）
- **07_multi_agent/** - 多智能体（待补充）
