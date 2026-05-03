"""Week 10 练习 3：日期对象序列化。"""

import datetime
import json


def date_serializer(obj):
    """把 date/datetime 转为 ISO 字符串。"""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError(f"{type(obj).__name__} is not JSON serializable")


def date_object_hook(data):
    """把常见日期字段从 ISO 字符串恢复为 date/datetime。"""
    result = data.copy()
    for key in ("date", "created_at"):
        value = result.get(key)
        if not isinstance(value, str):
            continue
        try:
            if "T" in value:
                result[key] = datetime.datetime.fromisoformat(value)
            else:
                result[key] = datetime.date.fromisoformat(value)
        except ValueError:
            pass
    return result


def serialize_event(event):
    """序列化包含日期的事件字典。"""
    return json.dumps(event, default=date_serializer, ensure_ascii=False)


def deserialize_event(json_text):
    """反序列化事件字典并恢复日期字段。"""
    return json.loads(json_text, object_hook=date_object_hook)
