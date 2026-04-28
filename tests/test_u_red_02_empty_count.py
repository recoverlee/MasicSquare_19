"""U-RED-02 / TC-MS-D-007 — exactly two empty cells (RED until GREEN implements counting)."""

from __future__ import annotations

import pytest

from magicsquare.boundary import validate_empty_cell_count
from magicsquare.constants import EMPTY_CELL, MATRIX_SIZE, MSG_EMPTY_COUNT


def _full_grid_without_zeros() -> list[list[int]]:
    """16 distinct values 1..16 (no zeros)."""
    values = list(range(1, MATRIX_SIZE * MATRIX_SIZE + 1))
    return [values[r * MATRIX_SIZE : (r + 1) * MATRIX_SIZE] for r in range(MATRIX_SIZE)]


def test_u_red_02_raises_when_no_empty_cells() -> None:
    """Zero blanks → EMPTY_COUNT (PRD)."""
    matrix = _full_grid_without_zeros()
    with pytest.raises(ValueError) as exc:
        validate_empty_cell_count(matrix)
    assert str(exc.value) == MSG_EMPTY_COUNT


def test_u_red_02_raises_when_one_empty_cell() -> None:
    """One blank → EMPTY_COUNT."""
    matrix = _full_grid_without_zeros()
    matrix[0][0] = EMPTY_CELL
    with pytest.raises(ValueError) as exc:
        validate_empty_cell_count(matrix)
    assert str(exc.value) == MSG_EMPTY_COUNT


def test_u_red_02_raises_when_three_empty_cells() -> None:
    """Three blanks → EMPTY_COUNT."""
    matrix = _full_grid_without_zeros()
    matrix[0][0] = EMPTY_CELL
    matrix[0][1] = EMPTY_CELL
    matrix[0][2] = EMPTY_CELL
    with pytest.raises(ValueError) as exc:
        validate_empty_cell_count(matrix)
    assert str(exc.value) == MSG_EMPTY_COUNT
