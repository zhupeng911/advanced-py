"""
- 文件操作，包括：
- 文件夹/文件常用操作
- JSON 文件读写操作
- YAML 文件读写操作
- CSV 文件读写操作
"""
import json
import shutil
from pathlib import Path

import yaml


# 1.文件夹与文件
def demo_file():
    # 文件夹
    folder = Path("docs")
    print(f'当前工作目录: {Path.cwd()}')
    print(f"文件夹路径: {folder}")
    print(f"文件夹存在吗 {folder.exists()}")
    print(f"文件夹绝对路径: {folder.resolve()}")
    print(f"文件夹是否是绝对路径? {folder.is_absolute()}")
    print(f"文件夹是否是目录? {folder.is_dir()}")
    print(f"文件夹是否是文件? {folder.is_file()}")
    print(f"文件夹是否是符号链接? {folder.is_symlink()}")
    print(f'文件夹大小: {folder.stat().st_size} 字节')

    # 1. 创建文件夹
    folder.mkdir(exist_ok=True)
    print(f"创建文件夹: {folder}")

    # 2. 重命名文件夹
    renamed_folder = folder.rename("docs")
    print(f"重命名文件夹: {renamed_folder}")

    # 3. 遍历文件夹
    if folder.exists() and folder.is_dir():
        for file in folder.glob("*"):  # 仅限当前目录
            print(file)
        for file in folder.glob("*"):  # 递归列出所有子目录和文件
            print(file)
        for item in folder.iterdir():  # 当你需要查看所有内容（文件+文件夹）且不关心过滤规则时。
            type_str = "文件夹" if item.is_dir() else "文件"
            print(f"[{type_str}] {item.name}")

        # 遍历只获取后缀为 .txt 的文件
        text_files1 = [f for f in folder.iterdir() if f.suffix == '.txt']
        text_files2 = list(folder.glob("*.txt"))
        print(text_files1)
        print(text_files2)

    # 4. 复制文件夹
    copied_folder = shutil.copytree("docs", "copied_folder")
    print(f"\n复制文件夹: {copied_folder}")

    # 5. 移动文件夹
    # shutil.move("源路径", "目标路径")

    # 6. 删除文件+文件夹
    Path.unlink(copied_folder / "test.txt", missing_ok=True)
    Path.rmdir(copied_folder)
    shutil.rmtree(copied_folder)

    # 文件
    file_path = folder / "test.txt"
    print(file_path.name)  # 文件名: "test.txt"
    print(file_path.stem)  # 文件主名: "test"
    print(file_path.suffix)  # 后缀: ".txt"
    print(file_path.parent)  # 父目录: "docs"
    print(file_path.exists())  # 是否存在
    print(file_path.is_file())  # 是文件还是文件夹
    print(file_path.stat().st_size)  # 文件大小

    # 1. 创建文件并写入内容(会自动处理打开和关闭)
    if not file_path.exists():
        file_path.write_text("文件测试写入内容", encoding="utf-8")
    else:
        print(f"文件存在: {file_path}")

    # 写入文件：'w' 模式会覆盖现有文件
    with open(file_path, 'w') as f:
        f.write('Hello world!\n')  # 返回写入的字符数

    # 追加到文件：'a' 模式会追加到现有文件
    with open(file_path, 'a') as f:
        f.write('追加内容.')

    # 2. 读取文件内容，如果处理 GB 级别的大文件，不能一次性 read_text()
    content = file_path.read_text(encoding="utf-8")
    print(f"文件内容: {content}")

    # 3. 读取文件内容，with，这种方式内存占用极低，因为它是按需读取的
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read() # 读取整个文件内容
        lines = f.readlines()  # 返回一个列表，其中每行都是一个字符串
    print(f"文件内容: {content}")
    print(f"文件行数: {len(lines)}")

    # 4.删除文件
    # file_path.unlink(missing_ok=True)
    # print(f"删除文件: {file_path}")


# 2. JSON 文件操作
class Address:
    def __init__(self, city: str = "", district: str = ""):
        self.city = city
        self.district = district

    def __repr__(self):
        return f"Address(city='{self.city}', district='{self.district}')"


class Student:
    def __init__(self, name: str = "", age: int = 0, skills: list = None,
                 is_active: bool = False, address: Address = None):
        self.name = name
        self.age = age
        self.skills = skills or []
        self.is_active = is_active
        self.address = address or Address()

    def __repr__(self):
        return (f"Student(name='{self.name}', age={self.age}, "
                f"skills={self.skills}, is_active={self.is_active}, address={self.address})")

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        """从字典创建 Student 对象"""
        address_data = data.get("address", {})
        address = Address(
            city=address_data.get("city", ""),
            district=address_data.get("district", "")
        )
        return cls(
            name=data.get("name", ""),
            age=data.get("age", 0),
            skills=data.get("skills", []),
            is_active=data.get("is_active", False),
            address=address
        )

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "name": self.name,
            "age": self.age,
            "skills": self.skills,
            "is_active": self.is_active,
            "address": {
                "city": self.address.city,
                "district": self.address.district
            }
        }


def demo_json():
    # 1. 读取 JSON 文件
    system_json_path = Path("docs/subsystems.json")
    with open(system_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"读取 JSON: {data}")

    # 2. 更新 JSON 文件 (追加数据)
    if system_json_path.exists():
        with open(system_json_path, "r+", encoding="utf-8") as f:
            # 1. 读取文件内容
            existing_data = json.load(f)
            # 2. 修改数据
            existing_data["name"] = "张三"
            existing_data["age"] = 25
            # 3. 写回文件
            f.seek(0)  # 把文件指针移到文件开头（覆盖模式）
            json.dump(existing_data, f, ensure_ascii=False, indent=4)  # 把字典转成 JSON 写入
            f.truncate()  # 截断后面可能残留的旧内容
    print("更新 JSON 文件 (追加字段)")

    # 3. 写入 JSON 文件
    stu_json_path = Path("docs/student.json")
    json_data = {
        "name": "张三",
        "age": 25,
        "skills": ["Python", "JavaScript", "Go"],
        "is_active": True,
        "address": {"city": "北京", "district": "朝阳区"}
    }
    with open(stu_json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    # 4. Student 类与 JSON 文件互转
    student = Student.from_dict(json_data)
    print(f"字典转 Student 对象: {student}")
    print(f"学生姓名: {student.name}, 年龄: {student.age}")
    print(f"技能列表: {student.skills}")
    print(f"地址: {student.address.city} {student.address.district}")

    converted_dict = student.to_dict()
    print(f"\nStudent 对象转字典: {converted_dict}")


# 3. YAML 文件操作
def demo_yaml():
    yaml_file = Path("docs/application.yaml")

    # 1. 写入 YAML 文件
    data = {
        "name": "李四",
        "age": 30,
        "skills": ["Python", "Docker", "Kubernetes"],
        "is_active": True,
        "address": {"city": "上海", "district": "浦东新区"}
    }

    with open(yaml_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"写入 YAML: {yaml_file}")

    # 2. 读取 YAML 文件
    with open(yaml_file, "r", encoding="utf-8") as f:
        loaded_data = yaml.safe_load(f)
    print(f"读取 YAML: {loaded_data}")

    # 3. 更新 YAML 文件 (追加数据)
    if yaml_file.exists():
        with open(yaml_file, "r", encoding="utf-8") as f:
            existing_data = yaml.safe_load(f) or {}
            existing_data["updated"] = True
            existing_data["score"] = 88.5
        with open(yaml_file, "w", encoding="utf-8") as f:
            yaml.dump(existing_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print("更新 YAML 文件 (追加字段)")

    # 5. YAML 字符串与 Python 对象互转
    yaml_string = yaml.dump(data, allow_unicode=True, default_flow_style=False)
    print(f"\nPython 对象转 YAML 字符串:\n{yaml_string}")

    parsed_object = yaml.safe_load(yaml_string)
    print(f"YAML 字符串转 Python 对象: {parsed_object}")

    # 清理测试文件
    # yaml_file.unlink()
    # print("清理测试文件\n")


# 4. CSV 文件操作
import csv


def demo_csv():
    csv_file = Path("docs/teachers.csv")

    # 1. 写入 CSV 文件
    teachers = [
        ["name", "age", "city"],
        ["张三", 25, "北京"],
        ["李四", 30, "上海"],
        ["王五", 28, "深圳"]
    ]

    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(teachers)
    print(f"写入 CSV: {csv_file}")

    # 2. 读取 CSV 文件（逐行）
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

    # 3. 读取 CSV 文件（作为字典）
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"姓名: {row['name']}, 年龄: {row['age']}, 城市: {row['city']}")

    # 4. 追加数据到 CSV
    with open(csv_file, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["赵六", 22, "广州"])

    # 5. 读取更新后的内容
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

    # 6. 写入字典形式的 CSV
    dict_csv_file = Path("docs/teachers_dict.csv")
    teachers_dict = [
        {"name": "张三", "age": 25, "city": "北京"},
        {"name": "李四", "age": 30, "city": "上海"},
        {"name": "王五", "age": 28, "city": "深圳"}
    ]

    with open(dict_csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
        writer.writeheader()
        writer.writerows(teachers_dict)
    print(f"\n字典写入 CSV: {dict_csv_file}")

    # 7. 读取字典形式的 CSV
    with open(dict_csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"姓名: {row['name']}, 年龄: {row['age']}, 城市: {row['city']}")


if __name__ == "__main__":
    demo_file()
    demo_json()
    demo_yaml()
    demo_csv()
