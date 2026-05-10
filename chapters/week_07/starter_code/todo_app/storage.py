"""Todo 数据读写。"""

from pathlib import Path


def get_data_file(filename="todos.txt"):
    return Path(filename)


def load_todos(filename="todos.txt"):
    path = get_data_file(filename)
    if not path.exists():
        return []
    todos = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        marker, title = line.split("|", 1)
        todos.append({"title": title, "done": marker == "1"})
    return todos


def save_todos(todos, filename="todos.txt"):
    path = get_data_file(filename)
    lines = [f"{'1' if todo.get('done') else '0'}|{todo.get('title', '')}" for todo in todos]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
