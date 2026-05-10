"""Todo 业务逻辑。"""


def add_todo(todos, title):
    title = title.strip()
    if not title:
        return False
    todos.append({"title": title, "done": False})
    return True


def complete_todo(todos, index):
    if 1 <= index <= len(todos):
        todos[index - 1]["done"] = True
        return True
    return False


def show_todos(todos):
    if not todos:
        print("暂无待办")
        return
    for i, todo in enumerate(todos, 1):
        marker = "x" if todo.get("done") else " "
        print(f"{i}. [{marker}] {todo.get('title', '')}")
