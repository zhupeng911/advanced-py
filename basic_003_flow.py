# 技术点：基本逻辑控制语句
def basic_logic_control():
    # if
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

    # 三目运算符
    age = 10
    print('未成年' if age < 18 else '成年')

    # switch
    response_code = 201
    match response_code:
        case 200:
            print("OK")
        case 201:
            print("Created")
        case 300:
            print("Multiple Choices")
        case 307:
            print("Temporary Redirect")
        case 404:
            print("404 Not Found")
        case 500:
            print("Internal Server Error")
        case 502:
            print("502 Bad Gateway")

    response_code = 502
    match response_code:
        case 200 | 201:
            print("OK")
        case 300 | 307:
            print("Redirect")
        case 400 | 401:
            print("Bad Request")
        case 500 | 502:
            print("Internal Server Error")
        case _:
            print("Unknown")

    # while 循环
    count = 1
    sum = 0
    while count <= 100:
        sum += count
        count += 1
    else:
        print(count, "大于100，结束")
    print(sum)

    # for 循环
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
    else:
        print("循环正常结束")

    # pass 语句:pass 语句不执行任何操作
    # match语句


if __name__ == '__main__':
    basic_logic_control()
