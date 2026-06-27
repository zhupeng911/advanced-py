import operator
import os
import sqlite3
from typing import TypedDict, Annotated

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.constants import END, START
from langgraph.graph import StateGraph


# LangGraph持久化-sqlite
# pip install langgraph-checkpoint-sqlite
# pip install langgraph-checkpoint-postgres

# 定义状态
class PersistenceState(TypedDict):
    messages: Annotated[list, operator.add]


# 定义节点
def step_one(state: PersistenceState) -> dict:
    print("Step one")
    return {
        "messages": ["执行了step one"]
    }


# 构建图
def create_graph():
    builder = StateGraph(PersistenceState)
    builder.add_node("step_one", step_one)
    builder.add_edge(START, "step_one")
    builder.add_edge("step_one", END)
    return builder


if __name__ == "__main__":
    # 编译图:使用sqlite存储
    db_path = os.path.join(os.path.dirname(__file__), "..", "persistence_v2.db")
    sqliteDB = SqliteSaver(conn=sqlite3.connect(database=db_path, check_same_thread=False))
    app = create_graph().compile(checkpointer=sqliteDB)

    # 运行图：配置线程id
    config = {"configurable": {"thread_id": "zhupeng"}}
    result = app.invoke({"messages": ["开始执行"], "step_count": 0}, config)
    print(f'结果: {result}')

    # 查看执行后的状态
    final_state = app.get_state(config)
    print(final_state)