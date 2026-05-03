"""
Week 02 作业参考实现

本文件是 Starter Code 的参考答案，供学生在遇到困难时查看。
实现了基础作业要求，并额外演示进阶作业中的难度选择和输入验证。

注意：这只是一个参考实现，不是唯一正确的答案。
编程有多种正确的写法，鼓励学生探索自己的实现方式。

运行方式：python3 chapters/week_02/starter_code/solution.py
"""

import random


def get_difficulty():
    """
    获取用户选择的难度

    返回: (max_num, max_attempts) 元组
        - max_num: 数字范围上限
        - max_attempts: 最大尝试次数
    """
    print("=== 猜数字游戏 ===")
    print("选择难度：")
    print("1. 简单（1-50，最多 7 次）")
    print("2. 中等（1-100，最多 5 次）")
    print("3. 困难（1-200，最多 5 次）")

    while True:
        difficulty = input("请输入难度（1-3）：")

        if difficulty == "1":
            return 50, 7
        elif difficulty == "2":
            return 100, 5
        elif difficulty == "3":
            return 200, 5
        else:
            print("无效输入，请选择 1、2 或 3")


def play_game(max_num, max_attempts):
    """
    进行猜数字游戏

    参数:
        max_num: 数字范围上限
        max_attempts: 最大尝试次数
    """
    secret = random.randint(1, max_num)
    print(f"\n我想好了一个 1 到 {max_num} 之间的数字，")
    print(f"你有 {max_attempts} 次机会猜中它！")

    for attempt in range(max_attempts):
        print()
        guess = get_guess(attempt + 1, max_num)

        if guess == secret:
            print(f"恭喜！你用了 {attempt + 1} 次猜中了答案 {secret}！")
            return

        # 给出提示
        if guess < secret:
            print("太小了")
        else:
            print("太大了")

        # 显示剩余次数
        remaining = max_attempts - attempt - 1
        if remaining > 0:
            print(f"还有 {remaining} 次机会")

    # 循环正常结束（没猜中）
    print(f"\n很遗憾，{max_attempts} 次都用完了。答案是 {secret}")


def get_guess(attempt_num, max_num):
    """
    获取用户输入的猜测数字

    参数:
        attempt_num: 当前是第几次尝试
        max_num: 数字范围上限

    返回: 用户猜测的数字（整数）
    """
    while True:
        try:
            guess = int(input(f"第 {attempt_num} 次猜测（1-{max_num}）："))
            if 1 <= guess <= max_num:
                return guess
            print(f"请输入 1 到 {max_num} 之间的数字")
        except ValueError:
            print("无效输入，请输入一个数字")


def main():
    """主函数"""
    max_num, max_attempts = get_difficulty()
    play_game(max_num, max_attempts)

    # 询问是否再来一局
    print()
    play_again = input("再玩一次？（y/n）：").lower()
    if play_again == "y" or play_again == "yes":
        print()
        main()


if __name__ == "__main__":
    main()


# --- 实现说明 ---
#
# 本实现包含以下特点：
#
# 1. 输入验证：
#    - 难度选择：防止输入非 1/2/3 的值
#    - 猜测数字：防止输入非数字或超出范围的值
#
# 2. 代码结构：
#    - 使用函数分割不同功能（虽然 Week 02 还没正式讲函数，
#      但这是良好的编程实践）
#    - 主逻辑清晰：选择难度 -> 进行游戏 -> 询问是否重玩
#
# 3. 用户体验：
#    - 清晰的提示信息
#    - 剩余次数提示
#    - 支持多轮游戏
#
# 4. 错误处理：
#    - 使用 try/except 处理非数字输入
#    - 范围检查确保数字在有效区间内
#
# --- 与作业要求的对应 ---
#
# 基础作业（必做）：
# ✅ 完整的猜数字游戏
# ✅ 限制猜测次数
# ✅ 给出"大了"/"小了"的提示
# ✅ 显示剩余次数
#
# 进阶作业（可选）：
# ✅ 难度选择（简单/中等/困难）
# ✅ 输入验证（防止非法输入）
# ✅ 多轮游戏（玩完一局可以再玩）
# ✅ 使用函数组织代码
#
# 挑战作业（可选）：
# ⚠️ 计时功能（未实现，可作为扩展）
# ⚠️ 历史记录（未实现，可作为扩展）
