"""Boundary value/duplicate/all + Domain magic square / solver coverage."""

from __future__ import annotations

import copy

import pytest

from magicsquare.boundary import solve, validate_all, validate_no_duplicate_nonzero, validate_value_range
from magicsquare.constants import (
    CELL_MAX,
    EMPTY_CELL,
    MAGIC_SUM,
    MSG_DUPLICATE,
    MSG_GRID_NOT_4X4,
    MSG_NO_SOLUTION,
    MSG_VALUE_RANGE,
)
from magicsquare.domain import is_magic_square, solve_grid


# Completed 4×4 classical magic square (1..16), row/col/diag sum = MAGIC_SUM.
_CLASSIC_SOLVED: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


def test_validate_value_range_rejects_negative() -> None:
    matrix = copy.deepcopy(_CLASSIC_SOLVED)
    matrix[0][0] = -1
    with pytest.raises(ValueError) as exc:
        validate_value_range(matrix)
    assert str(exc.value) == MSG_VALUE_RANGE


def test_validate_value_range_rejects_above_cell_max() -> None:
    matrix = copy.deepcopy(_CLASSIC_SOLVED)
    matrix[3][3] = CELL_MAX + 1
    with pytest.raises(ValueError) as exc:
        validate_value_range(matrix)
    assert str(exc.value) == MSG_VALUE_RANGE


def test_validate_no_duplicate_nonzero_rejects_duplicate() -> None:
    matrix = copy.deepcopy(_CLASSIC_SOLVED)
    matrix[0][1] = matrix[0][2]
    with pytest.raises(ValueError) as exc:
        validate_no_duplicate_nonzero(matrix)
    assert str(exc.value) == MSG_DUPLICATE


def test_validate_all_none_raises_size_before_other_checks() -> None:
    with pytest.raises(ValueError) as exc:
        validate_all(None)
    assert str(exc.value) == MSG_GRID_NOT_4X4


def test_validate_all_accepts_solvable_partial_grid() -> None:
    """Two blanks, unique 1..16 except missing pair — boundary pipeline passes."""
    partial = [
        [EMPTY_CELL, 3, 2, 13],
        [5, EMPTY_CELL, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]
    validate_all(partial)


def test_is_magic_square_true_on_classic() -> None:
    assert is_magic_square(_CLASSIC_SOLVED)


def test_is_magic_square_false_when_empty_cell() -> None:
    partial = copy.deepcopy(_CLASSIC_SOLVED)
    partial[0][0] = EMPTY_CELL
    assert is_magic_square(partial) is False


def test_is_magic_square_false_when_row_sum_wrong() -> None:
    bad = copy.deepcopy(_CLASSIC_SOLVED)
    bad[0][0] += 1
    bad[0][1] -= 1
    assert is_magic_square(bad) is False


def test_is_magic_square_false_when_rows_cols_ok_but_diagonal_wrong() -> None:
    """Semi-magic: all rows/cols sum to MAGIC_SUM; main diagonal ≠ MAGIC_SUM (PRD diagonal check)."""
    semi = [
        [16, 5, 11, 2],
        [8, 9, 7, 10],
        [3, 12, 6, 13],
        [7, 8, 10, 9],
    ]
    assert sum(semi[0]) == MAGIC_SUM
    assert sum(semi[i][0] for i in range(4)) == MAGIC_SUM
    assert is_magic_square(semi) is False


def test_is_magic_square_false_when_anti_diagonal_wrong_only() -> None:
    """Rows/cols/main diagonal are MAGIC_SUM, but anti-diagonal is not (covers anti-diagonal branch)."""
    semi = [
        [17, 5, 2, 10],
        [12, 7, 8, 7],
        [8, 5, 7, 14],
        [-3, 17, 17, 3],
    ]
    for row in semi:
        assert sum(row) == MAGIC_SUM
    for col in range(4):
        assert sum(semi[row][col] for row in range(4)) == MAGIC_SUM
    assert sum(semi[i][i] for i in range(4)) == MAGIC_SUM
    assert sum(semi[i][3 - i] for i in range(4)) != MAGIC_SUM
    assert is_magic_square(semi) is False


def test_solve_grid_first_forward_attempt_succeeds() -> None:
    """Blanks (0,2),(2,3) — forward (low→first, high→second) already matches the classic solution."""
    partial = [
        [16, 3, EMPTY_CELL, 13],
        [5, 10, 11, 8],
        [9, 6, 7, EMPTY_CELL],
        [4, 15, 14, 1],
    ]
    assert solve_grid(partial) == [1, 3, 2, 3, 4, 12]


def test_solve_grid_uses_reverse_placement_when_forward_not_magic() -> None:
    """Blanks (0,0),(1,1): missing {10,16}. Low→first / high→second breaks row 0; reverse restores classic."""
    partial = [
        [EMPTY_CELL, 3, 2, 13],
        [5, EMPTY_CELL, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]
    assert solve_grid(partial) == [1, 1, 16, 2, 2, 10]


def test_solve_grid_raises_no_solution() -> None:
    """Valid contract input but neither placement yields a magic square."""
    partial = [
        [EMPTY_CELL, 2, 3, 4],
        [5, EMPTY_CELL, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]
    with pytest.raises(ValueError) as exc:
        solve_grid(partial)
    assert str(exc.value) == MSG_NO_SOLUTION


def test_solve_delegates_validate_and_domain() -> None:
    partial = [
        [EMPTY_CELL, 3, 2, 13],
        [5, EMPTY_CELL, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]
    assert solve(partial) == [1, 1, 16, 2, 2, 10]
