"""
示例：遍历列表和字典，计算统计信息。

本例演示如何用 for 循环遍历列表和字典，找出最高分、统计及格人数、生成成绩单。

运行方式：python3 chapters/week_04/examples/05_grade_statistics.py
预期输出：演示遍历模式、enumerate、items()、统计计算
"""

# ========== 遍历列表 ==========

print("=== 遍历列表 ===")

scores = [85, 92, 78, 90, 88]

# 方式1：直接遍历元素
print("遍历每个成绩：")
for score in scores:
    print(f"  成绩：{score}")

# 方式2：用 enumerate() 同时获取索引和元素
print("\n遍历带索引：")
for index, score in enumerate(scores):
    print(f"  第 {index + 1} 个成绩：{score}")

# ========== 遍历字典 ==========

print("\n=== 遍历字典 ===")

scores = {
    "小北": 85,
    "阿码": 92,
    "老潘": 78,
    "小红": 90,
    "小明": 88
}

# 遍历键（默认）
print("遍历键：")
for name in scores:
    print(f"  {name}")

# 遍历值
print("\n遍历值：")
for score in scores.values():
    print(f"  {score}")

# 遍历键值对
print("\n遍历键值对：")
for name, score in scores.items():
    print(f"  {name}: {score}")

# ========== 找出最高分（手动遍历） ==========

print("\n=== 找出最高分 ===")

scores = {"小北": 85, "阿码": 92, "老潘": 78, "小红": 90, "小明": 88}

max_score = None
max_name = None

for name, score in scores.items():
    if max_score is None or score > max_score:
        max_score = score
        max_name = name

print(f"最高分：{max_name}，{max_score} 分")

# ========== 找出最高分（用内置函数） ==========

print("\n=== 用内置函数找最高分 ===")

max_score = max(scores.values())
print(f"最高分：{max_score}")

# 找出最高分是谁
max_name = max(scores, key=scores.get)
print(f"最高分是：{max_name}，{scores[max_name]} 分")

# ========== 统计及格人数 ==========

print("\n=== 统计及格人数 ===")

scores = {"小北": 85, "阿码": 92, "老潘": 78, "小红": 90, "小明": 88}

pass_count = 0
fail_count = 0

for score in scores.values():
    if score >= 60:
        pass_count += 1
    else:
        fail_count += 1

print(f"及格：{pass_count} 人")
print(f"不及格：{fail_count} 人")

# ========== 生成成绩单 ==========

print("\n=== 生成成绩单 ===")

scores = {"小北": 85, "阿码": 92, "老潘": 78, "小红": 90, "小明": 88}

print("=== 成绩单 ===")

for name, score in scores.items():
    # 根据分数判断等级
    if score >= 90:
        level = "优秀"
    elif score >= 80:
        level = "良好"
    elif score >= 60:
        level = "及格"
    else:
        level = "不及格"

    print(f"{name}: {score} ({level})")

# ========== 按分数排序（不使用字典排序） ==========

print("\n=== 按分数排序（转换为列表） ===")

scores = {"小北": 85, "阿码": 92, "老潘": 78, "小红": 90, "小明": 88}

# 将字典转换为列表，然后排序
score_list = [(name, score) for name, score in scores.items()]  # 列表推导式（高级写法，week_09 会详细讲）
score_list.sort(key=lambda x: x[1], reverse=True)  # 按分数降序；lambda 是高级写法（week_09 会详细讲解）

print("=== 成绩排名 ===")
for i, (name, score) in enumerate(score_list):
    print(f"第 {i+1} 名：{name}，{score} 分")

# ========== 数据驱动设计的威力 ==========

print("\n=== 数据驱动设计 ===")

print("添加一个新学生，代码不需要修改：")
scores["小李"] = 87

print(f"\n现在有 {len(scores)} 个学生")
print("遍历代码不需要改，自动处理新数据！")
