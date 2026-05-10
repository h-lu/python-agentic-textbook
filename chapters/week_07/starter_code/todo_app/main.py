"""Todo 多模块入口。"""

try:
    from .input_handler import get_choice, get_todo_title
    from .storage import load_todos, save_todos
    from .todo_manager import add_todo, complete_todo, show_todos
except ImportError:  # direct script fallback
    from input_handler import get_choice, get_todo_title
    from storage import load_todos, save_todos
    from todo_manager import add_todo, complete_todo, show_todos


def main():
    todos = load_todos()
    while True:
        print("\n1. 添加待办")
        print("2. 查看待办")
        print("3. 标记完成")
        print("4. 保存并退出")
        choice = get_choice()
        if choice == 1:
            add_todo(todos, get_todo_title())
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
