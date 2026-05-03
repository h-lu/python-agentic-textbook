"""
Week 07 练习 2 起点：单文件 Todo List。

这个文件故意把输入、业务逻辑和存储放在一起，供学生重构为：

todo_app/
├── main.py
├── storage.py
├── todo_manager.py
└── input_handler.py
"""

from pathlib import Path


DATA_FILE = Path("todos.txt")


def load_todos():
    """从文本文件加载待办事项。"""
    if not DATA_FILE.exists():
        return []

    todos = []
    for line in DATA_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        done_marker, title = line.split("|", 1)
        todos.append({"title": title, "done": done_marker == "1"})
    return todos


def save_todos(todos):
    """把待办事项保存到文本文件。"""
    lines = []
    for todo in todos:
        done_marker = "1" if todo["done"] else "0"
        lines.append(f"{done_marker}|{todo['title']}")
    DATA_FILE.write_text("\n".join(lines), encoding="utf-8")


def add_todo(todos, title):
    """添加一条待办事项。"""
    title = title.strip()
    if not title:
        print("待办标题不能为空")
        return False
    todos.append({"title": title, "done": False})
    return True


def complete_todo(todos, index):
    """按 1-based 索引标记待办事项完成。"""
    if 1 <= index <= len(todos):
        todos[index - 1]["done"] = True
        return True
    print("没有这个编号的待办")
    return False


def show_todos(todos):
    """打印所有待办事项。"""
    if not todos:
        print("暂无待办")
        return

    for i, todo in enumerate(todos, 1):
        status = "x" if todo["done"] else " "
        print(f"{i}. [{status}] {todo['title']}")


def get_choice():
    """读取菜单选择。"""
    try:
        return int(input("请选择功能（1-4）："))
    except ValueError:
        return 0


def main():
    """单文件版本主循环。"""
    todos = load_todos()

    while True:
        print("\n1. 添加待办")
        print("2. 查看待办")
        print("3. 标记完成")
        print("4. 保存并退出")

        choice = get_choice()
        if choice == 1:
            add_todo(todos, input("请输入待办标题："))
        elif choice == 2:
            show_todos(todos)
        elif choice == 3:
            try:
                index = int(input("请输入待办编号："))
            except ValueError:
                print("编号必须是数字")
                continue
            complete_todo(todos, index)
        elif choice == 4:
            save_todos(todos)
            print("已保存，再见！")
            break
        else:
            print("请输入 1-4 之间的数字")


if __name__ == "__main__":
    main()
