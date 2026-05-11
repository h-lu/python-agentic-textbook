# PR1-PR5 Audit Backlog

本文件按当前可见审计范围重建。原多 Agent 审计报告未随任务提供，因此本轮以用户给定 PR1-PR5 定义、仓库现状、校验脚本和 Week 01-14 交付物为准收口。

## PR1：事实 / 技术正确性 / 术语 / 示例

- [x] 检查 `README.md`、`scripts/validate_book.py`、`scripts/validate_week.py`、`chapters/SYLLABUS.md`、`chapters/TOC.md` 与 Week 01-14 章包结构。
- [x] 弱化 Week 01、02、03、04、05、06、08、09、10、11、12、13、14 中无法在当前上下文核验的动态统计数字、价格、用户数、效率提升百分比和预测数据。
- [x] 将 AlphaGeometry、Copilot、AI 生成代码、TDD、API、CLI、agent 等段落改为稳定趋势表述，避免把单一报告或营销口径当成教材事实。
- [x] 保留 Python 语法、pytest、JSON、dataclass、argparse、异常处理等稳定技术点的正文示例，不做大重写。

## PR2：PyHelper / 贯穿项目连续性 / 跨周一致性

- [x] 检查 `chapters/PYHELPER_SNAPSHOTS.md` 与 `shared/book_project.md` 的 Week 01-14 PyHelper 演进路径。
- [x] 确认每周 `CHAPTER.md` 仍包含 `## PyHelper 进度`，且 `validate_week.py --mode release` 会继续检查 PyHelper 提及。
- [x] 本轮未改动 `chapters/week_*/pyhelper/` 代码；无需新增 PyHelper 专项测试。
- [x] 未发现需要重写 PyHelper 线索的断点；本轮只修正文和验收材料一致性。

## PR3：新手认知负荷 / 最低线 / 分层

- [x] 保持作业分层结构，不把进阶 / 挑战项提升为必做项。
- [x] 对测试文档中夸大的测试数量和固定通过输出做收敛，避免学生被不一致的数量误导。
- [x] 动态事实段落从数字堆叠改为趋势说明，降低章首导入和 AI 小专栏的外部信息负荷。

## PR4：AI 时代小专栏 / 动态事实 / FACT_CHECK

- [x] 对无法在当前上下文核验的数据统一弱化为趋势表述。
- [x] 更新 `FACT_CHECK.md`：记录本轮已处理范围、保留的动态风险和后续出版前复核要求。
- [x] 不新增未经搜索工具或研究缓存确认的新 URL、统计数字或行业报告。

## PR5：作业 / 测试 / Rubric / Release 验收材料

- [x] 核对 Week 01-14 `ASSIGNMENT.md` / `RUBRIC.md` / tests docs 中的 pytest 命令形态。
- [x] 修正 Week 02、03、05、07、08 测试文档或评分标准中的明显过期测试数量 / 通过输出。
- [x] 保持命令以项目根目录可运行的 `python3 -m pytest chapters/week_XX/tests -q` 为主；子目录命令保留时明确目录。
- [x] 加固 `scripts/validate_week.py` 的 pytest 子进程，默认禁用外部 pytest 插件自动加载，避免全局插件在沙箱或课堂环境中污染 release 校验。
- [x] 运行 `python3 scripts/validate_book.py` 和 Week 01-14 release 校验作为最终验收。

## 本轮遗留风险

- 现有章节仍保留历史参考链接；本轮未联网逐条验证 URL 内容，只移除了正文中依赖这些链接的硬数字结论。出版前仍应按 `FACT_CHECK.md` 逐条复核。
- 部分测试说明文档包含教学性覆盖矩阵，矩阵按主题归类，可能与 pytest 采集数量不是一一映射；验收以实际 pytest 输出为准。
