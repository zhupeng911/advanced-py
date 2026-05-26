import json

# 1.JSON 格式化
# json.dumps()参数说明
# 功能：用于将 Python 对象序列化为 JSON 字符串
# indent = 2 表示缩进为2个空格
# ensure_ascii=False 表示显示中文（不转义 Unicode）
# sort_keys=True  表示 按 key 排序
stu = {"name": "张三", "age": 30, "city": "北京"}
print(f'stu: {stu}')
print(f'stu.name: {stu["name"]}')
print(f'json.dumps(stu): {json.dumps(stu)}')
print(f'json.dumps(stu, indent=2, ensure_ascii=False): {json.dumps(stu, indent=2, ensure_ascii=False)}')

# 2.取值：字典嵌套列表（字典中包含列表，列表中包含字典）
PRODUCT_DATABASE = {
    "无线耳机": [
        {"id": "1", "name": "AirPods", "popularity": "99", "price": 299},
        {"id": "2", "name": "Bose QuietComfort", "popularity": "95", "price": 249},
        {"id": "3", "name": "Samsung Galaxy Buds", "popularity": "90", "price": 199},
        {"id": "4", "name": "Sony WH-1000XM4", "popularity": "85", "price": 399},
        {"id": "5", "name": "Jabra Elite 7t", "popularity": "80", "price": 299},
    ],
    "游戏鼠标": [
        {"id": "6", "name": "罗技", "popularity": "99", "price": 399},
        {"id": "7", "name": "三星 Galaxy Watch 4", "popularity": "95", "price": 299},
        {"id": "8", "name": "苹果 Watch Series 7", "popularity": "90", "price": 399},
    ],
    "笔记本电脑": [
        {"id": "9", "name": "Apple MacBook Air", "popularity": "99", "price": 899},
        {"id": "10", "name": "Dell XPS 13", "popularity": "95", "price": 799},
        {"id": "11", "name": "HP Spectre x360", "popularity": "90", "price": 699},
        {"id": "12", "name": "Lenovo ThinkPad X1 Carbon", "popularity": "85", "price": 599},
        {"id": "13", "name": "Fitbit Versa 3", "popularity": "90", "price": 199},
        {"id": "14", "name": "Garmin Venu 2", "popularity": "85", "price": 399},
        {"id": "15", "name": "Moto 360 Smartwatch", "popularity": "80", "price": 299},
    ]
}
print(f'PRODUCT_DATABASE: {PRODUCT_DATABASE}')
print(f'PRODUCT_DATABASE["无线耳机"]:{PRODUCT_DATABASE["无线耳机"]}')
print(f'PRODUCT_DATABASE["无线耳机"][0]:{PRODUCT_DATABASE["无线耳机"][0]}')
print(f'PRODUCT_DATABASE["无线耳机"][0]["id"]:{PRODUCT_DATABASE["无线耳机"][0]["id"]}')
print(f'PRODUCT_DATABASE["无线耳机"][0]["name"]:{PRODUCT_DATABASE["无线耳机"][0]["name"]}')

# 3. any()/all() + 生成器表达式：匹配到第一个就停止遍历，不会继续检查后面的类别
# 基础模式：any(item in container for item in items)：container中是否存在任意一个items中的元素
# 1. 检查字符串是否包含任意一个敏感词
text = "这个手机很好用"
banned = ["骗子", "假货", "垃圾"]
print(f'any(bad in text for bad in banned): {any(bad in text for bad in banned)}')  # False

# 2. 检查列表中是否有偶数
numbers = [1, 2, 3, 4]
print(f'any(n % 2 == 0 for n in numbers): {any(n % 2 == 0 for n in numbers)}')  # True

# 3. 检查用户是否有任意一个权限
allowed_roles = ["guest", "viewer"]
user_roles = ["admin", "user", "guest"]
print(f'any(role in allowed_roles for role in user_roles): {any(role in allowed_roles for role in user_roles)}')  # True
