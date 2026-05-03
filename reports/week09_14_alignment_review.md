# Week 09–14 Alignment Review

Date: 2026-05-03
Repo HEAD before changes: `3d77a7d`
Scope: Codex-generated alignment changes for `chapters/week_09` through `chapters/week_14`.

## Verdict

**Conservative pass, with cleanup caveats before commit.**

The previous critical problems are materially addressed:

- Week 09 tests no longer define answer functions inline; they import real `starter_code` modules.
- Week 10 `starter_code/solution.py` no longer has the `\uXXXX` unicode-escape `SyntaxError`; assignment practice files now exist.
- Week 11 now follows the assignment's `Student` / `Enrollment` / `Book` contract instead of the old Task/Note contract, and the named practice files now exist.
- Week 12 now implements habit-cli rather than todo-cli, with a real `habit.py` entry wrapper and non-skipping tests.
- Week 13 assignment test references were updated to actual test filenames.
- Week 14 gained realistic local deliverable validation helpers instead of requiring real push/release operations.
- `make test W=09` octal parsing bug is fixed.

## Verification run

Commands run after freezing the stuck Codex tmux process:

```bash
python3 -m py_compile chapters/week_{09..14}/starter_code/*.py
python3 -m pytest chapters/week_09/tests chapters/week_10/tests chapters/week_11/tests chapters/week_12/tests chapters/week_13/tests chapters/week_14/tests -q
for W in 09 10 11 12 13 14; do make test W="$W"; done
for W in week_09 week_10 week_11 week_12 week_13 week_14; do python3 scripts/validate_week.py --week "$W" --mode release; done
```

Results:

- `py_compile`: **27 files compiled**
- Combined pytest before cleanup: **278 passed in 1.75s**
- Combined pytest after Week 12 `conftest.py` cleanup: **278 passed in 0.70s**
- `make test W=09..14`: all passed
  - Week 09: 6 passed
  - Week 10: 7 passed
  - Week 11: 7 passed
  - Week 12: 7 passed
  - Week 13: 116 passed
  - Week 14: 135 passed
- `validate_week --mode release`: all Week 09–14 OK

## Audit notes by week

### Week 09

Good:
- Assignment-referenced files now exist: `log_parser.py`, `csv_handler.py`, `pattern_matcher.py`, `log_analyzer.py`, `url_parser.py`, `safe_reader.py`.
- Tests import these modules directly and cover positive/negative/edge cases.

Caveat:
- Test count is intentionally small after deleting false-positive concept tests. That is acceptable for release gating, but future expansion should add per-file tests (`test_log_parser.py`, etc.) if this chapter needs stronger student-facing grading.

### Week 10

Good:
- The syntax error is fixed by replacing the old monolithic solution with importable practice modules.
- Practice files and `student_manager_fixed.py` exist under `starter_code` and tests exercise each one.

Caveat:
- `ASSIGNMENT.md` originally said “创建文件 `practice*.py`” without explicitly saying `starter_code/practice*.py`; I clarified this before PR.

### Week 11

Good:
- The main contract now matches the assignment: `Student`, type-hint functions, `EnrollmentStatus`, `Enrollment`, JSON-convertible `Task`, `Book`, library fix.
- Second pass added the missing named practice files and `library_system_fixed.py`.

Caveat:
- The practice files mostly re-export from `solution.py`. This is okay for reference release artifacts, but not ideal if these are meant to be starter blanks for students.

### Week 12

Good:
- The implementation is now habit-cli, not todo-cli.
- `starter_code/habit.py` provides a real assignment-facing entry point around `solution.py`.
- Tests use temp data/log paths and do not write user/project state.
- No skip-on-missing-solution behavior remains.

Caveats:
- `ASSIGNMENT.md` originally spoke in terms of `habit.py`, `habits.json`, and `habit.log` without clarifying repo/runtime locations; I clarified `starter_code/habit.py` and runtime-generated data/log artifacts before PR.
- `--verbose` is parsed but not meaningfully implemented beyond being accepted. Because it is under the optional challenge section, this is not blocking.
- `tests/conftest.py` originally contained old todo-oriented fixtures; I cleaned it after audit and reran Week 12 + combined tests.

### Week 13

Good:
- Assignment references are now aligned to actual tests.
- `tests/conftest.py` path now points to `../starter_code`.

Caveat:
- Existing Week 13 tests still contain many `pytest.skip` references around missing/incomplete solution paths. This predates the current alignment work and did not hide Week 09–12 failures, but it is worth reviewing separately if Week 13 is used as a strict grading artifact.

### Week 14

Good:
- New `validate_sample_deliverable` style helpers give tests something realistic to check without requiring real GitHub release/push.

Caveat:
- Existing concept tests still define local helper functions in test files. That is less harmful here because they are testing concepts/templates, but only the new `test_deliverable_validation.py` really verifies `starter_code/solution.py` deliverable helpers.

## Project-level notes

- `pytest.ini` adds `--import-mode=importlib`, which is needed because multiple week folders contain same-named tests such as `test_smoke.py`. A diagnostic run without this option failed on pytest import-file mismatch.
- `.pct-state.json` is an untracked tmux helper artifact. Do **not** commit it.
- Codex second pass got stuck in tmux after producing changes; I stopped it with Ctrl-C before this audit to avoid concurrent writes.

## Recommended pre-commit cleanup

1. Exclude `.pct-state.json` from commit.

After the documentation clarification and Week 12 conftest cleanup, I am comfortable committing this as an alignment fix. Keep `.pct-state.json` out of the commit.
