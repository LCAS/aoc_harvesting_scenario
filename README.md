# AOC HARVESTING SCENARIO

AOC harvesting scenario for mobile manipulators including interactable plants, part of the Agri-OpenCore (AOC) project

To get started with this scenario, follow these steps:

1. Clone the repository into your workspace:
    ```bash
    git clone https://github.com/LCAS/aoc_harvesting_scenario.git
    ```

2. Open the cloned repository with `vscode`. When prompted by `vscode`, choose to reopen the repository in a container. This will build the container, install all dependencies, and set up the workspace.

3. Once inside the container, launch the scenario with the following command:
    ```bash
    ros2 launch scenario_bringup bringup.launch.py
    ```
    or
    ```bash
    ros2 launch scenario_bringup only_world_sim.launch.py
    ```

![image](https://github.com/user-attachments/assets/9a034ec5-72de-432a-9bc1-40bb208f2aa8)
