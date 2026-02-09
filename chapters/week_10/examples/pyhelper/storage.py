"""
storage.py - PyHelper 存储模块（Week 10 JSON 版本）

职责：负责学习记录的文件读写操作（JSON 格式）

功能：
- save_notes()：保存笔记到 JSON 文件
- load_notes()：从 JSON 文件加载笔记
- export_notes()：导出笔记到文件（JSON/TXT 格式）
- import_notes()：从 JSON 文件导入笔记
- migrate_note()：数据迁移（处理旧版本数据）

运行方式（测试）：
  python3 storage.py

导入方式：
  from storage import save_notes, load_notes, export_notes, import_notes
"""

import json
from pathlib import Path
import datetime

# 默认数据文件路径
DATA_FILE = Path.home() / ".pyhelper" / "notes.json"


def _ensure_data_dir():
    """确保数据目录存在"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def _default_serializer(obj):
    """自定义序列化函数，处理日期时间类型"""
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def save_notes(notes):
    """
    保存笔记到 JSON 文件

    Args:
        notes: 笔记列表（每个笔记是字典）

    Returns:
        True 如果保存成功
    """
    _ensure_data_dir()

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False, default=_default_serializer)

    return True


def load_notes():
    """
    从 JSON 文件加载笔记

    Returns:
        笔记列表，如果文件不存在或损坏则返回空列表

    防御性处理：
    - 文件不存在：返回空列表
    - JSON 格式错误：打印错误，返回空列表
    - 数据类型错误：打印警告，返回空列表
    """
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            notes = json.load(f)

        # 验证数据类型
        if not isinstance(notes, list):
            print("警告: 数据文件格式不正确，已重置")
            return []

        # 数据迁移：确保每条笔记都有必要的字段
        notes = [migrate_note(note) for note in notes]

        return notes

    except json.JSONDecodeError:
        print("错误: 数据文件损坏，已重置")
        return []
    except Exception as e:
        print(f"错误: 读取数据失败 - {e}")
        return []


def migrate_note(note):
    """
    将旧版本笔记迁移到最新版本

    版本变更历史：
    - v1: 只有 date 和 content
    - v2: 添加 tags 字段
    - v3: 添加 created_at 字段
    - v4: 添加 mood 字段

    Args:
        note: 笔记字典

    Returns:
        迁移后的笔记字典
    """
    # 确保基本字段存在
    if not isinstance(note, dict):
        return {"date": "", "content": str(note), "tags": [], "mood": ""}

    # v1 → v2: 添加 tags 字段
    if "tags" not in note:
        note["tags"] = []

    # v2 → v3: 添加 created_at 字段
    if "created_at" not in note:
        note["created_at"] = note.get("date", "")

    # v3 → v4: 添加 mood 字段
    if "mood" not in note:
        note["mood"] = ""

    return note


def export_notes(filepath, format="json"):
    """
    导出笔记到文件

    Args:
        filepath: 输出文件路径
        format: 导出格式，支持 "json" 或 "txt"

    Returns:
        导出的笔记数量

    Raises:
        ValueError: 如果格式不支持
    """
    notes = load_notes()
    filepath = Path(filepath)

    if format == "json":
        # 导出为 JSON 格式
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(notes, f, indent=2, ensure_ascii=False, default=_default_serializer)

    elif format == "txt":
        # 导出为易读的文本格式
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=" * 50 + "\n")
            f.write("PyHelper 学习笔记导出\n")
            f.write(f"导出时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"笔记数量: {len(notes)}\n")
            f.write("=" * 50 + "\n\n")

            for i, note in enumerate(notes, 1):
                f.write(f"[{i}] 日期: {note.get('date', '未知')}\n")
                f.write(f"    内容: {note.get('content', '')}\n")
                if note.get('mood'):
                    f.write(f"    心情: {note['mood']}\n")
                if note.get('tags'):
                    f.write(f"    标签: {', '.join(note['tags'])}\n")
                f.write("-" * 40 + "\n")

    else:
        raise ValueError(f"不支持的格式: {format}")

    print(f"已导出 {len(notes)} 条笔记到 {filepath}")
    return len(notes)


def import_notes(filepath):
    """
    从 JSON 文件导入笔记

    如果笔记已存在（相同日期和内容），则跳过（去重）

    Args:
        filepath: JSON 文件路径

    Returns:
        成功导入的新笔记数量
    """
    filepath = Path(filepath)

    if not filepath.exists():
        print(f"错误: 文件不存在 - {filepath}")
        return 0

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            new_notes = json.load(f)

        # 验证数据格式
        if not isinstance(new_notes, list):
            print("错误: 文件格式不正确（根元素必须是列表）")
            return 0

        # 加载现有笔记
        existing_notes = load_notes()
        existing_keys = {
            (n.get("date"), n.get("content")) for n in existing_notes
        }

        # 导入新笔记（去重）
        added = 0
        for note in new_notes:
            if not isinstance(note, dict):
                continue

            key = (note.get("date"), note.get("content"))
            if key not in existing_keys:
                # 迁移数据格式
                note = migrate_note(note)
                existing_notes.append(note)
                existing_keys.add(key)
                added += 1

        # 保存
        save_notes(existing_notes)
        print(f"成功导入 {added} 条新笔记（跳过 {len(new_notes) - added} 条重复）")
        return added

    except json.JSONDecodeError as e:
        print(f"错误: JSON 格式不正确 - {e}")
        return 0
    except Exception as e:
        print(f"错误: 导入失败 - {e}")
        return 0


# =====================
# 测试代码
# =====================

if __name__ == "__main__":
    print("=== 测试 storage 模块（JSON 版本）===\n")

    import tempfile

    # 保存原始数据文件路径
    original_data_file = DATA_FILE

    with tempfile.TemporaryDirectory() as tmpdir:
        # 使用临时目录作为数据目录
        # 通过修改模块全局变量来指向临时文件
        import sys
        current_module = sys.modules[__name__]
        current_module.DATA_FILE = Path(tmpdir) / "test_notes.json"

        # 测试数据
        test_notes = [
            {"date": "2026-02-09", "content": "学习了 JSON 序列化", "mood": "开心", "tags": ["Python", "JSON"]},
            {"date": "2026-02-08", "content": "练习了数据导入导出", "mood": "充实", "tags": ["Python"]},
        ]

        # 测试保存
        print("--- 测试 save_notes ---")
        save_notes(test_notes)
        print(f"✓ 已保存 {len(test_notes)} 条笔记")
        print(f"  文件位置: {DATA_FILE}")
        print(f"  文件内容预览:")
        content = DATA_FILE.read_text()
        print(content[:200] + "...\n")

        # 测试加载
        print("--- 测试 load_notes ---")
        loaded = load_notes()
        print(f"✓ 已加载 {len(loaded)} 条笔记")
        assert len(loaded) == len(test_notes), "数据数量不一致"
        print("✓ 数据验证通过\n")

        # 测试数据迁移
        print("--- 测试 migrate_note ---")
        old_note = {"date": "2026-01-01", "content": "旧格式笔记"}  # 缺少 tags, mood
        migrated = migrate_note(old_note)
        print(f"原始笔记: {old_note}")
        print(f"迁移后: {migrated}")
        assert "tags" in migrated, "迁移后应该有 tags 字段"
        assert "mood" in migrated, "迁移后应该有 mood 字段"
        print("✓ 数据迁移正常\n")

        # 测试导出 JSON
        print("--- 测试 export_notes (JSON) ---")
        export_path = Path(tmpdir) / "export.json"
        count = export_notes(export_path, format="json")
        print(f"✓ 导出 {count} 条笔记到 JSON\n")

        # 测试导出 TXT
        print("--- 测试 export_notes (TXT) ---")
        export_txt_path = Path(tmpdir) / "export.txt"
        count = export_notes(export_txt_path, format="txt")
        print(f"✓ 导出 {count} 条笔记到 TXT")
        print("  文件内容预览:")
        print(export_txt_path.read_text()[:300] + "...\n")

        # 测试导入
        print("--- 测试 import_notes ---")
        # 创建一个新的导入文件
        import_data = [
            {"date": "2026-02-07", "content": "新导入的笔记", "mood": "好奇"},
            {"date": "2026-02-09", "content": "学习了 JSON 序列化", "mood": "开心"},  # 重复的
        ]
        import_file = Path(tmpdir) / "import.json"
        with open(import_file, "w", encoding="utf-8") as f:
            json.dump(import_data, f)

        added = import_notes(import_file)
        print(f"✓ 成功导入 {added} 条新笔记（应该只有 1 条，另 1 条是重复的）\n")

        # 验证最终数据
        final_notes = load_notes()
        print(f"--- 最终笔记数量: {len(final_notes)} ---")
        for note in final_notes:
            print(f"  [{note['date']}] {note['content'][:20]}...")

        # 恢复原始数据文件路径
        current_module.DATA_FILE = original_data_file

    print("\n✓ 所有测试通过！")
