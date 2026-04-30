from langchain_core.tools import tool


# 功能：@tool工具函数定义
# 1.定义工具
@tool
def get_weather(location):
    """模拟获得天气信息"""
    return f"{location}当前天气：23℃，晴，风力2级"


@tool
def get_user_name(user):
    """模拟获得用户名字"""
    return f'用户名字是:{user}'


# 2.封装工具
tools = [get_weather, get_user_name]

print('工具箱封装完成')
