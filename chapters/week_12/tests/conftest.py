"""Week 12 pytest configuration.

The Week 12 assignment is habit-cli.  The real contract tests create isolated
`habits.json` / `habit.log` paths with monkeypatching inside
`test_week12_habit_cli.py`, so this file only provides import-path hygiene.
"""

import os
import sys


# Add starter_code to import path for `import habit` / `import solution`.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "starter_code"))
sys.modules.pop("solution", None)
sys.modules.pop("habit", None)
