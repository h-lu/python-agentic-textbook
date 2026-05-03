"""Week 10 练习 6：JSON 配置管理器。"""

import json
import shutil
from pathlib import Path


class ConfigManager:
    """支持嵌套键的简单 JSON 配置管理器。"""

    def __init__(self, config_path):
        self.config_path = Path(config_path)
        self.config = {}
        if self.config_path.exists():
            with self.config_path.open("r", encoding="utf-8") as file:
                loaded = json.load(file)
            if isinstance(loaded, dict):
                self.config = loaded

    def get(self, key, default=None):
        current = self.config
        for part in key.split("."):
            if not isinstance(current, dict) or part not in current:
                return default
            current = current[part]
        return current

    def set(self, key, value):
        current = self.config
        parts = key.split(".")
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = value

    def save(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        if self.config_path.exists():
            shutil.copy2(self.config_path, self.config_path.with_suffix(".json.bak"))
        with self.config_path.open("w", encoding="utf-8") as file:
            json.dump(self.config, file, ensure_ascii=False, indent=2)

    def export(self, filepath, format="json"):
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        if format == "json":
            with path.open("w", encoding="utf-8") as file:
                json.dump(self.config, file, ensure_ascii=False, indent=2)
        elif format == "txt":
            with path.open("w", encoding="utf-8") as file:
                for key, value in self.config.items():
                    file.write(f"{key}: {value}\n")
        else:
            return False
        return True

    def import_config(self, filepath):
        with Path(filepath).open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            return False
        self.config.update(data)
        return True
