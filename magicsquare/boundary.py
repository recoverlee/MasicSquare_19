"""Input/output boundary — validation and mapping; no business rules beyond contracts."""

from __future__ import annotations

from magicsquare.constants import MATRIX_SIZE, MSG_GRID_NOT_4X4


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
