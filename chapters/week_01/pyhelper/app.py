# PyHelper - 你的命令行学习助手
# Week 01：第一颗种子

DEFAULT_NAME = "同学"
DAILY_MESSAGE = "写代码就像搭积木，一块一块来。"

def build_welcome(name: str = DEFAULT_NAME) -> str:
    clean_name = name.strip() or DEFAULT_NAME
    return f"欢迎使用 PyHelper，{clean_name}！\n今日一句：{DAILY_MESSAGE}"

def main() -> None:
    name = input("你的名字是？").strip() or DEFAULT_NAME
    print(build_welcome(name))

if __name__ == "__main__":
    main()
