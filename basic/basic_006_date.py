# 内置函数datetime date
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
