"""Week 09 练习 2：用 split 和 join 处理 CSV 风格文本。"""


def parse_csv_line(line):
    """解析一行简单 CSV 日志，字段数量不是 5 个时返回 None。"""
    if not line:
        return None

    parts = [part.strip() for part in line.strip().split(",")]
    if len(parts) != 5:
        return None

    return {
        "time": parts[0],
        "ip": parts[1],
        "method": parts[2],
        "path": parts[3],
        "status": parts[4],
    }


def filter_by_status(lines, status_code):
    """过滤指定状态码的记录，自动跳过表头和坏行。"""
    records = []
    for line in lines:
        if not line or line.strip().lower().startswith("timestamp"):
            continue
        record = parse_csv_line(line)
        if record and record["status"] == str(status_code):
            records.append(record)
    return records


def format_as_table(records):
    """把记录列表格式化为一个简单表格字符串。"""
    header = "时间                  | IP           | 路径"
    separator = "----------------------|--------------|----------------"
    rows = [header, separator]

    for record in records:
        rows.append(
            " | ".join(
                [
                    record.get("time", "").ljust(20),
                    record.get("ip", "").ljust(12),
                    record.get("path", ""),
                ]
            )
        )

    return "\n".join(rows)
