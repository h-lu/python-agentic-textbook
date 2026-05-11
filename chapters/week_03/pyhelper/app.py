"""Week 03 PyHelper: functions and a tiny menu."""

def get_advice(minutes: int) -> str:
    if minutes < 15:
        return "做一道最小练习题。"
    if minutes < 45:
        return "完成一个小函数，并自己运行一次。"
    return "做一个完整小项目，并写下复盘。"


def quote_of_day() -> str:
    return "不是等有信心才开始，而是开始后才会有信心。"


def render_menu() -> str:
    return "1. 获取学习建议\n2. 查看今日名言\n3. 退出"


def main() -> None:
    print("欢迎使用 PyHelper！")
    print(render_menu())
    print("\n演示：如果今天有 30 分钟，可以：" + get_advice(30))
    print("今日名言：" + quote_of_day())


if __name__ == "__main__":
    main()
