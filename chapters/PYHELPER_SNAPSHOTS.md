# PyHelper 每周官方代码包索引

PyHelper 是全书贯穿项目。每周对应的官方快照统一放在：

```text
chapters/week_XX/pyhelper/
```

这些快照不是互相独立的小样例，而是**逐周增量演进**：每一周都继承上一周的完整可运行代码，再加入本周新能力。

| 周次 | 路径 | 继承关系 | 本周新增 |
|---|---|---|---|
| Week 01 | `chapters/week_01/pyhelper/` | 项目种子 | 欢迎语、名字输入、鼓励语 |
| Week 02 | `chapters/week_02/pyhelper/` | 继承 Week 01 | 心情判断与学习建议 |
| Week 03 | `chapters/week_03/pyhelper/` | 继承 Week 02 | 函数拆分与菜单 |
| Week 04 | `chapters/week_04/pyhelper/` | 继承 Week 03 | `list[dict]` 学习记录、查看和统计 |
| Week 05 | `chapters/week_05/pyhelper/` | 继承 Week 04 | `pyhelper_data.txt` 文本持久化 |
| Week 06 | `chapters/week_06/pyhelper/` | 继承 Week 05 | `try/except`、输入校验、坏数据容错 |
| Week 07 | `chapters/week_07/pyhelper/` | 继承 Week 06 | 拆成 `main/storage/input_handler/encouragement/records` 多模块 |
| Week 08 | `chapters/week_08/pyhelper/` | 继承 Week 07 | pytest 测试覆盖核心模块 |
| Week 09 | `chapters/week_09/pyhelper/` | 继承 Week 08 | 搜索、日期过滤、`#tag` 提取 |
| Week 10 | `chapters/week_10/pyhelper/` | 继承 Week 09 | JSON 存储、导入导出、旧文本迁移 |
| Week 11 | `chapters/week_11/pyhelper/` | 继承 Week 10 | dataclass 模型 `Note` / `StudyPlan` |
| Week 12 | `chapters/week_12/pyhelper/` | 继承 Week 11 | argparse CLI：`add/list/search/export/stats/advice` |
| Week 13 | `chapters/week_13/pyhelper/` | 继承 Week 12 | agent team 学习计划追踪，CLI 接入 `plan/review` |
| Week 14 | `chapters/week_14/pyhelper/` | 继承 Week 13 | v1.0 发布包、README、RELEASE_NOTES |

## 约定

- `starter_code/solution.py` 仍是每周作业/参考实现入口。
- `pyhelper/` 是贯穿项目官方快照，不替代作业入口。
- 每个 `pyhelper/README.md` 都说明“继承上周”和“本周新增”。
- 每周 README 的运行命令默认从对应的 `chapters/week_XX/pyhelper/` 目录执行。
- Week 01–04 不写入数据文件；Week 05 以后包含示例数据文件，运行时默认写入系统临时目录。需要固定数据文件时使用 `PYHELPER_DATA_FILE=/path/to/file`。
