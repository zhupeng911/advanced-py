from psycopg_pool import ConnectionPool

from config.db_config import Config


class DatabasePool:
    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._pool = ConnectionPool(
                conninfo=Config.get_database_url(),
                min_size=Config.DB_MIN_CONN,
                max_size=Config.DB_MAX_CONN,
                timeout=30,
            )
        return cls._instance

    @property
    def pool(self):
        return self._pool

    def close_all(self):
        if self._pool:
            self._pool.close()


db_pool = DatabasePool()
