"""Shared constants for grid dimension and PRD §6.1 boundary messages."""

from typing import Final

# Physical grid order (4×4 classical magic square problem).
MATRIX_SIZE: Final[int] = 4

# Sentinel for an empty cell in input grids.
EMPTY_CELL: Final[int] = 0

# PRD §6.1 — code SIZE
MSG_GRID_NOT_4X4: Final[str] = "Grid must be 4x4."
