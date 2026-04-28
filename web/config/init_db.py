from config.db_pool import db_pool

# 数据库初始化
def init_db():
    with db_pool.pool.connection() as conn:
        cursor = conn.cursor()

        # 创建 users 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 创建索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
        """)

        conn.commit()
        print("数据库初始化完成")


def drop_database():
    """删除数据库表（慎用）"""
    with db_pool.pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS users CASCADE")
        conn.commit()
        print("数据库表已删除")


if __name__ == '__main__':
    init_db()
