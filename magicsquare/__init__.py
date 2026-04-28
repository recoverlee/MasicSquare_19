"""Magic Square 4×4 package — domain rules and boundary validation."""

from magicsquare.boundary import solve, validate_all, validate_empty_cell_count, validate_grid_shape
from magicsquare.constants import (
    EMPTY_CELL,
    MATRIX_SIZE,
    MSG_DUPLICATE,
    MSG_EMPTY_COUNT,
    MSG_GRID_NOT_4X4,
    MSG_NO_SOLUTION,
    MSG_VALUE_RANGE,
)
from magicsquare.domain import find_blank_coords

__all__ = [
    "EMPTY_CELL",
    "MATRIX_SIZE",
    "MSG_DUPLICATE",
    "MSG_EMPTY_COUNT",
    "MSG_GRID_NOT_4X4",
    "MSG_NO_SOLUTION",
    "MSG_VALUE_RANGE",
    "find_blank_coords",
    "solve",
    "validate_all",
    "validate_empty_cell_count",
    "validate_grid_shape",
]
