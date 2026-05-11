try:
    from .encouragement import advice_for_mood, build_welcome
    from .input_handler import get_menu_choice
    from .records import add_record, list_records, search_records, stats
    from .storage import load_records, save_records
except ImportError:
    from encouragement import advice_for_mood, build_welcome
    from input_handler import get_menu_choice
    from records import add_record, list_records, search_records, stats
    from storage import load_records, save_records

def render_menu() -> str:
    return "\n1. 获取学习建议\n2. 新增学习记录\n3. 查看学习记录\n4. 搜索学习记录\n5. 查看统计\n6. 保存并退出"

def demo() -> str:
    records = load_records()
    add_record(records, "2026-05-13", "练习搜索 #python")
    found = search_records(records, "搜索")
    return "\n".join([build_welcome("同学"), advice_for_mood("卡住"), *list_records(found), stats(records)])

def main() -> None:
    name = input("你的名字是？").strip() or "同学"
    records = load_records()
    print(build_welcome(name))
    while True:
        print(render_menu())
        choice = get_menu_choice(input("请选择："), {"1", "2", "3", "4", "5", "6"})
        if choice == "1":
            print("学习建议：" + advice_for_mood(input("你今天学习状态如何？")))
        elif choice == "2":
            ok = add_record(records, input("日期 YYYY-MM-DD："), input("学习内容："))
            print("已记录。" if ok else "日期或内容不合法，未保存。")
        elif choice == "3":
            print("\n".join(list_records(records)) or "暂无记录。")
        elif choice == "4":
            print("\n".join(list_records(search_records(records, input("关键词：")))) or "没有匹配记录。")
        elif choice == "5":
            print(stats(records))
        elif choice == "6":
            save_records(records)
            print("已保存，下次见！")
            break
        else:
            print("请输入 1-6。")

if __name__ == "__main__":
    print(demo())
