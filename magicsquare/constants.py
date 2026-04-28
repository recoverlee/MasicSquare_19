"""Shared constants for grid dimension and PRD §6.1 boundary messages."""

from typing import Final

# Physical grid order (4×4 classical magic square problem).
MATRIX_SIZE: Final[int] = 4

# Classical cell labels for a 4×4 puzzle use 1 .. N² inclusive (non-blanks).
CELL_MIN: Final[int] = 1
CELL_MAX: Final[int] = MATRIX_SIZE * MATRIX_SIZE

# Magic constant for row/col/diag sums (n×n with 1..n²): n(n²+1)/2.
MAGIC_SUM: Final[int] = MATRIX_SIZE * (MATRIX_SIZE * MATRIX_SIZE + 1) // 2

# Sentinel for an empty cell in input grids.
EMPTY_CELL: Final[int] = 0

# PRD §6.1 — code SIZE
MSG_GRID_NOT_4X4: Final[str] = "Grid must be 4x4."

# PRD §6.1 — code EMPTY_COUNT
MSG_EMPTY_COUNT: Final[str] = "There must be exactly 2 empty cells (0)."

# PRD §6.1 — code VALUE_RANGE
MSG_VALUE_RANGE: Final[str] = "Each cell must be 0 or in range 1..16."

# PRD §6.1 — code DUPLICATE
MSG_DUPLICATE: Final[str] = "Values 1..16 must not duplicate (excluding zeros)."

# PRD §6.1 — code NO_SOLUTION
MSG_NO_SOLUTION: Final[str] = "No valid placement forms a 4x4 magic square."
