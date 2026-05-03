# Week 11-12 Alignment Audit Report

## Scope

Audited only:
- `chapters/week_11/`
- `chapters/week_12/`
- `reports/week09_14_alignment_agent_w11_12.md`

Compared student-facing chapter, assignment, rubric, QA, anchors, examples, starter code, and tests for stale paths, promised APIs, import pollution, validation readiness, and broken examples.

## Issues Found

- Week 11 anchors referenced deleted split test files such as `tests/test_state.py`, `tests/test_json_conversion.py`, and `tests/test_dataclass.py`.
- Week 11 test coverage docs and QA/rubric output still described an older 88-test / 12-pass suite, while the current contract suite is `test_week11.py` with 7 tests.
- Week 11 assignment had a bare `python3 practice2_type_hints.py` command that was ambiguous from repo root.
- Week 11 chapter had a stale illustrative test filename, `tests/test_task_state.py`.
- Week 12 chapter code-block filenames referenced old example names that no longer exist; current files are `01_simple_argparse.py` through `06_logging.py`.
- Week 12 anchors used stale or cwd-dependent commands, including `python task.py --help` and `python examples/pyhelper/cli.py --help`.
- Week 12 test README and summary described an obsolete 195-test todo-cli suite with known failures, while current tests are 7 habit-cli contract tests.
- Week 12 examples README referenced missing `tests/test_examples.py`.
- Week 12 reference solution promised logging-module behavior in assignment/rubric but wrote log lines manually.
- Week 12 PyHelper CLI example failed in this sandbox because it tried to write logs under read-only `/root/.pyhelper`.

## Files Changed

- `chapters/week_11/ANCHORS.yml`
- `chapters/week_11/ASSIGNMENT.md`
- `chapters/week_11/CHAPTER.md`
- `chapters/week_11/QA_REPORT.md`
- `chapters/week_11/RUBRIC.md`
- `chapters/week_11/tests/TEST_COVERAGE.md`
- `chapters/week_12/ANCHORS.yml`
- `chapters/week_12/CHAPTER.md`
- `chapters/week_12/QA_REPORT.md`
- `chapters/week_12/examples/README.md`
- `chapters/week_12/examples/pyhelper/cli.py`
- `chapters/week_12/starter_code/solution.py`
- `chapters/week_12/tests/README.md`
- `chapters/week_12/tests/TEST_SUMMARY.md`

## Commands Run

Exact requested commands:
- `python3 scripts/validate_week.py --week 11 --mode release` failed before tests loaded because `pytest_rerunfailures` tried to open a socket and hit `PermissionError: [Errno 1] Operation not permitted`.
- `python3 scripts/validate_week.py --week 12 --mode release` failed for the same sandbox/plugin reason.
- `python3 -m pytest chapters/week_11/tests chapters/week_12/tests -q` failed for the same sandbox/plugin reason.

Content verification with plugin autoload disabled:
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/validate_week.py --week 11 --mode release` passed.
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/validate_week.py --week 12 --mode release` passed.
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest chapters/week_11/tests chapters/week_12/tests -q` passed: `14 passed`.
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest chapters/week_12/tests chapters/week_11/tests -q` passed: `14 passed`.
- `python3 -m compileall -q chapters/week_11/starter_code chapters/week_11/examples chapters/week_12/starter_code chapters/week_12/examples` passed.

Example spot checks:
- `python3 chapters/week_12/examples/01_simple_argparse.py --help` passed.
- `python3 chapters/week_12/examples/04_subcommands.py add "任务"` passed.
- `python3 -m chapters.week_12.examples.pyhelper.cli --help` passed after the data-dir fallback fix.

## Remaining Risks

- The exact requested pytest/validate commands remain blocked in this sandbox by the globally installed `pytest_rerunfailures` plugin attempting socket creation. The week content passes when plugin autoload is disabled.
- Other weeks and reports already had unrelated edits in the worktree; they were not inspected or modified.

DONE
