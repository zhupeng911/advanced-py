# 构建SQL Agent
import os
import sqlite3

from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI

from agent.config import OPENAI_API_KEY

# 1. 配置LLM基本信息
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)

# 2.创建一个临时的数据库--用于演示
db_file = "test_sql.db"
if os.path.exists(db_file):
    os.remove(db_file)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute("CREATE TABLE users (id INT,name TEXT,age INT);")
cursor.execute("INSERT INTO users (id,name,age) VALUES (1,'Alice',30);")
cursor.execute("INSERT INTO users (id,name,age) VALUES (2,'Bob',25);")
conn.commit()
conn.close()

db_uri = f'sqlite:///{db_file}'
db = SQLDatabase.from_uri(db_uri)

# 3.创建sqlAgent -- 一键完成，无需定义tools，仅告诉它使用openai-tools,即Tool Calling(工具调用)模式
sql_agent = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="openai-tools",
    verbose=True
)

# 4. 运行sqlAgent
# response = sql_agent.invoke({"input": "SELECT * FROM users;"})
response = sql_agent.invoke({"input": "Alice 年龄多大"})
print(response)

# 5.关闭连接池
db._engine.dispose()
if os.path.exists(db_file):
    os.remove(db_file)
