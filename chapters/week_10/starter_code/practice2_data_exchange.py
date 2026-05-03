"""Week 10 练习 2：数据导入导出工具。"""

import json
from pathlib import Path


def export_data(data, filepath, format="json"):
    """导出字典或列表到 JSON/TXT 文件，成功返回 True。"""
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        if format == "json":
            with path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        elif format == "txt":
            with path.open("w", encoding="utf-8") as file:
                if isinstance(data, dict):
                    for key, value in data.items():
                        file.write(f"{key}: {value}\n")
                elif isinstance(data, list):
                    for item in data:
                        file.write(f"{item}\n")
                else:
                    return False
        else:
            return False
        return True
    except OSError:
        return False


def import_data(filepath):
    """从 JSON 文件导入字典或列表，失败返回 None。"""
    path = Path(filepath)
    if not path.exists():
        return None

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return None

    return data if isinstance(data, (dict, list)) else None


def convert_format(input_path, output_path, output_format):
    """把 JSON 文件转换为指定输出格式。"""
    data = import_data(input_path)
    if data is None:
        return False
    return export_data(data, output_path, output_format)
