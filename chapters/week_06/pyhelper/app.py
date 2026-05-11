# PyHelper - 你的命令行学习助手
# Week 06：异常处理与防御性编程

import os
from datetime import date
from pathlib import Path
from tempfile import gettempdir

DEFAULT_NAME = "同学"
DAILY_MESSAGE = "写代码就像搭积木，一块一块来。"
SAMPLE_DATA_FILE = Path(__file__).with_name("pyhelper_data.txt")
MOOD_ADVICE = {
    "开心": "太好了！趁状态好，挑战一道稍难的练习题。",
    "累": "先休息 5 分钟，再回来写 3 行代码。",
    "卡住": "把报错复制下来，只解决最上面的一条。",
    "紧张": "先跑通最小例子，再慢慢加功能。",
}

def data_file() -> Path:
    return Path(os.environ.get("PYHELPER_DATA_FILE", Path(gettempdir()) / "pyhelper_week06_data.txt"))

def is_valid_date(text: str) -> bool:
    try:
        date.fromisoformat(text)
        return True
    except ValueError:
        return False

def get_menu_choice(raw: str, valid: set[str]) -> str | None:
    choice = raw.strip()
    return choice if choice in valid else None

def safe_record(date_text: str, content: str) -> dict[str, str] | None:
    date_text = date_text.strip()
    content = content.strip()
    if not is_valid_date(date_text) or not content:
        return None
    return {"date": date_text, "content": content}

def build_welcome(name: str = DEFAULT_NAME) -> str:
    return f"欢迎使用 PyHelper，{(name.strip() or DEFAULT_NAME)}！\n今日一句：{DAILY_MESSAGE}"

def advice_for_mood(mood: str) -> str:
    for keyword, advice in MOOD_ADVICE.items():
        if keyword in mood.strip():
            return advice
    return "不管现在什么心情，先完成一个 10 分钟小任务。"

def add_record(records: list[dict[str, str]], date_text: str, content: str) -> bool:
    record = safe_record(date_text, content)
    if record is None:
        return False
    records.append(record)
    return True

def list_records(records: list[dict[str, str]]) -> list[str]:
    return [f"{item['date']}: {item['content']}" for item in records]

def stats(records: list[dict[str, str]]) -> str:
    days = {item["date"] for item in records}
    return f"共 {len(records)} 条记录，覆盖 {len(days)} 天。"

def parse_line(line: str) -> dict[str, str] | None:
    try:
        date_text, content = line.strip().split("|", 1)
    except ValueError:
        return None
    return safe_record(date_text, content)

def load_records(path: Path | None = None) -> list[dict[str, str]]:
    path = path or data_file()
    source = path if path.exists() else SAMPLE_DATA_FILE
    records: list[dict[str, str]] = []
    try:
        lines = source.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return records
    except OSError as exc:
        print(f"读取记录失败：{exc}")
        return records
    for line in lines:
        record = parse_line(line)
        if record is not None:
            records.append(record)
    return records

def save_records(records: list[dict[str, str]], path: Path | None = None) -> None:
    path = path or data_file()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(f"{item['date']}|{item['content']}\n" for item in records), encoding="utf-8")
    except OSError as exc:
        print(f"保存记录失败：{exc}")

def render_menu() -> str:
    return "\n1. 获取学习建议\n2. 新增学习记录\n3. 查看学习记录\n4. 查看统计\n5. 保存并退出"

def main() -> None:
    name = input("你的名字是？").strip() or DEFAULT_NAME
    records = load_records()
    print(build_welcome(name))
    while True:
        print(render_menu())
        choice = get_menu_choice(input("请选择："), {"1", "2", "3", "4", "5"})
        if choice == "1":
            print("学习建议：" + advice_for_mood(input("你今天学习状态如何？")))
        elif choice == "2":
            ok = add_record(records, input("日期 YYYY-MM-DD："), input("学习内容："))
            print("已记录。" if ok else "日期或内容不合法，未保存。")
        elif choice == "3":
            print("\n".join(list_records(records)) or "暂无记录。")
        elif choice == "4":
            print(stats(records))
        elif choice == "5":
            save_records(records)
            print("已保存，下次见！")
            break
        else:
            print("请输入 1-5。")

if __name__ == "__main__":
    main()
