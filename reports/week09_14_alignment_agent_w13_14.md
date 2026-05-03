# Week 13-14 Alignment Audit Report

## Scope

- Audited only `chapters/week_13/` and `chapters/week_14/`.
- Compared student-facing chapter, assignment, rubric, QA, anchors, terms, examples, starter code, and tests for stale paths, promised APIs, import/test issues, broken examples, and release validation mismatches.
- Edited only `chapters/week_13/`, `chapters/week_14/`, and this report.

## Issues Found

1. Week 13 assignment referenced removed starter files:
   - `starter_code/agent_basic.py`
   - `starter_code/agent_reviewer.py`
   - `starter_code/agent_team.py`
   The actual shipped starter surface is `starter_code/solution.py` plus focused pytest modules.

2. Week 13 rubric referenced stale test modules:
   - `test_basic.py`
   - `test_reviewer.py`
   - `test_agent_team.py`
   These do not exist; the current tests are `test_reader_agent.py`, `test_writer_agent.py`, `test_reviewer_agent.py`, and `test_iteration.py`.

3. Week 13 assignment/rubric described `ReviewerAgent.review_plan()` as returning `ReviewResult`, but the starter solution and tests use `List[str]` for plan review issues. `ReviewResult` remains a valid generic dataclass, but not the direct return value for `review_plan()`.

4. Week 13 student-facing snippets omitted required `StudyPlan` fields (`topics`, `estimated_hours`) now required by the starter solution/tests.

5. Week 13 chapter metadata and an example import snippet referenced stale/nonexistent example module names.

6. Week 13 test skip reason had a typo: `尚尚不实现`.

7. Week 14 final PyHelper example failed before showing `--help` in this sandbox because logging opened `~/.pyhelper/pyhelper.log` under a read-only home directory.

8. Week 14 starter task manager did not create its data directory before saving tasks, so the documented CLI `add` flow could fail on a fresh machine.

## Files Changed

- `chapters/week_13/ASSIGNMENT.md`
- `chapters/week_13/CHAPTER.md`
- `chapters/week_13/RUBRIC.md`
- `chapters/week_13/examples/13_pyhelper_agent_team.py`
- `chapters/week_13/tests/test_iteration.py`
- `chapters/week_14/examples/14_pyhelper_v1.py`
- `chapters/week_14/starter_code/solution.py`
- `reports/week09_14_alignment_agent_w13_14.md`

## Commands Run

- `find chapters/week_13 chapters/week_14 -maxdepth 3 -type f | sort`
- `sed -n '1,620p' scripts/validate_week.py`
- `find chapters/week_13 chapters/week_14 -path '*/__pycache__' -prune -o -type f -print | sort | xargs rg ...`
- `find chapters/week_13 chapters/week_14 -path '*/__pycache__' -prune -o -type f -name '*.py' -print | sort | xargs -r python3 -m py_compile`
- `python3 scripts/validate_week.py --week 13 --mode release`
- `python3 scripts/validate_week.py --week 14 --mode release`
- `python3 -m pytest chapters/week_13/tests chapters/week_14/tests -q`
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/validate_week.py --week 13 --mode release`
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/validate_week.py --week 14 --mode release`
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest chapters/week_13/tests chapters/week_14/tests -q`
- `python3 chapters/week_13/examples/13_pyhelper_agent_team.py`
- `python3 chapters/week_13/examples/03_full_agent_team.py`
- `python3 chapters/week_14/examples/14_pyhelper_v1.py --help`
- `python3 chapters/week_14/examples/14_pyhelper_v1.py add "今天学了代码收敛" --tags Python 工程化`
- `python3 chapters/week_14/examples/14_pyhelper_v1.py list`
- `TASKMGR_HOME=/tmp/week14_taskmgr_test python3 chapters/week_14/starter_code/solution.py add "测试任务"`
- `TASKMGR_HOME=/tmp/week14_taskmgr_test python3 chapters/week_14/starter_code/solution.py list --all`

## Verification Results

- Raw pytest/validate commands without environment overrides were blocked by the sandbox because the installed `pytest_rerunfailures` plugin attempted to open a socket and raised `PermissionError: [Errno 1] Operation not permitted`.
- With `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`:
  - `validate_week.py --week 13 --mode release`: passed
  - `validate_week.py --week 14 --mode release`: passed
  - combined Week 13/14 pytest: `251 passed`
- Targeted examples now run:
  - Week 13 `03_full_agent_team.py`: passed
  - Week 13 `13_pyhelper_agent_team.py`: passed
  - Week 14 `14_pyhelper_v1.py --help/add/list`: passed
  - Week 14 starter `solution.py add/list`: passed with `TASKMGR_HOME=/tmp/week14_taskmgr_test`

## Remaining Risks

- Week 14 assignment/rubric validation commands intentionally use `python3 -m pytest tests/ -v` because they refer to the student's own capstone project, not the textbook repo path.
- The repository environment's auto-loaded pytest plugin remains incompatible with the sandbox socket policy; this is not a Week 13/14 content issue.

DONE
