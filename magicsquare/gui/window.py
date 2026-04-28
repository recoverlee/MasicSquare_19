"""Main window: 4×4 grid editor and solve action."""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from magicsquare.boundary import solve
from magicsquare.constants import CELL_MAX, EMPTY_CELL, MATRIX_SIZE


class MainWindow(QWidget):
    """Minimal MVP: spin boxes for cells, Solve runs boundary ``solve``."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Magic Square 4×4")
        self._cells: list[list[QSpinBox]] = []

        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        for row in range(MATRIX_SIZE):
            row_boxes: list[QSpinBox] = []
            for col in range(MATRIX_SIZE):
                spin = QSpinBox()
                spin.setRange(EMPTY_CELL, CELL_MAX)
                spin.setValue(EMPTY_CELL)
                spin.setMinimumWidth(52)
                grid_layout.addWidget(spin, row, col)
                row_boxes.append(spin)
            self._cells.append(row_boxes)

        self._result = QLabel("")
        self._result.setWordWrap(True)

        solve_btn = QPushButton("풀기")
        solve_btn.clicked.connect(self._on_solve)

        actions = QHBoxLayout()
        actions.addWidget(solve_btn)
        actions.addStretch()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("격자 (빈칸 = 0):"))
        layout.addWidget(grid_widget)
        layout.addLayout(actions)
        layout.addWidget(QLabel("결과 [r1,c1,n1,r2,c2,n2] (좌표 1-index):"))
        layout.addWidget(self._result)

    def _read_matrix(self) -> list[list[int]]:
        return [[self._cells[r][c].value() for c in range(MATRIX_SIZE)] for r in range(MATRIX_SIZE)]

    def _on_solve(self) -> None:
        matrix = self._read_matrix()
        try:
            out = solve(matrix)
            self._result.setText(
                f"[{out[0]}, {out[1]}, {out[2]}, {out[3]}, {out[4]}, {out[5]}]"
            )
        except ValueError as exc:
            self._result.clear()
            QMessageBox.warning(self, "입력 또는 해 없음", str(exc))
