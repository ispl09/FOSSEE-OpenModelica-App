import os
import scipy.io
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor


def read_results(result_file):

    if not os.path.exists(result_file):
        raise FileNotFoundError(
            "Simulation result file was not found."
        )

    return scipy.io.loadmat(result_file)


def get_variable_names(data):

    names = data["name"]

    variable_names = []

    for column in range(len(names[0])):

        name = ""

        for row in names:
            if column < len(row):
                character = row[column]

                if character != "\x00":
                    name += character

        name = name.strip()

        if name:
            variable_names.append(name)

    return variable_names


def get_variable(data, variable_name):

    names = get_variable_names(data)

    if variable_name not in names:
        raise ValueError(
            f"Variable '{variable_name}' was not found."
        )

    index = names.index(variable_name)

    data_info = data["dataInfo"]

    data_set = int(data_info[0, index])
    data_index = int(data_info[1, index])

    if data_index < 0:
        data_index = abs(data_index)

        values = data["data_2"][data_index - 1, :]

    else:
        values = data["data_1"][data_index - 1, :]

    return np.asarray(values).flatten()


def plot_tank_heights(result_file):

    data = read_results(result_file)

    time = get_variable(data, "time")
    tank1_height = get_variable(data, "tank1.h")
    tank2_height = get_variable(data, "tank2.h")

    plt.figure(figsize=(8, 5))

    plt.plot(time, tank1_height, label="Tank 1 Height")
    plt.plot(time, tank2_height, label="Tank 2 Height")

    plt.xlabel("Time")
    plt.ylabel("Height")

    plt.title("Two Connected Tanks - Simulation Results")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

class TankResultVisualization(QWidget):

    def __init__(self, tank1_height, tank2_height):
        super().__init__()

        self.tank1_height = tank1_height
        self.tank2_height = tank2_height

        self.setMinimumHeight(260)

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        tank_width = 140
        tank_height = 180

        tank_y = 40
        total_width = 540
        start_x = (
            self.width() - total_width
        ) // 2

        tank1_x = start_x
        tank2_x = start_x + 400

        max_height = max(
            self.tank1_height,
            self.tank2_height,
            2.0
        )

        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(3)

        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

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

        water1 = int(
            (self.tank1_height / max_height)
        * tank_height
        )

        water2 = int(
            (self.tank2_height / max_height)
        * tank_height
        )

        if self.tank1_height > 0 and water1 < 5:
            water1 = 5

        if self.tank2_height > 0 and water2 < 5:
            water2 = 5

        water_brush = QBrush(
            QColor("#4A90E2")
        )

        painter.setBrush(water_brush)

        painter.drawRect(
            tank1_x,
            tank_y + tank_height - water1,
            tank_width,
            water1
        )

        painter.drawRect(
            tank2_x,
            tank_y + tank_height - water2,
            tank_width,
            water2
        )

        painter.setPen(pen)

        pipe_y = tank_y + 100

        painter.drawLine(
            tank1_x + tank_width,
            pipe_y,
            tank2_x,
            pipe_y
        )

        painter.drawText(
            tank1_x + 45,
            tank_y + tank_height + 30,
            "Tank 1"
        )

        painter.drawText(
            tank2_x + 45,
            tank_y + tank_height + 30,
            "Tank 2"
        )

        painter.end()

class ResultsWindow(QWidget):

    def __init__(self, result_file):
        super().__init__()

        self.setWindowTitle(
            "Two Connected Tanks - Simulation Results"
        )

        self.setMinimumSize(900, 700)

        data = read_results(result_file)

        self.time = get_variable(
            data,
            "time"
        )

        self.tank1_height = get_variable(
            data,
            "tank1.h"
        )

        self.tank2_height = get_variable(
            data,
            "tank2.h"
        )

        self.final_tank1 = float(
            self.tank1_height[-1]
        )

        self.final_tank2 = float(
            self.tank2_height[-1]
        )

        layout = QVBoxLayout()

        title = QLabel(
            "Two Connected Tanks - Simulation Results"
        )

        title.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(title)

        self.tank_visualization = TankResultVisualization(
            self.final_tank1,
            self.final_tank2
        )

        layout.addWidget(
            self.tank_visualization
        )

        heights_layout = QHBoxLayout()

        tank1_label = QLabel(
            f"Tank 1 Height: {self.final_tank1:.3f}"
        )

        tank2_label = QLabel(
            f"Tank 2 Height: {self.final_tank2:.3f}"
        )

        tank1_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        tank2_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        heights_layout.addWidget(
            tank1_label
        )

        heights_layout.addWidget(
            tank2_label
        )

        layout.addLayout(
            heights_layout
        )


        # Graph Plotting

        figure = Figure(figsize=(8, 4))

        canvas = FigureCanvas(figure)

        axis = figure.add_subplot(111)

        axis.plot(
            self.time,
            self.tank1_height,
            label="Tank 1 Height"
        )

        axis.plot(
            self.time,
            self.tank2_height,
            label="Tank 2 Height"
        )

        axis.set_xlabel("Time")
        axis.set_ylabel("Height")

        axis.set_title(
            "Two Connected Tanks - Height vs Time"
        )

        axis.legend()
        axis.grid(True)

        figure.tight_layout()

        layout.addWidget(canvas)

        self.setLayout(layout)