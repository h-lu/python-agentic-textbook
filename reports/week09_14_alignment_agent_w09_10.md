# Week 09-10 Alignment Audit Report

## Scope

Audited and fixed only:

- `chapters/week_09`
- `chapters/week_10`
- `reports/week09_14_alignment_agent_w09_10.md`

Compared `CHAPTER.md`, `ASSIGNMENT.md`, `RUBRIC.md`, `QA_REPORT.md`, `ANCHORS.yml`, `TERMS.yml`, `examples/`, `starter_code/`, and `tests/` for stale paths, mismatched test references, promised APIs, broken examples, import pollution, and release validation consistency.

## Issues Found

1. Week 09 assignment validation commands referenced non-existent split test files:
   - `test_log_parser.py`
   - `test_csv_handler.py`
   - `test_pattern_matcher.py`
   - `test_log_analyzer.py`
   Actual tests live in `chapters/week_09/tests/test_week09.py`.

2. Week 09 rubric listed the same stale split test file names instead of the current `test_week09.py` contract tests.

3. Week 09 anchors referenced non-existent pytest classes/nodeids such as `TestStringMethods`, `TestSplitAndJoin`, and `TestRegularExpressions`. One PyHelper anchor also used a missing top-level `test_extract_tags` nodeid instead of the existing class-based tests.

4. Week 09 `examples/05_edge_cases.py` had a Python 3.11 syntax error: f-string expressions contained backslash escapes directly.

5. Week 10 chapter metadata referenced `examples/pyhelper/storage_json.py`, but the actual JSON storage example is `examples/pyhelper/storage.py`.

6. Week 10 assignment had a stale root-relative verification command for `practice2_data_exchange.py`; the current contract is tested through `chapters/week_10/tests/test_week10.py`.

7. Week 10 rubric showed stale pytest sample output (`12 passed`) while the current Week 10 test suite has 7 tests. The reviewer checklist also used root-relative `python3 practice*.py` commands that do not match the repository paths.

## Files Changed

- `chapters/week_09/ASSIGNMENT.md`
- `chapters/week_09/RUBRIC.md`
- `chapters/week_09/ANCHORS.yml`
- `chapters/week_09/examples/05_edge_cases.py`
- `chapters/week_10/CHAPTER.md`
- `chapters/week_10/ASSIGNMENT.md`
- `chapters/week_10/RUBRIC.md`
- `reports/week09_14_alignment_agent_w09_10.md`

## Commands Run

- `python3 scripts/validate_week.py --week 09 --mode release`
  - Blocked by sandbox: `pytest_rerunfailures` attempted to open a socket and raised `PermissionError`.
- `python3 scripts/validate_week.py --week 10 --mode release`
  - Blocked by the same sandbox/plugin issue.
- `python3 -m pytest chapters/week_09/tests chapters/week_10/tests -q`
  - Blocked by the same sandbox/plugin issue.
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/validate_week.py --week 09 --mode release`
  - Passed.
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/validate_week.py --week 10 --mode release`
  - Passed.
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest chapters/week_09/tests chapters/week_10/tests -q`
  - Passed: `13 passed`.
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest chapters/week_09/examples/pyhelper/tests -q`
  - Passed: `22 passed`.
- Targeted anchor/assignment nodeid checks for Week 09 and Week 10
  - Passed: `17 passed`.
- Ran all top-level example scripts under `chapters/week_09/examples/*.py` and `chapters/week_10/examples/*.py`
  - Passed after fixing `05_edge_cases.py`.
- `rg` checks for stale names: `test_log_parser`, `test_csv_handler`, `test_pattern_matcher`, `test_log_analyzer`, `TestStringMethods`, `TestSplitAndJoin`, `TestRegularExpressions`, `storage_json`, stale `test_extract_tags` nodeid
  - No stale references remained; remaining hits are current `test_week09.py` contract names.
- `git diff --check -- chapters/week_09 chapters/week_10 reports/week09_14_alignment_agent_w09_10.md`
  - Passed.

## Remaining Risks

- The exact requested pytest/validator commands cannot complete in this sandbox unless plugin autoload is disabled, because `pytest_rerunfailures` opens a socket during pytest configuration. The content and tests pass with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`.
- I did not edit shared glossary/concept files because the allowed scope was limited to Week 09, Week 10, and this report.

DONE
