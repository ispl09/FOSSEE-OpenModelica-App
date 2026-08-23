import os
import subprocess


def run_simulation(application, start_time, stop_time):
    """Run the compiled OpenModelica simulation."""

    model_folder = os.path.dirname(
        os.path.abspath(application)
    )

    project_folder = os.path.dirname(model_folder)
    runtime_folder = os.path.join(
        project_folder,
        "runtime"
    )

    environment = os.environ.copy()

    environment["PATH"] = (
        runtime_folder
        + os.pathsep
        + environment["PATH"]
    )

    command = [
        application,
        f"-override=startTime={start_time},stopTime={stop_time}",
        f"-inputPath={model_folder}",
    ]

    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=model_folder,
        env=environment,
    )