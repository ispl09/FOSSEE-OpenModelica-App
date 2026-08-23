#FOSSEE OpenModelica Desktop Application

Overview

A desktop application developed using Python 3.6+ and PyQt6 to run a compiled OpenModelica simulation of a two-connected-tank system.

The application provides a simple graphical interface for selecting the OpenModelica executable, entering simulation start and stop times, running the simulation, and viewing the simulation results.

Features

- PyQt6-based desktop GUI

- Browse and select the OpenModelica executable

- Start time and stop time input fields

- Integer validation for simulation parameters

- Validation of the required condition:
  
  "0 <= Start Time < Stop Time < 5"

- OpenModelica simulation execution using runtime flags

- Simulation status and error messages

- Simulation result visualization

- Two-connected-tank visualization

- Self-contained OpenModelica runtime dependencies

Project Structure

FOSSEE_OpenModelica_App/
│
├── app/
│   ├── main.py
│   ├── results.py
│   ├── simulation.py
│   ├── ui.py
│   └── visualization.py
│
├── NonInteractingTanks/
│   ├── TwoConnectedTanks.exe
│   ├── TwoConnectedTanks.mo
│   ├── FlowConnect.mo
│   ├── Tank.mo
│   ├── Tank2.mo
│   ├── package.mo
│   ├── package.order
│   ├── TwoConnectedTanks_init.xml
│   ├── TwoConnectedTanks_info.json
│   ├── TwoConnectedTanks_external_functions.json
│   └── TwoConnectedTanks_JacA.bin
│
├── runtime/
│   └── Required OpenModelica runtime DLL files
|
├── requirements.txt
└── README.md

Technologies

- Python 3.6+
- PyQt6
- OpenModelica
- Windows 10/11

Installation

1. Install Python

Install Python 3.6 or later.

2. Install dependencies

Open a terminal in the project directory and run:

pip install -r requirements.txt

Running the Application

From the project root directory, run:

python app/main.py

The application window will open.

Step 1: Select the executable

Click Browse and select:

NonInteractingTanks/TwoConnectedTanks.exe

Step 2: Enter simulation times

Enter integer values for:

- Start Time
- Stop Time

The following condition must be satisfied:

0 <= Start Time < Stop Time < 5

For example:

Start Time: 0
Stop Time: 1

Step 3: Run the simulation

Click Run Simulation.

The application passes the simulation parameters to the OpenModelica executable using the runtime override flag:

-override=startTime=<start>,stopTime=<stop>

Step 4: View results

After a successful simulation, click Show Results to display the simulation results.

OpenModelica Model

The application uses the compiled "TwoConnectedTanks" OpenModelica model.

The executable and its required model/runtime files are included in the repository so that the application can execute the simulation without depending on the developer's local OpenModelica installation path.

Error Handling

The application checks for:

- Missing executable
- Missing simulation result file
- Empty simulation parameters
- Non-integer input
- Invalid simulation time range
- Simulation execution failure

Appropriate error messages are displayed through the GUI.

Simulation Parameters

The application accepts integer start and stop times subject to:

0 <= Start Time < Stop Time < 5

Examples:

Start Time| Stop Time| Result
0| 1| Valid
1| 4| Valid
0| 4| Valid
2| 2| Invalid
3| 1| Invalid
0| 5| Invalid
-1| 2| Invalid
0.5| 2| Invalid

Purpose

This project was developed as a screening task demonstrating:

- Desktop GUI development with PyQt6
- Python programming and object-oriented design
- Integration of Python with an external simulation executable
- OpenModelica simulation execution
- Command-line argument handling
- Runtime dependency management
- Input validation
- Simulation result visualization
- User-oriented error handling
