"""
Week 05 作业参考实现
题目：学习记录存储器

功能要求：
1. 添加学习记录（日期 + 内容）
2. 查看所有学习记录
3. 按关键词搜索学习记录
4. 退出时保存到文件 records.txt
5. 启动时从文件加载历史记录

运行方式：python3 chapters/week_05/starter_code/solution.py
"""

from datetime import datetime
from pathlib import Path


# =====================
# 日记本函数（与 tests/test_diary_app.py 的行为保持一致）
# =====================

def add_diary_entry(content, filename="diary.txt"):
    """
    追加一条日记记录

    content: 日记内容
    filename: 日记文件路径
    """
    diary_file = Path(filename)
    today = datetime.now().strftime("%Y-%m-%d")
    entry = f"{today}: {content}\n"

    with diary_file.open("a", encoding="utf-8") as file:
        file.write(entry)


def read_all_diaries(filename="diary.txt"):
    """
    读取所有非空日记记录

    文件不存在时返回空列表。
    """
    diary_file = Path(filename)
    if not diary_file.exists():
        return []

    content = diary_file.read_text(encoding="utf-8")
    return [line for line in content.splitlines() if line.strip()]


def search_diaries(keyword, filename="diary.txt"):
    """按关键词搜索日记记录"""
    return [line for line in read_all_diaries(filename) if keyword in line]


def count_diaries(filename="diary.txt"):
    """统计日记记录条数"""
    return len(read_all_diaries(filename))


# =====================
# 文件操作函数
# =====================

def load_records(filename="records.txt"):
    """
    从文件加载学习记录

    返回：字典，格式为 {"日期": ["内容1", "内容2", ...]}
    """
    data_file = Path(filename)
    records = {}

    # 检查文件是否存在
    if data_file.exists():
        content = data_file.read_text(encoding="utf-8")

        # 解析文件内容（每行格式：日期: 内容）
        for line in content.split("\n"):
            line = line.strip()
            if line:
                parts = line.split(": ", 1)
                if len(parts) == 2:
                    date, content = parts

                    # 如果日期不存在，创建一个空列表
                    if date not in records:
                        records[date] = []

                    # 添加内容到列表
                    records[date].append(content)

        print(f"✓ 已加载 {sum(len(v) for v in records.values())} 条学习记录")
    else:
        print("✓ 首次运行，将创建新的数据文件")

    return records


def save_records(records, filename="records.txt"):
    """
    保存学习记录到文件

    records: 字典，格式为 {"日期": ["内容1", "内容2", ...]}
    """
    data_file = Path(filename)

    # 构建文件内容
    content = ""
    for date in sorted(records.keys()):
        for item in records[date]:
            content += f"{date}: {item}\n"

    # 写入文件
    data_file.write_text(content, encoding="utf-8")

    total = sum(len(v) for v in records.values())
    print(f"✓ 已保存 {total} 条学习记录到 {filename}")


# =====================
# 核心功能函数
# =====================

def add_record(records):
    """
    添加学习记录

    records: 字典（会被修改）
    """
    date = input("请输入日期（如 02-09）：")

    # 如果日期不存在，创建空列表
    if date not in records:
        records[date] = []

    content = input("请输入今天学了什么：")

    # 添加到列表
    records[date].append(content)

    print(f"✓ 已添加：{date} - {content}")


def show_records(records):
    """
    查看所有学习记录

    records: 字典
    """
    if not records:
        print("✗ 还没有学习记录哦，去添加一些吧！")
        return

    print("\n=== 学习记录 ===")

    # 按日期排序后显示
    for date in sorted(records.keys()):
        print(f"\n{date}:")
        for item in records[date]:
            print(f"  - {item}")


def search_records(records, keyword):
    """
    按关键词搜索学习记录

    records: 字典
    keyword: 关键词

    返回：匹配的记录列表
    """
    results = []

    for date in records:
        for item in records[date]:
            if keyword in item:
                results.append(f"{date}: {item}")

    return results


# =====================
# 交互式菜单
# =====================

def print_menu():
    """打印菜单"""
    print("\n" + "=" * 40)
    print("  学习记录存储器")
    print("=" * 40)
    print("1. 添加学习记录")
    print("2. 查看所有记录")
    print("3. 搜索记录")
    print("4. 退出并保存")
    print("-" * 40)


def get_choice():
    """获取用户选择"""
    while True:
        choice = input("\n请选择（1-4）：")
        if choice in ["1", "2", "3", "4"]:
            return choice
        print("✗ 无效输入，请输入 1-4")


# =====================
# 主程序
# =====================

def main():
    """主函数"""
    # 启动时加载学习记录
    records = load_records()

    while True:
        print_menu()
        choice = get_choice()

        if choice == "1":
            add_record(records)

        elif choice == "2":
            show_records(records)

        elif choice == "3":
            keyword = input("请输入关键词：")
            if keyword.strip():
                results = search_records(records, keyword)
                if results:
                    print(f"\n=== 搜索结果（共 {len(results)} 条）===")
                    for result in results:
                        print(f"  {result}")
                else:
                    print(f"\n✗ 没有找到包含'{keyword}'的记录")
            else:
                print("✗ 关键词不能为空")

        elif choice == "4":
            # 退出前保存
            save_records(records)
            print("\n再见！祝你学习愉快！")
            break

        print()


# =====================
# 启动程序
# =====================

if __name__ == "__main__":
    main()


# =====================
# 实现说明
# =====================

"""
本实现的核心设计：

1. **数据结构**
   - 用字典存储记录：{"日期": ["内容1", "内容2", ...]}
   - 一个日期可以有多条记录（用列表存储）

2. **文件格式**
   - 每行一条记录，格式：日期: 内容
   - 示例：
     02-09: 学会了文件操作
     02-09: 学会了 pathlib
     02-10: 写了日记本项目

3. **文件操作**
   - 用 pathlib 管理路径（跨平台兼容）
   - 用 read_text() 和 write_text() 快捷读写
   - 统一用 UTF-8 编码（避免中文乱码）

4. **搜索功能**
   - 遍历所有记录，检查关键词是否在内容中
   - 返回匹配的记录列表

5. **错误处理（基础）**
   - 检查文件是否存在（path.exists()）
   - 检查输入是否为空（input().strip()）

本实现满足基础作业要求：
- ✓ 添加学习记录
- ✓ 查看所有记录
- ✓ 搜索记录
- ✓ 保存到文件
- ✓ 从文件加载

进阶挑战（可选）：
- 添加编辑功能（修改已有记录）
- 添加删除功能（删除某条记录）
- 添加统计功能（按日期统计学习天数）
- 添加异常处理（try/except）
- 用 dataclass 建模（Week 11 会学）
"""
