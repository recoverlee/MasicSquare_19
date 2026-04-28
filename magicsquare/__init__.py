"""Magic Square 4×4 package — domain rules and boundary validation."""

from magicsquare.boundary import validate_grid_shape
from magicsquare.constants import EMPTY_CELL, MATRIX_SIZE, MSG_GRID_NOT_4X4
from magicsquare.domain import find_blank_coords

__all__ = [
    "EMPTY_CELL",
    "MATRIX_SIZE",
    "MSG_GRID_NOT_4X4",
    "find_blank_coords",
    "validate_grid_shape",
]
