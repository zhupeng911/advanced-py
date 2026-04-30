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
    print(f'当前工作目录绝对路径: {Path.cwd()}')
    print(f"文件夹相对路径: {folder}")
    print(f"文件夹绝对路径: {folder.resolve()}")
    print(f'文件夹大小: {folder.stat().st_size} 字节')
    print(f"文件夹存在: {folder.exists()}")
    print(f"文件夹是否是目录: {folder.is_dir()}")
    print(f"文件夹是否是文件:{folder.is_file()}")
    print(f"文件夹是否是符号链接: {folder.is_symlink()}")

    # 1. 创建文件夹
    folder.mkdir(exist_ok=True)  # exist_ok=True 表示目录已存在时不报错
    print(f"创建文件夹: {folder}")

    # 创建多层目录
    deep_folder = Path("docs/a/b/c")
    deep_folder.mkdir(parents=True, exist_ok=True)
    print(f"创建多层目录: {deep_folder}")

    # 2. 重命名文件夹
    renamed_folder = deep_folder.rename("docs/a/b/c-update")
    print(f"重命名文件夹: {renamed_folder}")

    # 3. 遍历文件夹
    if folder.exists() and folder.is_dir():
        for file in folder.glob("*"):  # 仅限当前目录
            print(file)
        for file in folder.rglob("*"):  # 递归列出所有子目录和文件
            print(file)
        for item in folder.iterdir():  # 当你需要查看所有内容（文件+文件夹）且不关心过滤规则时。
            type_str = "文件夹" if item.is_dir() else "文件"
            print(f"[{type_str}] {item.name}")

        # 遍历只获取后缀为 .txt 的文件
        text_files1 = [f for f in folder.iterdir() if f.suffix == '.txt']
        text_files2 = list(folder.glob("*.txt"))
        print(text_files1)
        print(text_files2)

    # 4. 复制文件夹（目标已存在会报错，可用 shutil.copytree + dirs_exist_ok=True 覆盖）
    # copied_folder = shutil.copytree("docs", "docs_bk")
    # print(f"复制文件夹: {copied_folder}")
    copied_folder = shutil.copytree("docs", "docs_bk", dirs_exist_ok=True)

    # 5. 移动文件夹
    # shutil.move("源路径", "目标路径")

    # 6. 删除文件+文件夹
    Path.rmdir(renamed_folder)  # 只能删除空目录
    Path.rmdir(Path("docs/a/b"))  # 只能删除空目录
    Path.rmdir(Path("docs/a"))  # 只能删除空目录
    shutil.rmtree(copied_folder)  # 递归删除非空目录（慎用！）

    # 文件
    file_path = folder / "test.txt"
    print(file_path.name)  # 文件名: "test.txt"
    print(file_path.stem)  # 文件主名: "test"
    print(file_path.suffix)  # 后缀: ".txt"
    print(file_path.parent)  # 父目录: "docs"
    print(file_path.exists())  # 是否存在
    print(file_path.is_file())  # 是文件还是文件夹
    print(file_path.stat().st_size)  # 文件大小

    # 1. 直接写(会自动处理打开和关闭)
    file_path.write_text("文件测试写入内容", encoding="utf-8")

    # 2. 直接读（大文件不推荐）
    content = file_path.read_text(encoding="utf-8")
    print(f"文件内容: {content}")

    # 3.按需读写
    # 写入文件：'w' 模式会覆盖现有文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('Hello world!')

    # 追加到文件：'a' 模式会追加到现有文件
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write('追加内容.')

    # 按需读
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()  # 读取整个文件内容
    print(f"文件内容: {content}")

    # 4.删除文件
    # file_path.unlink(missing_ok=True)
    # print(f"删除文件: {file_path}")


# 2. JSON 文件操作
def demo_json():
    # 1. 读取 JSON 文件
    coder_json_path = Path("docs/Coder.json")
    with open(coder_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"读取 JSON: {data}")

    # 2. 更新 JSON 文件 (覆盖数据)
    temp_data = {"name": "张三", "age": 25}
    with open(coder_json_path, "w", encoding="utf-8") as f:
        json.dump(temp_data, f, ensure_ascii=False, indent=4)

    # 3. 更新 JSON 文件 (追加数据)
    if coder_json_path.exists():
        with open(coder_json_path, "r+", encoding="utf-8") as f:
            # 1. 读取文件内容
            existing_data = json.load(f)
            # 2. 修改数据
            existing_data["name"] = "李四"  # 更新
            existing_data["age"] = 99  # 更新
            existing_data["city"] = "上海"  # 新增
            # 3. 写回文件
            f.seek(0)  # 把文件指针移到文件开头（覆盖模式）
            json.dump(existing_data, f, ensure_ascii=False,
                      indent=4)  # 把字典转成 JSON 写入 ensure_ascii=False 支持中文, indent=4 格式化
            f.truncate()  # 截断后面可能残留的旧内容
    print("更新 JSON 文件 (追加字段)")

    # 3. 写入 JSON 文件
    stu_info = {
        "name": "张三",
        "age": 25,
        "skills": ["Python", "JavaScript", "Go"],
        "is_active": True,
        "address": {"city": "北京", "district": "朝阳区"}
    }
    with open(Path("docs/student.json"), "w", encoding="utf-8") as f:
        json.dump(stu_info, f, ensure_ascii=False, indent=4)

    # 4. Student -> JSON
    student = Student(
        name="张三",
        age=25,
        skills=["Python", "JavaScript", "Go"],
        is_active=True,
        address=Address(
            city="北京",
            district="朝阳区")
    )
    student_json = student.to_dict()
    print(f"Student对象转字典: {student_json}")

    # 5. JSON -> Student
    student = Student.from_dict(stu_info)
    print(f"字典转 Student 对象: {student}")
    print(f"学生姓名: {student.name}, 年龄: {student.age}")
    print(f"技能列表: {student.skills}")
    print(f"地址: {student.address.city} {student.address.district}")


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


# 3. YAML 文件操作
def demo_yaml():
    yaml_path = Path("docs/application.yaml")

    # 1. 读取 YAML 文件
    with open(yaml_path, "r", encoding="utf-8") as f:
        yaml_data = yaml.safe_load(f)
    print(f"读取 YAML: {yaml_data}")

    # 2. 写入 YAML 文件 [覆盖]
    content = {
        "spring": {
            "profiles": {
                "active": True
            },
            "redis": {
                "host": "127.0.0.1",
                "port": 6379
            }
        },
        "skills": ["Python", "Docker", "Kubernetes"]
    }
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(content, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"覆盖写入 YAML: {yaml_path}")

    # 3. 更新 YAML 文件 (追加数据)
    with open(yaml_path, "r+", encoding="utf-8") as f:
        existing_data = yaml.safe_load(f) or {}
        existing_data["updated"] = True
        existing_data["score"] = 88.5
        existing_data["spring"]["profiles"]["active"] = False  # 更新active =false
        f.seek(0)  # 指针移到开头
        yaml.dump(existing_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        f.truncate()  # 截断多余内容

    # 6. YAML -> Python 类
    app_config = AppConfig.from_dict(yaml_data)
    print(f"YAML 转 AppConfig: {app_config}")
    print(f"  - active: {app_config.spring.profiles['active']}")
    print(f"  - redis: {app_config.spring.redis}")
    print(f"  - skills: {app_config.skills}")

    # 7. Python 类 -> YAML
    config_dict = app_config.to_dict()
    print(f"AppConfig 转字典: {config_dict}")


# YAML 对应配置类
class RedisConfig:
    def __init__(self, host: str = "127.0.0.1", port: int = 6379):
        self.host = host
        self.port = port

    def __repr__(self):
        return f"RedisConfig(host='{self.host}', port={self.port})"


class SpringConfig:
    def __init__(self, profiles: dict = None, redis: RedisConfig = None):
        self.profiles = profiles or {"active": False}
        self.redis = redis or RedisConfig()

    def __repr__(self):
        return f"SpringConfig(profiles={self.profiles}, redis={self.redis})"


class AppConfig:
    def __init__(self, spring: SpringConfig = None, skills: list = None,
                 updated: bool = False, score: float = 0.0):
        self.spring = spring or SpringConfig()
        self.skills = skills or []
        self.updated = updated
        self.score = score

    def __repr__(self):
        return (f"AppConfig(spring={self.spring}, skills={self.skills}, "
                f"updated={self.updated}, score={self.score})")

    @classmethod
    def from_dict(cls, data: dict) -> "AppConfig":
        spring_data = data.get("spring", {})
        redis_data = spring_data.get("redis", {})
        return cls(
            spring=SpringConfig(
                profiles=spring_data.get("profiles", {"active": False}),
                redis=RedisConfig(
                    host=redis_data.get("host", "127.0.0.1"),
                    port=redis_data.get("port", 6379)
                )
            ),
            skills=data.get("skills", []),
            updated=data.get("updated", False),
            score=data.get("score", 0.0)
        )

    def to_dict(self) -> dict:
        return {
            "spring": {
                "profiles": self.spring.profiles,
                "redis": {"host": self.spring.redis.host, "port": self.spring.redis.port}
            },
            "skills": self.skills,
            "updated": self.updated,
            "score": self.score
        }


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
