# 技术点：四大容器
# 列表List: 有序、可变（可以增删改）、允许重复
#    students = ['alice', 'bob', 'red', 'cat']
#
# 元组Tuple: 不可变的列表,有序、不可变、允许重复
#     names = ("Alice", "Bob")
#
# 集合Set：去重神器,无序、可变、不允许重复
#     tags = {"python", "java", "python", "c++"}
#
# 字典Dictionary：键值对,键（Key）必须唯一且不可变，值（Value）可以任意
#     user = {"name": "Gemini", "age": 1, "city": "Mountain View"}

def basic_container():
    # 1.列表List，有序、可变（可以增删改）、允许重复
    students = ['alice', 'bob', 'red', 'cat']

    # 增
    students.append('alice')
    students.insert(5, 'alice')
    # 删
    del students[0]
    students.remove('bob')
    # 改
    students[0] = 'alice22'
    # 查
    print(students)
    print(students[1:2])  # 使用切片获取子列表
    print(students[:2])  # 返回前两个元素
    print(students[1:])  # 返回从第二个元素开始到末尾的所有元素
    print(students[:])  # 返回所有元素
    print(students[0])
    print(students[-1])  # 返回最后一个元素
    print(len(students))  # 返回列表长度
    print('alice' in students)
    print('alice' not in students)
    print(students.count('alice'))  # 出现次数
    print(students.index('alice'))  # 首次出现下标,如果没有会报错

    # 遍历
    for stu in students:
        print(stu)
    for i in range(len(students)):
        print(students[i])

    # 拼接
    teachers = ['zhangsan', 'lisi', 'wangwu']
    all = students + teachers
    print(all)

    # zip,在多个列表中循环
    # zip() 函数将多个列表打包成元组序列
    # for stu, tea in zip(...) 会同时遍历两个列表
    # 按顺序配对：alice-zhangsan，bob-lisi，red-wangwu，cat 被丢弃（列表长度不同）
    for stu, tea in zip(students, teachers):
        print(stu, tea)

    # 应用场景1:合并两个列表为字典
    # {'name': 'Alice', 'age': 25, 'city': 'Beijing'}
    keys = ['name', 'age', 'city']
    values = ['Alice', 25, 'Beijing']
    dict(zip(keys, values))

    # 应用场景2：批量更新数据库
    users = ['user1', 'user2', 'user3']
    scores = [95, 88, 92]
    for user, score in zip(users, scores):
        print(user, score)
        # db.execute("UPDATE scores SET v=? WHERE name=?", (score, user))

    # 排序
    scores = [100, 78, 78, 67, 90]
    scores.sort()
    print(scores)
    print(len(scores))
    print(max(scores))
    print(min(scores))
    print(sum(scores))
    scores.reverse()  # 反向列表中元素
    scores.sort(key=None, reverse=True)  # 对原列表进行排序

    # 2.元组Tuple，不可变的列表、有序、允许重复
    tuple1 = (1, 2, 3, 4, 5)
    # 不支持增、删、改
    # 查
    print(tuple1)
    print(tuple1[0:2])
    print(tuple1[1:3])
    print(tuple1[2:4])
    print(tuple1[:2])

    # 类型转换
    names = ['alice', 'bob', 'red', 'cat']
    tuple2 = tuple(names)
    print(tuple2)
    list2 = list(tuple2)
    print(list2)

    # 3.集合Set，去重神器,无序、可变、不允许重复
    set1 = {1, 2, 3, 3, 4, 1}  # 使用花括号
    # 增
    set1.add(6)
    # 删
    set1.remove(1)  # 如果值不存在，remove() 会引发 key error。
    set1.discard(2)  # 移除元素(安全，缺失时不报错)
    # 改
    set1.update({4, 5})
    set1.update([4, 5])
    # 查
    print(set1)
    print(len(set1))
    print(set1.pop())
    print(1 in set1)
    # 遍历
    for item in set1:
        print(item)

    # 集合运算
    set2 = set("abcde")
    set3 = set("defgh")
    print(set2 - set3)  # 集合a中包含而集合b中不包含的元素
    print(set2 | set3)  # 集合a或b中包含的所有元素
    print(set2 & set3)  # 集合a和b中都包含了的元素
    print(set2 ^ set3)  # 不同时包含于a和b的元素

    # 4.字典map：键值对,键（Key）必须唯一且不可变，值（Value）可以任意
    stuInfo = {
        "name": "zhangsan",
        "age": 23
    }
    # 增
    stuInfo.setdefault("city", "上海")
    # 删
    del stuInfo["name"]
    # stuInfo.pop("name")
    # del stuInfo
    # 改
    stuInfo["age"] = 24
    # 查
    print(stuInfo)
    # print(stuInfo["name"])
    print(len(stuInfo))
    print(stuInfo.keys())
    print(stuInfo.values())
    print(stuInfo.items())
    print("name" in stuInfo.keys())  # 判断键是否存在'
    print("zhupeng" in stuInfo.values())  # 判断值是否存在

    # 遍历
    for key in stuInfo.keys():
        print(key, stuInfo[key])

    for key, value in stuInfo.items():
        print(key, value)

    # 类型转换
    str = '123123'
    list_str = list(str)
    set_str = set(str)
    print(list_str)
    print(set_str)


from datetime import datetime, timedelta, date


def basic_date_format():
    # 1.标准datetime 年 月 日 时 分 秒
    now = datetime.now()
    print("now:", now)
    print("年:", now.year, "月:", now.month, "日:", now.day)
    print("时:", now.hour, "分:", now.minute, "秒:", now.second)

    one_year_later = now + timedelta(days=365)
    print("one_year_later:", one_year_later)
    one_day_later = now + timedelta(days=1)
    print("one_day_later:", one_day_later)
    one_hour_before = one_day_later - timedelta(hours=1)
    print("one_hour_before:", one_hour_before)

    # 字符串->时间
    date_time_str = "2023-04-01 12:00:00"
    date_time_format = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
    print("date_format:", date_time_format)

    date_one_year_later = date_time_format + timedelta(days=365)
    print("date_one_year_later:", date_one_year_later)

    # 2.标准date
    today = date.today()
    today2 = datetime.now().date()
    print("today:", today)
    print("today2:", today2)
    print("年:", today.year, "月:", today.month, "日:", today.day)
    one_day_later = today + timedelta(days=1)
    print("one_day_later:", one_day_later)
    one_day_before = today - timedelta(days=1)
    print("one_day_before:", one_day_before)

    date_str = "2023-04-01"
    date_format = date.strptime(date_str, "%Y-%m-%d")
    print("date_format:", date_format)


if __name__ == '__main__':
    basic_container()
    basic_date_format()
