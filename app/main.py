import sys

from PyQt6.QtWidgets import QApplication
from ui import SimulationApp

app = QApplication(sys.argv)

window = SimulationApp()
window.show()

sys.exit(app.exec())