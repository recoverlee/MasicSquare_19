"""Pure domain logic — no I/O, no PyQt, no boundary/framework imports."""

from __future__ import annotations

from magicsquare.constants import EMPTY_CELL, MATRIX_SIZE


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
