"""Input/output boundary — validation and mapping; no business rules beyond contracts."""

from __future__ import annotations

from magicsquare.constants import (
    CELL_MAX,
    CELL_MIN,
    EMPTY_CELL,
    MATRIX_SIZE,
    MSG_DUPLICATE,
    MSG_EMPTY_COUNT,
    MSG_GRID_NOT_4X4,
    MSG_VALUE_RANGE,
)
from magicsquare.domain import solve_grid


def validate_grid_shape(matrix: list[list[int]] | None) -> None:
    """Ensure ``matrix`` is a ``MATRIX_SIZE`` × ``MATRIX_SIZE`` rectangular grid.

    Raises:
        ValueError: With PRD §6.1 ``SIZE`` message when shape is invalid.
    """
    if matrix is None:
        raise ValueError(MSG_GRID_NOT_4X4)
    if len(matrix) != MATRIX_SIZE:
        raise ValueError(MSG_GRID_NOT_4X4)
    for row in matrix:
        if len(row) != MATRIX_SIZE:
            raise ValueError(MSG_GRID_NOT_4X4)


def validate_empty_cell_count(matrix: list[list[int]]) -> None:
    """Ensure ``matrix`` contains exactly two ``EMPTY_CELL`` values.

    Raises:
        ValueError: With PRD §6.1 ``EMPTY_COUNT`` message when count ≠ 2.
    """
    count = sum(1 for r in range(MATRIX_SIZE) for c in range(MATRIX_SIZE) if matrix[r][c] == EMPTY_CELL)
    if count != 2:
        raise ValueError(MSG_EMPTY_COUNT)


def validate_value_range(matrix: list[list[int]]) -> None:
    """Ensure each cell is ``EMPTY_CELL`` or in ``CELL_MIN``..``CELL_MAX`` (PRD §6)."""
    for row in range(MATRIX_SIZE):
        for col in range(MATRIX_SIZE):
            v = matrix[row][col]
            if v != EMPTY_CELL and not (CELL_MIN <= v <= CELL_MAX):
                raise ValueError(MSG_VALUE_RANGE)


def validate_no_duplicate_nonzero(matrix: list[list[int]]) -> None:
    """Ensure non-blank values are unique (zeros excluded)."""
    seen: list[int] = []
    for row in range(MATRIX_SIZE):
        for col in range(MATRIX_SIZE):
            v = matrix[row][col]
            if v != EMPTY_CELL:
                seen.append(v)
    if len(seen) != len(set(seen)):
        raise ValueError(MSG_DUPLICATE)


def validate_all(matrix: list[list[int]] | None) -> None:
    """Run full input contract: shape → empty count → value range → duplicates."""
    validate_grid_shape(matrix)
    assert matrix is not None
    validate_empty_cell_count(matrix)
    validate_value_range(matrix)
    validate_no_duplicate_nonzero(matrix)


def solve(matrix: list[list[int]] | None) -> list[int]:
    """Validate input then return PRD ``int[6]`` success vector (1-indexed coordinates)."""
    validate_all(matrix)
    assert matrix is not None
    return solve_grid(matrix)
