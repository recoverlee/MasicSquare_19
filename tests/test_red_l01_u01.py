"""Dual-Track RED bundle: L-RED-01 (domain blanks) + U-RED-01 (shape)."""

from __future__ import annotations

import pytest

from magicsquare.boundary import validate_grid_shape
from magicsquare.constants import EMPTY_CELL, MATRIX_SIZE, MSG_GRID_NOT_4X4
from magicsquare.domain import find_blank_coords


def test_l_red_01_find_blank_coords_returns_two_blanks_row_major() -> None:
    """L-RED-01: blanks appear in row-major order; exactly two coordinates."""
    grid: list[list[int]] = [
        [EMPTY_CELL, 2, 3, 4],
        [5, EMPTY_CELL, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]
    got = find_blank_coords(grid)
    assert got == [(0, 0), (1, 1)]


def test_u_red_01_wrong_height_raises_value_error() -> None:
    """U-RED-01: fewer rows than MATRIX_SIZE must raise with SIZE message."""
    matrix = [[1, 2, 3, 4] for _ in range(MATRIX_SIZE - 1)]
    with pytest.raises(ValueError) as exc:
        validate_grid_shape(matrix)
    assert str(exc.value) == MSG_GRID_NOT_4X4


def test_u_red_01_wrong_width_raises_value_error() -> None:
    """U-RED-01: ragged / wrong column count must raise."""
    matrix = [[1, 2, 3] for _ in range(MATRIX_SIZE)]
    with pytest.raises(ValueError) as exc:
        validate_grid_shape(matrix)
    assert str(exc.value) == MSG_GRID_NOT_4X4


def test_u_red_01_none_raises_value_error() -> None:
    """U-RED-01: missing grid reference must raise."""
    with pytest.raises(ValueError) as exc:
        validate_grid_shape(None)
    assert str(exc.value) == MSG_GRID_NOT_4X4
