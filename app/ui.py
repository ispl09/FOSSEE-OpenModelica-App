import os

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QFileDialog,
    QGroupBox
)

from simulation import run_simulation
from results import ResultsWindow
from visualization import TankVisualization


class SimulationApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Two Connected Tanks - Simulation"
        )

        self.setFixedWidth(550)

        project_folder = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        default_application = os.path.join(
            project_folder,
            "NonInteractingTanks",
            "TwoConnectedTanks.exe"
        )

        self.application = default_application

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # TITLE

        title = QLabel(
            "Two Connected Tanks"
        )

        title.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle = QLabel(
            "OpenModelica Simulation Interface"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # APPLICATION TO LAUNCH

        application_group = QGroupBox(
            "Application to Launch"
        )

        application_layout = QHBoxLayout()

        self.application_input = QLineEdit()

        self.application_input.setText(
            default_application
        )

        self.application_input.setPlaceholderText(
            "Select an executable"
        )

        application_layout.addWidget(
            self.application_input
        )

        browse_button = QPushButton(
            "Browse"
        )

        browse_button.clicked.connect(
            self.browse_application
        )

        application_layout.addWidget(
            browse_button
        )

        application_group.setLayout(
            application_layout
        )

        main_layout.addWidget(
            application_group
        )

        # SIMULATION PARAMETERS

        parameters_group = QGroupBox(
            "Simulation Parameters"
        )

        parameters_layout = QVBoxLayout()

        # Start time
        start_layout = QHBoxLayout()

        start_label = QLabel(
            "Start time"
        )

        self.start_time_input = QLineEdit()

        self.start_time_input.setText(
            "0"
        )

        self.start_time_input.setPlaceholderText(
            "Example: 0"
        )

        start_layout.addWidget(
            start_label
        )

        start_layout.addWidget(
            self.start_time_input
        )

        parameters_layout.addLayout(
            start_layout
        )

        stop_layout = QHBoxLayout()

        stop_label = QLabel(
            "Stop time"
        )

        self.stop_time_input = QLineEdit()

        self.stop_time_input.setText(
            "1"
        )

        self.stop_time_input.setPlaceholderText(
            "Example: 1"
        )

        stop_layout.addWidget(
            stop_label
        )

        stop_layout.addWidget(
            self.stop_time_input
        )

        parameters_layout.addLayout(
            stop_layout
        )

        parameters_group.setLayout(
            parameters_layout
        )

        main_layout.addWidget(
            parameters_group
        )

        # Run Button

        run_button = QPushButton(
            "Run Simulation"
        )

        run_button.clicked.connect(
            self.run_simulation
        )

        main_layout.addWidget(
            run_button
        )

        # Results Button

        self.results_button = QPushButton(
            "Show Results"
        )

        self.results_button.setEnabled(
            False
        )

        self.results_button.clicked.connect(
            self.show_results
        )

        main_layout.addWidget(
            self.results_button
        )

        # Status of the generated Simulation

        status_title = QLabel(
            "Status"
        )

        self.status_label = QLabel(
            "Ready to run simulation."
        )

        self.status_label.setStyleSheet(
            "padding: 8px; border: 1px solid #cccccc;"
        )

        main_layout.addWidget(
            status_title
        )

        main_layout.addWidget(
            self.status_label
        )

        self.setLayout(
            main_layout
        )

    # BROWSE APPLICATION

    def browse_application(self):

        application, _ = QFileDialog.getOpenFileName(
            self,
            "Select OpenModelica Executable",
            "",
            "Executable Files (*.exe);;All Files (*)"
        )

        if application:

            self.application = application

            self.application_input.setText(
                application
            )

            self.results_button.setEnabled(
                False
            )

            self.status_label.setText(
                "Application selected."
            )

    # RUN SIMULATION

    def run_simulation(self):

        application = (
            self.application_input.text().strip()
        )

        start_time = (
            self.start_time_input.text().strip()
        )

        stop_time = (
            self.stop_time_input.text().strip()
        )

        if not application:

            QMessageBox.warning(
                self,
                "Application Required",
                "Please select an application to launch."
            )

            return

        if not os.path.isfile(application):

            self.status_label.setText(
                "Simulation executable not found."
            )

            QMessageBox.critical(
                self,
                "Application Not Found",
                "The selected application was not found.\n\n"
                f"Selected path:\n{application}"
            )

            return

        # Check Times

        if not start_time or not stop_time:

            QMessageBox.warning(
                self,
                "Error",
                "Please enter start time and stop time."
            )

            return

        try:

            start_time = int(start_time)
            stop_time = int(stop_time)

        except ValueError:

            QMessageBox.warning(
                self,
                "Invalid Input",
                "Start time and stop time must be integers."
            )

            return

        if (
            start_time < 0
            or start_time >= stop_time
            or stop_time >= 5
        ):

            QMessageBox.warning(
                self,
                "Invalid Simulation Time",
                "Please ensure:\n\n"
                "0 ≤ Start Time < Stop Time < 5"
            )

            return

        self.application = application

        self.status_label.setText(
            "Running simulation..."
        )

        result = run_simulation(
            self.application,
            start_time,
            stop_time
        )

        if result.returncode == 0:

            self.status_label.setText(
                "Simulation completed successfully."
            )

            self.results_button.setEnabled(
                True
            )

            QMessageBox.information(
                self,
                "Simulation Complete",
                "Simulation completed successfully."
            )

        else:

            self.status_label.setText(
                "Simulation failed."
            )

            error_message = (
                "Simulation failed.\n\n"
                f"Exit code: {result.returncode}\n\n"
                f"Output:\n{result.stdout}\n\n"
                f"Error:\n{result.stderr}"
            )

            QMessageBox.critical(
                self,
                "Simulation Failed",
                error_message
            )


    def show_results(self):

        try:
            application_directory = os.path.dirname(
                self.application
            )

            application_name = os.path.splitext(
                os.path.basename(self.application)
            )[0]

            result_file = os.path.join(
                application_directory,
                application_name + "_res.mat"
            )

            if not os.path.exists(result_file):

                QMessageBox.critical(
                    self,
                    "Error",
                    "Simulation result file was not found.\n\n"
                    f"Expected location:\n{result_file}"
                )

                return

            self.results_window = ResultsWindow(
                result_file
            )

            self.results_window.show()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Results Error",
                "Could not display simulation results.\n\n"
                f"{e}"
            )

# Starting the application


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)

    window = SimulationApp()
    window.show()

    sys.exit(app.exec())