"""成绩计算函数。"""


def total(scores):
    return sum(scores)


def average(scores):
    return sum(scores) / len(scores) if scores else 0


if __name__ == "__main__":
    sample = [80, 90, 100]
    print(f"总分：{total(sample)}")
    print(f"平均分：{average(sample):.1f}")
