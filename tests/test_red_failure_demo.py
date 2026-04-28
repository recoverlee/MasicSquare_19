"""Optional RED demo: run only when env MAGICSQUARE_DEMO_RED=1 to see pytest FAIL output."""

from __future__ import annotations

import os

import pytest

@pytest.mark.skipif(
    os.environ.get("MAGICSQUARE_DEMO_RED") != "1",
    reason="Set MAGICSQUARE_DEMO_RED=1 to run intentional failure (traceback + exit code 1).",
)
def test_demo_red_phase_expected_failure_shows_in_pytest() -> None:
    """Deliberate failure so `pytest -v --tb=short` prints FAILED and traceback."""
    assert False, "RED: replace this with a real failing assertion during TDD."
