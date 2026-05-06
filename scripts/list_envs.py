"""
List gym environments registered by this external Isaac Lab project.
"""

from isaaclab.app import AppLauncher

app_launcher = AppLauncher(headless=True)
simulation_app = app_launcher.app

import gymnasium as gym
from prettytable import PrettyTable

import nonapod_lab.tasks  # noqa: F401


def main() -> None:
    table = PrettyTable(["S. No.", "Task Name", "Entry Point", "Config"])
    table.title = "Available Nonapod Isaac Lab Environments"
    table.align["Task Name"] = "l"
    table.align["Entry Point"] = "l"
    table.align["Config"] = "l"

    index = 0
    for task_spec in gym.registry.values():
        if "Isaac-Nonapod" not in task_spec.id:
            continue
        table.add_row([index + 1, task_spec.id, task_spec.entry_point, task_spec.kwargs["env_cfg_entry_point"]])
        index += 1

    print(table)


if __name__ == "__main__":
    try:
        main()
    finally:
        simulation_app.close()
