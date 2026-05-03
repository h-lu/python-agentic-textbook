# Week 07-08 Assignment/Code/Test Alignment Report

Agent: W07-W08

Scope:
- `chapters/week_07`
- `chapters/week_08`
- `reports/week01_08_alignment_agent_w07_08.md`

## Findings

1. Week 07 `ASSIGNMENT.md` says `starter_code/todo_list.py` is provided for the single-file refactoring exercise, but the file was missing.
2. Week 08 `tests/test_week08_concepts.py` imported `todo_manager` after adding `examples/` to `sys.path`. That passed in the full suite only when another test had already imported `starter_code/todo_manager.py`; the test failed when run by itself.
3. Week 08 `ASSIGNMENT.md` described the Todo Manager test file and implementation file with ambiguous or stale paths in several places.

## Changes

1. Added `chapters/week_07/starter_code/todo_list.py` as the promised single-file Todo List starter for the Week 07 refactoring exercise.
2. Updated `chapters/week_08/tests/test_week08_concepts.py` so `todo_manager` is imported from `chapters/week_08/starter_code`, matching the other Week 08 tests and the assignment.
3. Clarified Week 08 assignment paths:
   - Test file: `chapters/week_08/tests/test_todo_manager.py`
   - Tested implementation: `chapters/week_08/starter_code/todo_manager.py`
   - TDD notes: `chapters/week_08/TDD_NOTES.md`
   - Git add examples now use the same paths.

No files were removed. `__pycache__` directories were not touched.

## Verification

Passed:

```bash
python3 -m py_compile $(find chapters/week_07 chapters/week_08 -name '*.py' -not -path '*/__pycache__/*')
```

Passed with pytest third-party plugin autoload disabled:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest chapters/week_08/tests/test_week08_concepts.py -q
# 34 passed, 1 xfailed, 1 xpassed

PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest chapters/week_07/tests chapters/week_08/tests -q
# 243 passed, 1 xfailed, 1 xpassed

PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/validate_week.py --week 07 --mode release
# [validate-week] OK: week_07 (mode=release)

PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/validate_week.py --week 08 --mode release
# [validate-week] OK: week_08 (mode=release)
```

The raw requested pytest/validate commands were also run, but they fail in this sandbox before test collection because `pytest_rerunfailures` attempts to create a socket:

```text
PermissionError: [Errno 1] Operation not permitted
```

Affected raw commands:

```bash
python3 -m pytest chapters/week_07/tests chapters/week_08/tests -q
python3 scripts/validate_week.py --week 07 --mode release
python3 scripts/validate_week.py --week 08 --mode release
```

## Unresolved Blockers

No repository-level consistency blockers remain for weeks 07-08. The only unresolved verification blocker is environmental: the active pytest plugin set opens a socket that is denied by the current sandbox. Disabling third-party plugin autoload verifies the code and release gates successfully.
