#!/usr/bin/env python3
"""Week 12 作业参考实现：命令行习惯追踪器 habit-cli。"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path


DATA_FILE = Path("habits.json")
LOG_FILE = Path("habit.log")


def today_string():
    """返回今天的 ISO 日期字符串，方便测试替换。"""
    return date.today().isoformat()


def write_log(level, message):
    """把操作写入 habit.log。"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(f"{today_string()} - {level} - {message}\n")


def load_data():
    """加载习惯数据；首次运行返回空结构。"""
    if not DATA_FILE.exists():
        return {"habits": []}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        write_log("ERROR", "数据文件格式错误")
        return {"habits": []}

    if not isinstance(data, dict) or not isinstance(data.get("habits"), list):
        return {"habits": []}
    return data


def save_data(data):
    """保存习惯数据。"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def find_habit(data, name):
    """按名称查找习惯。"""
    for habit in data["habits"]:
        if habit.get("name") == name:
            return habit
    return None


def validate_name(name):
    """校验习惯名称并返回清洗后的名称。"""
    cleaned = name.strip() if isinstance(name, str) else ""
    if not cleaned:
        raise ValueError("习惯名称不能为空")
    return cleaned


def cmd_add(args):
    """添加习惯。"""
    try:
        name = validate_name(args.name)
    except ValueError as error:
        print(f"错误：{error}", file=sys.stderr)
        write_log("WARNING", str(error))
        return 1

    data = load_data()
    if find_habit(data, name):
        print("错误：习惯已存在", file=sys.stderr)
        write_log("WARNING", f"习惯已存在：{name}")
        return 1

    habit = {
        "name": name,
        "description": args.description or "",
        "created_at": today_string(),
        "active": True,
        "checkins": [],
    }
    data["habits"].append(habit)
    save_data(data)
    write_log("INFO", f"添加习惯：{name}")
    print(f"✓ 习惯已添加：{name}")
    return 0


def cmd_list(args):
    """列出习惯。"""
    data = load_data()
    habits = data["habits"]
    if getattr(args, "active", False):
        habits = [habit for habit in habits if habit.get("active", True)]

    if not habits:
        print("没有习惯")
        return 0

    print("习惯列表：")
    for index, habit in enumerate(habits, 1):
        active_text = "是" if habit.get("active", True) else "否"
        print(f"{index}. {habit['name']} - {habit.get('description', '')}")
        print(
            f"   创建时间：{habit.get('created_at', '')} | "
            f"活跃：{active_text} | 打卡次数：{len(habit.get('checkins', []))}"
        )
    return 0


def cmd_checkin(args):
    """记录一次打卡。"""
    try:
        name = validate_name(args.name)
    except ValueError as error:
        print(f"错误：{error}", file=sys.stderr)
        return 1

    data = load_data()
    habit = find_habit(data, name)
    if habit is None:
        print("错误：习惯不存在", file=sys.stderr)
        write_log("WARNING", f"习惯不存在：{name}")
        return 1

    today = today_string()
    if today not in habit["checkins"]:
        habit["checkins"].append(today)
    save_data(data)
    write_log("INFO", f"打卡成功：{name}")
    print(f"✓ 打卡成功：{name}")
    return 0


def cmd_log(args):
    """显示某个习惯的打卡历史。"""
    try:
        name = validate_name(args.name)
    except ValueError as error:
        print(f"错误：{error}", file=sys.stderr)
        write_log("WARNING", str(error))
        return 1

    data = load_data()
    habit = find_habit(data, name)
    if habit is None:
        print("错误：习惯不存在", file=sys.stderr)
        write_log("WARNING", f"习惯不存在：{name}")
        return 1

    print("打卡记录：")
    for item in habit.get("checkins", []):
        print(item)
    return 0


def cmd_delete(args):
    """删除习惯。"""
    try:
        name = validate_name(args.name)
    except ValueError as error:
        print(f"错误：{error}", file=sys.stderr)
        write_log("WARNING", str(error))
        return 1

    data = load_data()
    before = len(data["habits"])
    data["habits"] = [habit for habit in data["habits"] if habit.get("name") != name]

    if len(data["habits"]) == before:
        print("错误：习惯不存在", file=sys.stderr)
        write_log("WARNING", f"习惯不存在：{name}")
        return 1

    save_data(data)
    write_log("INFO", f"删除习惯：{name}")
    print(f"✓ 习惯已删除：{name}")
    return 0


def get_stats(data):
    """计算习惯统计信息。"""
    habits = data["habits"]
    return {
        "total_habits": len(habits),
        "active_habits": sum(1 for habit in habits if habit.get("active", True)),
        "total_checkins": sum(len(habit.get("checkins", [])) for habit in habits),
    }


def cmd_stats(args):
    """显示统计信息。"""
    stats = get_stats(load_data())
    if getattr(args, "json", False):
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print("习惯统计：")
        print(f"总习惯数：{stats['total_habits']}")
        print(f"活跃习惯：{stats['active_habits']}")
        print(f"总打卡次数：{stats['total_checkins']}")
    return 0


def create_parser():
    """创建 argparse 解析器。"""
    parser = argparse.ArgumentParser(description="habit-cli - 命令行习惯追踪器")
    parser.add_argument("--verbose", action="store_true", help="显示详细日志")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="添加习惯")
    add_parser.add_argument("name", help="习惯名称")
    add_parser.add_argument("--description", default="", help="习惯描述")
    add_parser.set_defaults(func=cmd_add)

    list_parser = subparsers.add_parser("list", help="列出习惯")
    list_parser.add_argument("--active", action="store_true", help="只显示活跃习惯")
    list_parser.set_defaults(func=cmd_list)

    checkin_parser = subparsers.add_parser("checkin", help="记录打卡")
    checkin_parser.add_argument("name", help="习惯名称")
    checkin_parser.set_defaults(func=cmd_checkin)

    log_parser = subparsers.add_parser("log", help="查看打卡历史")
    log_parser.add_argument("name", help="习惯名称")
    log_parser.set_defaults(func=cmd_log)

    delete_parser = subparsers.add_parser("delete", help="删除习惯")
    delete_parser.add_argument("name", help="习惯名称")
    delete_parser.set_defaults(func=cmd_delete)

    stats_parser = subparsers.add_parser("stats", help="显示统计信息")
    stats_parser.add_argument("--json", action="store_true", help="输出 JSON")
    stats_parser.set_defaults(func=cmd_stats)

    return parser


def main(argv=None):
    """CLI 主入口。"""
    parser = create_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
