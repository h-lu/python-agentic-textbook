# PyHelper - 你的命令行学习助手
# Week 05：文本文件持久化

import os
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
    return Path(os.environ.get("PYHELPER_DATA_FILE", Path(gettempdir()) / "pyhelper_week05_data.txt"))

def build_welcome(name: str = DEFAULT_NAME) -> str:
    return f"欢迎使用 PyHelper，{(name.strip() or DEFAULT_NAME)}！\n今日一句：{DAILY_MESSAGE}"

def advice_for_mood(mood: str) -> str:
    for keyword, advice in MOOD_ADVICE.items():
        if keyword in mood.strip():
            return advice
    return "不管现在什么心情，先完成一个 10 分钟小任务。"

def add_record(records: list[dict[str, str]], date: str, content: str) -> dict[str, str]:
    record = {"date": date.strip(), "content": content.strip()}
    records.append(record)
    return record

def list_records(records: list[dict[str, str]]) -> list[str]:
    return [f"{item['date']}: {item['content']}" for item in records]

def stats(records: list[dict[str, str]]) -> str:
    days = {item["date"] for item in records}
    return f"共 {len(records)} 条记录，覆盖 {len(days)} 天。"

def load_records(path: Path | None = None) -> list[dict[str, str]]:
    path = path or data_file()
    source = path if path.exists() else SAMPLE_DATA_FILE
    records: list[dict[str, str]] = []
    if not source.exists():
        return records
    with source.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "|" not in line:
                continue
            date, content = line.split("|", 1)
            records.append({"date": date, "content": content})
    return records

def save_records(records: list[dict[str, str]], path: Path | None = None) -> None:
    path = path or data_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for item in records:
            f.write(f"{item['date']}|{item['content']}\n")

def render_menu() -> str:
    return "\n1. 获取学习建议\n2. 新增学习记录\n3. 查看学习记录\n4. 查看统计\n5. 保存并退出"

def main() -> None:
    name = input("你的名字是？").strip() or DEFAULT_NAME
    records = load_records()
    print(build_welcome(name))
    while True:
        print(render_menu())
        choice = input("请选择：").strip()
        if choice == "1":
            print("学习建议：" + advice_for_mood(input("你今天学习状态如何？")))
        elif choice == "2":
            add_record(records, input("日期 YYYY-MM-DD："), input("学习内容："))
            print("已记录。")
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
