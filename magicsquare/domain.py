"""Pure domain logic — no I/O, no PyQt, no boundary/framework imports."""

from __future__ import annotations

import copy

from magicsquare.constants import (
    CELL_MAX,
    CELL_MIN,
    EMPTY_CELL,
    MAGIC_SUM,
    MATRIX_SIZE,
    MSG_NO_SOLUTION,
)


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Collect coordinates of empty cells in row-major (row asc, then col asc) order.

    Coordinates are **0-based** row and column indices, consistent with ``grid[r][c]``.

    Preconditions (enforced by Boundary in full flows): ``grid`` is ``MATRIX_SIZE``
    × ``MATRIX_SIZE`` and contains exactly two ``EMPTY_CELL`` values.

    Args:
        grid: Square matrix of integers.

    Returns:
        List of ``(row, col)`` pairs in row-major scan order.
    """
    blanks: list[tuple[int, int]] = []
    for row in range(MATRIX_SIZE):
        for col in range(MATRIX_SIZE):
            if grid[row][col] == EMPTY_CELL:
                blanks.append((row, col))
    return blanks


def _sorted_missing_pair(grid: list[list[int]]) -> tuple[int, int]:
    """Return the two numbers in ``CELL_MIN``..``CELL_MAX`` absent from non-empty cells."""
    present: set[int] = set()
    for row in range(MATRIX_SIZE):
        for col in range(MATRIX_SIZE):
            v = grid[row][col]
            if v != EMPTY_CELL:
                present.add(v)
    missing = [x for x in range(CELL_MIN, CELL_MAX + 1) if x not in present]
    return (missing[0], missing[1])


def is_magic_square(grid: list[list[int]]) -> bool:
    """True iff every row, column, both diagonals sum to ``MAGIC_SUM`` (full grid, no blanks)."""
    for row in range(MATRIX_SIZE):
        for col in range(MATRIX_SIZE):
            if grid[row][col] == EMPTY_CELL:
                return False
    for row in range(MATRIX_SIZE):
        if sum(grid[row][col] for col in range(MATRIX_SIZE)) != MAGIC_SUM:
            return False
    for col in range(MATRIX_SIZE):
        if sum(grid[row][col] for row in range(MATRIX_SIZE)) != MAGIC_SUM:
            return False
    if sum(grid[i][i] for i in range(MATRIX_SIZE)) != MAGIC_SUM:
        return False
    if sum(grid[i][MATRIX_SIZE - 1 - i] for i in range(MATRIX_SIZE)) != MAGIC_SUM:
        return False
    return True


def solve_grid(grid: list[list[int]]) -> list[int]:
    """Fill two blanks per PRD: try smaller→first blank / larger→second, then reverse.

    Returns:
        ``[r1, c1, n1, r2, c2, n2]`` with **1-indexed** coordinates.

    Raises:
        ValueError: ``MSG_NO_SOLUTION`` when neither placement yields a magic square.
    """
    blanks = find_blank_coords(grid)
    (r1, c1), (r2, c2) = blanks[0], blanks[1]
    low, high = _sorted_missing_pair(grid)

    for n_first, n_second in ((low, high), (high, low)):
        trial = copy.deepcopy(grid)
        trial[r1][c1] = n_first
        trial[r2][c2] = n_second
        if is_magic_square(trial):
            return [
                r1 + 1,
                c1 + 1,
                n_first,
                r2 + 1,
                c2 + 1,
                n_second,
            ]

    raise ValueError(MSG_NO_SOLUTION)
