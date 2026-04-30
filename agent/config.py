import os
import warnings

# 全局抑制 Pydantic V1 兼容性警告（Python 3.14+）
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality", category=UserWarning)

from dotenv import load_dotenv

# 1. 加载.env文件
load_dotenv()

# 2. 解决 UUID v7 警告
try:
    from langsmith import uuid7
    import uuid

    uuid.uuid4 = uuid7  # 全局替换
except ImportError:
    pass  # 如果没装 langsmith，省略


# 3. 解决TensorFlow & Numpy 兼容性告警
def silence_framework_warnings():
    import os
    import logging
    import warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    warnings.filterwarnings('ignore')
    logging.getLogger('tensorflow').setLevel(logging.ERROR)


silence_framework_warnings()

# 4. 获取API_KEYS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
AMAP_MAPS_API_KEY = os.getenv("AMAP_MAPS_API_KEY")
CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("× 请在.env中设置OPENAI_API_KEY")
if not LANGCHAIN_API_KEY:
    raise ValueError("× 请在.env中设置LANGCHAIN_API_KEY")
if not AMAP_MAPS_API_KEY:
    raise ValueError("× 请在.env中设置AMAP_MAPS_API_KEY")
if not CHATGPT_API_KEY:
    raise ValueError("× 请在.env中设置CHATGPT_API_KEY")
