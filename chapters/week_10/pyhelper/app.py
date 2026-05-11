"""Week 10 PyHelper: JSON import/export."""

from pathlib import Path

try:
    from .records import add_record
    from .storage import export_json, load_json, save_json
except ImportError:
    from records import add_record
    from storage import export_json, load_json, save_json

DATA_FILE = Path(__file__).with_name("sample_records.json")


def main() -> None:
    records = load_json(DATA_FILE)
    demo_records = add_record(records.copy(), "2026-05-12", "导出 JSON", ["json", "export"])
    print(export_json(demo_records))


if __name__ == "__main__":
    main()
