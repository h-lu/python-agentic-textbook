"""
示例：自定义格式的问题——为什么需要 JSON

本示例演示使用自定义分隔符格式存储数据时可能遇到的问题。
当数据内容包含分隔符本身时，解析就会出错。

运行方式：python3 chapters/week_10/examples/01_custom_format_problem.py
预期输出：展示解析成功和失败的案例
"""


def load_notes_old_format(filepath):
    """读取旧格式的学习记录（竖线分隔格式）"""
    notes = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) == 2:
                    notes.append({
                        "date": parts[0],
                        "content": parts[1]
                    })
                else:
                    print(f"警告：无法解析行（分隔符问题）：{line}")
    except FileNotFoundError:
        print(f"文件不存在：{filepath}")
    return notes


def save_notes_old_format(notes, filepath):
    """保存学习记录到旧格式（竖线分隔）"""
    with open(filepath, "w", encoding="utf-8") as f:
        for note in notes:
            f.write(f"{note['date']}|{note['content']}\n")


# =====================
# 演示问题
# =====================

if __name__ == "__main__":
    import tempfile
    from pathlib import Path

    print("=== 自定义格式的问题演示 ===\n")

    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "notes.txt"

        # 案例 1：正常数据（没有问题）
        print("案例 1：正常数据")
        normal_notes = [
            {"date": "2026-02-01", "content": "学习了 JSON 格式"},
            {"date": "2026-02-02", "content": "练习了序列化"},
        ]
        save_notes_old_format(normal_notes, test_file)
        loaded = load_notes_old_format(test_file)
        print(f"保存了 {len(normal_notes)} 条，成功读取了 {len(loaded)} 条")
        print("✓ 正常数据没问题\n")

        # 案例 2：内容包含分隔符（出现问题！）
        print("案例 2：内容包含竖线 |（分隔符本身）")
        problematic_notes = [
            {"date": "2026-02-03", "content": "学习了 split 方法，它按分隔符拆分字符串，比如 a|b|c"},
            {"date": "2026-02-04", "content": "了解了 | 管道符号的用法"},
        ]
        save_notes_old_format(problematic_notes, test_file)
        loaded = load_notes_old_format(test_file)
        print(f"保存了 {len(problematic_notes)} 条，成功读取了 {len(loaded)} 条")
        print("✗ 有数据丢失了！因为内容里的 | 被当成了分隔符\n")

        # 案例 3：尝试用更特殊的分隔符
        print("案例 3：尝试用更特殊的分隔符 |||")
        special_file = Path(tmpdir) / "notes_special.txt"

        with open(special_file, "w", encoding="utf-8") as f:
            for note in problematic_notes:
                f.write(f"{note['date']}|||{note['content']}\n")

        # 读取
        notes_from_special = []
        with open(special_file, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|||")
                if len(parts) == 2:
                    notes_from_special.append({"date": parts[0], "content": parts[1]})
                else:
                    print(f"警告：无法解析行：{line.strip()}")

        print(f"使用 ||| 分隔符，成功读取了 {len(notes_from_special)} 条")
        print("但问题：如果内容里有 ||| 呢？还是会出现同样的问题！")
        print()

        # 案例 4：更复杂的情况
        print("案例 4：多层级嵌套数据（自定义格式很难处理）")
        complex_data = {
            "date": "2026-02-05",
            "content": "学习了嵌套数据结构",
            "tags": ["Python", "JSON", "学习笔记"],
            "rating": 5,
            "metadata": {"source": "教材", "chapter": 10}
        }
        print(f"复杂数据：{complex_data}")
        print("自定义格式很难优雅地表示这种嵌套结构")
        print()

    print("=" * 50)
    print("结论：自定义格式的问题")
    print("1. 分隔符冲突：内容可能包含分隔符本身")
    print("2. 需要手动处理转义：增加复杂度")
    print("3. 难以表示嵌套结构")
    print("4. 其他工具无法识别")
    print()
    print("解决方案：使用标准格式，如 JSON")
