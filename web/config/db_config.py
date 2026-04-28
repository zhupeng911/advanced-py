import os

from dotenv import load_dotenv

# - load_dotenv() 读取项目根目录的.env文件， 将其中的键值对设置为系统环境变量, 之后 os.getenv("KEY")就能读取到对应的值
load_dotenv()


class Config:
    # postgres
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME", "testdb_py")
    DB_USER = os.getenv("DB_USER", "zhupeng")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "zhupeng123")
    DB_MIN_CONN = int(os.getenv("DB_MIN_CONN", 2))
    DB_MAX_CONN = int(os.getenv("DB_MAX_CONN", 10))

    # Flask
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

    @staticmethod
    def get_database_url() -> str:
        return (
            f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}"
            f"@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
            f"?client_encoding=UTF8"
        )
