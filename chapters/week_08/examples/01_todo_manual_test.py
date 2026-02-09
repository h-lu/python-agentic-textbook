"""
示例：手动测试版本（有问题的代码）

本例演示：为什么手动测试容易遗漏问题
- 代码看起来能工作
- 但隐藏了边界情况的 bug
- 每次改代码都要手动重测，既慢又容易漏

运行方式：
  cd chapters/week_08/examples
  python3 01_todo_manual_test.py

预期输出：
  手动测试显示"正常"，但 delete_task 有边界情况未处理
"""


def add_task(tasks, task_name):
    """添加任务到列表"""
    task_name = task_name.strip()  # 去除首尾空格
    tasks.append({"name": task_name, "done": False})
    return tasks


def list_tasks(tasks):
    """列出所有任务"""
    if not tasks:
        print("暂无任务")
        return

    for i, task in enumerate(tasks, 1):
        status = "✓" if task["done"] else " "
        print(f"{i}. [{status}] {task['name']}")


def mark_done(tasks, index):
    """标记任务为完成（1-based 索引）"""
    if 1 <= index <= len(tasks):
        tasks[index - 1]["done"] = True
        return True
    return False


def delete_task(tasks, index):
    """删除指定索引的任务（1-based 索引）"""
    # BUG: 没有检查索引是否合法！
    # 当 index 为 0 或负数时，Python 会反向索引
    # 当 index 超过长度时，会抛出 IndexError
    tasks.pop(index - 1)
    return True


def manual_test():
    """手动测试 - 容易遗漏边界情况"""
    print("=== 手动测试 Todo Manager ===\n")

    tasks = []

    # 测试 1：添加任务
    print("1. 添加任务...")
    add_task(tasks, "买牛奶")
    add_task(tasks, "写作业")
    add_task(tasks, "  运动  ")  # 带空格的任务名
    print(f"   已添加 {len(tasks)} 个任务")

    # 测试 2：列出任务
    print("\n2. 列出任务...")
    list_tasks(tasks)

    # 测试 3：标记完成
    print("\n3. 标记第一个任务完成...")
    mark_done(tasks, 1)
    list_tasks(tasks)

    # 测试 4：删除任务
    print("\n4. 删除第二个任务...")
    delete_task(tasks, 2)
    list_tasks(tasks)

    print("\n=== 手动测试完成 ===")
    print("看起来一切正常？但边界情况没有测试！")
    print("试试 delete_task(tasks, 0) 或 delete_task(tasks, 99) 看看会发生什么")


# 反例：展示有问题的调用
def show_the_bug():
    """展示 delete_task 的 bug"""
    print("\n=== 展示隐藏的 bug ===")

    tasks = [{"name": "买牛奶", "done": False}]

    # 这个调用会导致 IndexError，但手动测试时可能没测到
    try:
        # 索引 99 不存在，应该返回 False 或给出提示
        # 但实际上会抛出 IndexError
        result = delete_task(tasks, 99)
        print(f"删除结果: {result}")
    except IndexError as e:
        print(f"出错了！IndexError: {e}")
        print("这就是手动测试容易遗漏的问题")


if __name__ == "__main__":
    manual_test()
    show_the_bug()
