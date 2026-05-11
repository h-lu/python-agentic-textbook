"""Week 08 PyHelper: tested modules."""

from pathlib import Path
from tempfile import gettempdir

try:
    from .records import make_record, search_records
    from .storage import load_records, save_records
except ImportError:
    from records import make_record, search_records
    from storage import load_records, save_records

DATA_FILE = Path(gettempdir()) / "pyhelper_week08_demo.json"


def main() -> None:
    records = load_records(DATA_FILE)
    records.append(make_record("2026-05-11", "给 PyHelper 补测试"))
    save_records(DATA_FILE, records)
    print(search_records(records, "测试"))


if __name__ == "__main__":
    main()
