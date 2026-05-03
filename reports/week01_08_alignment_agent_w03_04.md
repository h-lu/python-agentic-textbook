# Week 03-04 Assignment/Code/Test Alignment Report

Agent: W03-W04
Date: 2026-05-03

## Scope

Reviewed and fixed consistency for:
- `chapters/week_03/ASSIGNMENT.md`
- `chapters/week_03/starter_code/solution.py`
- `chapters/week_03/tests/`
- `chapters/week_04/ASSIGNMENT.md`
- `chapters/week_04/starter_code/solution.py`
- `chapters/week_04/tests/`

No files outside `chapters/week_03`, `chapters/week_04`, and this report were edited by this agent.

## Findings

1. Week 03 assignment named `rectangle_area(width, height)` and `rectangle_perimeter(width, height)`, but the starter solution did not include those functions.
2. Week 03 assignment did not clearly state where students should place code and the scope-analysis text answer.
3. Running week 03 and week 04 tests together caused pytest to import both `tests/conftest.py` files as the same `tests.conftest` package.
4. The environment has `pytest_rerunfailures` and `xdist` installed; the plugin attempted to open a local socket during pytest configuration, which is blocked in this sandbox.
5. Week 04 release validation required a `## 阻塞项` section in `QA_REPORT.md`; the report only had `## 学生视角阻塞项（已清零）`.
6. Week 04 assignment, starter code, and `test_assignment.py` were already aligned: tests import `chapters/week_04/starter_code/solution.py`, and the functions/edge cases match the assignment requirements.

## Changes

1. Added `chapters/week_03/__init__.py` and `chapters/week_04/__init__.py` so multi-week pytest runs import the test packages distinctly.
2. Patched week 03 and week 04 test `conftest.py` files to make `pytest_rerunfailures` use its no-op in-memory status DB in this socket-restricted environment.
3. Added Week 03 `rectangle_area()` and `rectangle_perimeter()` to `starter_code/solution.py`.
4. Added Week 03 assignment submission-path guidance:
   - code in `chapters/week_03/starter_code/solution.py`
   - scope explanation in `chapters/week_03/starter_code/scope_analysis.txt`
   - tests are concept/function validation and do not auto-grade the text answer
5. Added the required `## 阻塞项` section to Week 04 `QA_REPORT.md`.

## Verification

Passed:

```bash
python3 -m py_compile $(find chapters/week_03 chapters/week_04 -path '*/__pycache__' -prune -o -name '*.py' -print | sort)
```

```bash
python3 -m pytest chapters/week_03/tests chapters/week_04/tests -q
# 485 passed in 6.83s
```

```bash
python3 scripts/validate_week.py --week 03 --mode release
# [validate-week] OK: week_03 (mode=release)
```

```bash
python3 scripts/validate_week.py --week 04 --mode release
# [validate-week] OK: week_04 (mode=release)
```

## Unresolved Blockers

None for weeks 03-04.

Note: the worktree already contained unrelated modified/untracked files outside this agent's scope. They were not edited.
