# PyHelper - 你的命令行学习助手
# Week 02：根据心情推荐建议

DEFAULT_NAME = "同学"
DAILY_MESSAGE = "写代码就像搭积木，一块一块来。"

MOOD_ADVICE = {
    "开心": "太好了！趁状态好，挑战一道稍难的练习题。",
    "累": "先休息 5 分钟，再回来写 3 行代码。",
    "卡住": "把报错复制下来，只解决最上面的一条。",
    "紧张": "先跑通最小例子，再慢慢加功能。",
}

def build_welcome(name: str = DEFAULT_NAME) -> str:
    clean_name = name.strip() or DEFAULT_NAME
    return f"欢迎使用 PyHelper，{clean_name}！\n今日一句：{DAILY_MESSAGE}"

def advice_for_mood(mood: str) -> str:
    mood = mood.strip()
    for keyword, advice in MOOD_ADVICE.items():
        if keyword in mood:
            return advice
    return "不管现在什么心情，先完成一个 10 分钟小任务。"

def main() -> None:
    name = input("你的名字是？").strip() or DEFAULT_NAME
    mood = input("你今天学习状态如何？例如：开心/累/卡住/紧张：")
    print(build_welcome(name))
    print("学习建议：" + advice_for_mood(mood))

if __name__ == "__main__":
    main()
