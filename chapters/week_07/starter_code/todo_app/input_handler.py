"""Todo 命令行输入处理。"""


def get_choice():
    try:
        return int(input("请选择功能（1-4）："))
    except ValueError:
        return 0


def get_todo_title():
    while True:
        title = input("请输入待办标题：").strip()
        if title:
            return title
        print("待办标题不能为空")
