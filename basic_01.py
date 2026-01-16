if __name__ == '__main__':
    # 1.列表相关[java中list]
    students = ['alice', 'bob', 'red', 'cat']
    print(students)
    print(students[0:2])  # ['alice', 'bob']
    print(students[1:2])  # ['bob']
    print(students[0])
    print(students[1])
    print(students[2])

    for stu in students:
        print(stu, len(stu))

    for i in range(len(students)):
        print(students[i])

    # 常用方法
    students.append('cook')  # 在列表末尾添加新的对象
    students.insert(5, 'alice')  # 将对象插入列表指定下班
    students.remove('bob')  # 移除列表中某个值的第一个匹配项
    print(students.count('alice'))  # 出现次数
    print(students.index('alice'))  # 首次出现下标,如果没有会报错
    print('jack' in students)

    scores = [100, 78, 78, 67, 90]
    print(len(scores))
    print(max(scores))
    print(min(scores))
    print(sum(scores))

    students.reverse()  # 反向列表中元素
    students.sort(key=None, reverse=True)  # 对原列表进行排序

    # 2.集合相关[java中set]
    set1 = {1, 2, 3, 3, 4}  # 不可重复
    set1.add(8)
    set1.update({4, 99})
    set1.remove(1)
    set1.discard(2)
    print(set1)
    print(len(set1))
    print(set1.pop())
    print(1 in set1)

    for item in set1:
        print(item)

    set2 = set("abcde")
    set3 = set("defgh")
    print(set2 - set3)  # 集合a中包含而集合b中不包含的元素
    print(set2 | set3)  # 集合a或b中包含的所有元素
    print(set2 & set3)  # 集合a和b中都包含了的元素
    print(set2 ^ set3)  # 不同时包含于a和b的元素

    # 3.字典相关[java中map]
    stuInfo = {"name": "zhangsan", "age": 23}
    print(stuInfo)
    print(stuInfo["name"])
    print(stuInfo["age"])
    print(len(stuInfo))
    print(stuInfo.pop("name"))

    for key in stuInfo.keys():
        print(key, stuInfo[key])

    for key, value in stuInfo.items():
        print(key, value)

    del stuInfo

    # 4.if相关
    num = int(input("input a number: "))
    if num % 2 == 0:
        if num % 3 == 0:
            print("你输入的数字可以整除 2 和 3")
        else:
            print("你输入的数字可以整除 2，但不能整除 3")
    else:
        if num % 3 == 0:
            print("你输入的数字可以整除 3，但不能整除 2")
        else:
            print("你输入的数字不能整除 2 和 3")

    age = int(input("请输入你家狗狗的年龄: "))
    if age <= 0:
        print("你是在逗我吧!")
    elif age == 1:
        print("相当于 14 岁的人。")
    elif age == 2:
        print("相当于 22 岁的人。")
    elif age > 2:
        human = 22 + (age - 2) * 5
        print("对应人类年龄: ", human)

    # 5.循环
    count = 1
    sum = 0
    while count <= 100:
        sum += count
        count += 1
    else:
        print(count, "大于100，结束")
    print(sum)

    for n in range(2, 10):
        for x in range(2, n):
            if n % x == 0:
                print(n, 'equals', x, '*', n // x)
                break
        else:  # 与if语句相比，循环的else子句更像try的else子句
            print(n, 'is a prime number')

    for x in range(5, 10):
        if x % 2 == 0:
            print("找到偶数: ", x)
            continue
        print(x)

    # pass 语句:pass 语句不执行任何操作
    # match语句