DEFAULT_NAME = "同学"
DAILY_MESSAGE = "写代码就像搭积木，一块一块来。"
MOOD_ADVICE = {
    "开心": "太好了！趁状态好，挑战一道稍难的练习题。",
    "累": "先休息 5 分钟，再回来写 3 行代码。",
    "卡住": "把报错复制下来，只解决最上面的一条。",
    "紧张": "先跑通最小例子，再慢慢加功能。",
}

def build_welcome(name: str = DEFAULT_NAME) -> str:
    return f"欢迎使用 PyHelper，{(name.strip() or DEFAULT_NAME)}！\n今日一句：{DAILY_MESSAGE}"

def advice_for_mood(mood: str) -> str:
    for keyword, advice in MOOD_ADVICE.items():
        if keyword in mood.strip():
            return advice
    return "不管现在什么心情，先完成一个 10 分钟小任务。"
