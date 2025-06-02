# AOC HARVESTING SCENARIO

AOC harvesting scenario for mobile manipulators, including interactable plants, part of the Agri-OpenCore (AOC) project

To get started with this scenario, follow these steps:

1. Clone the repository into your workspace:
    ```bash
    git clone https://github.com/LCAS/aoc_harvesting_scenario.git
    ```

2. Open the cloned repository with `vscode`. When prompted by `vscode`, choose to reopen the repository in a container. This will build the container, install all dependencies, and set up the workspace.

3. Once inside the container, launch the scenario with the following command:
    To simulate Gazebo world with the platform (robot/robot(s) + sensors) 
    ```bash
    ROBOT_MODEL=mobile_manipulator ros2 launch scenario_bringup platform_with_world_sim.launch.py
    ```
    or

    To simulate Gazebo world only

    ```bash
    ros2 launch scenario_bringup only_world_sim.launch.py
    ``` 
![harvesting_gazebo_world](https://github.com/user-attachments/assets/928a1c9a-c802-4a4f-ac55-a50d805693e1)
