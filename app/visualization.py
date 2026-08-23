from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtWidgets import QWidget

class TankVisualization(QWidget):

    def __init__(self):
        super().__init__()

        self.setMinimumHeight(220)

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        # Dimensions of the Tanks
        tank_width = 100
        tank_height = 140

        # Positions of the Tanks
        tank1_x = 80
        tank2_x = 320
        tank_y = 40

        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(2)

        painter.setPen(pen)

        painter.drawRect(
            tank1_x,
            tank_y,
            tank_width,
            tank_height
        )

        painter.drawRect(
            tank2_x,
            tank_y,
            tank_width,
            tank_height
        )

        water_brush = QBrush(
            Qt.GlobalColor.blue
        )

        painter.setBrush(water_brush)

        water_height = 70

        painter.drawRect(
            tank1_x,
            tank_y + tank_height - water_height,
            tank_width,
            water_height
        )

        painter.drawRect(
            tank2_x,
            tank_y + tank_height - water_height,
            tank_width,
            water_height
        )

        painter.setPen(pen)

        pipe_y = tank_y + 90

        painter.drawLine(
            tank1_x + tank_width,
            pipe_y,
            tank2_x,
            pipe_y
        )

        painter.drawText(
            tank1_x + 25,
            tank_y + tank_height + 25,
            "Tank 1"
        )

        painter.drawText(
            tank2_x + 25,
            tank_y + tank_height + 25,
            "Tank 2"
        )

        painter.end()