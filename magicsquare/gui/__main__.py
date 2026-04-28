"""Official GUI entry: ``python -m magicsquare.gui``."""

from __future__ import annotations

import sys


def main() -> None:
    from PyQt6.QtWidgets import QApplication

    from magicsquare.gui.window import MainWindow

    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(360, 320)
    window.show()
    raise SystemExit(app.exec())


if __name__ == "__main__":
    main()
