# W05-W06 Assignment/Code/Test Alignment Report

## Scope

- Inspected and edited only:
  - `chapters/week_05/ASSIGNMENT.md`
  - `chapters/week_05/starter_code/solution.py`
  - `chapters/week_06/ASSIGNMENT.md`
  - `chapters/week_06/starter_code/solution.py`
  - `reports/week01_08_alignment_agent_w05_06.md`
- Did not edit git config, root config files, other week directories, tests, or `__pycache__`.

## Findings

### Week 05

- `ASSIGNMENT.md` described a persistent account book (`accountbook.py`, `accountbook.txt`), but the existing starter code, examples, and tests are centered on file I/O, learning records, PyHelper persistence, and a diary-style app.
- `starter_code/solution.py` implemented a learning-record tool with `records.txt`, but did not expose the diary helper function names documented by `tests/test_diary_app.py`.

### Week 06

- `ASSIGNMENT.md` referenced non-existent test files such as `chapters/week_06/tests/test_basic_q1_safe_divider.py` and `chapters/week_06/tests/test_ai_collaboration.py`.
- The assignment asked for `get_positive_integer()`, `get_age()`, and `get_menu_choice()`, but `starter_code/solution.py` did not expose those interfaces.
- The actual automated tests import from `chapters/week_06/starter_code/solution.py` and primarily run `test_smoke.py` and `test_week06.py`.

## Changes

### Week 05

- Rewrote `ASSIGNMENT.md` to align with the existing week theme: persistent learning diary / learning records.
- Stated the relevant test files and starter path clearly.
- Replaced obsolete account-book paths with `chapters/week_05/starter_code/solution.py`, `records.txt`, and diary/PyHelper examples.
- Added diary helper APIs to `starter_code/solution.py`:
  - `add_diary_entry`
  - `read_all_diaries`
  - `search_diaries`
  - `count_diaries`

### Week 06

- Updated `ASSIGNMENT.md` to point students at `chapters/week_06/starter_code/solution.py` and the real test suite.
- Replaced the optional AI collaboration submission path with `chapters/week_06/ai_review.md`.
- Clarified the PyHelper path as `chapters/week_06/examples/06_pyhelper.py`.
- Added assignment-facing interfaces to `starter_code/solution.py`:
  - `get_positive_integer`
  - `get_age`
  - `get_menu_choice`
- Adjusted `get_positive_integer_with_retry()` messages so zero and negative integer input get the "大于 0" feedback path.

## Verification

- `python3 -m py_compile $(rg --files chapters/week_05 chapters/week_06 -g '*.py' | sort)`  
  Result: passed.

- `python3 -m pytest chapters/week_05/tests chapters/week_06/tests -q`  
  Result: blocked before collection by installed `pytest_rerunfailures`, which attempts to create a socket and fails in this sandbox with `PermissionError: [Errno 1] Operation not permitted`.

- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest chapters/week_05/tests chapters/week_06/tests -q`  
  Result: `241 passed in 1.01s`.

- `python3 scripts/validate_week.py --week 05 --mode release`  
  Result: blocked by the same `pytest_rerunfailures` socket permission error.

- `python3 scripts/validate_week.py --week 06 --mode release`  
  Result: blocked by the same `pytest_rerunfailures` socket permission error.

- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/validate_week.py --week 05 --mode release`  
  Result: `[validate-week] OK: week_05 (mode=release)`.

- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 scripts/validate_week.py --week 06 --mode release`  
  Result: `[validate-week] OK: week_06 (mode=release)`.

## Unresolved Blockers

- The code and week packages validate when third-party pytest plugin autoload is disabled.
- The exact plain pytest/validate commands are still blocked in this sandbox by the globally installed `pytest_rerunfailures` plugin opening a socket. I did not change root pytest configuration or environment files because those paths are outside this task's edit constraints.
