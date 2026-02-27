"""Smoke tests for package importability."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def test_import_main_module() -> None:
    from pah_workbench import main

    assert hasattr(main, "main")
