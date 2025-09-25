# AOC HARVESTING SCENARIO

AOC harvesting scenario for mobile manipulators, including interactable plants, part of the Agri-OpenCore (AOC) project

To get started with this scenario, follow these steps:

1. Clone the repository into your workspace:
    ```bash
    git clone https://github.com/LCAS/aoc_harvesting_scenario.git
    ```

2. Open the cloned repository with `vscode`. When prompted by `vscode`, select reopen the repository in a container. This will build the container, install all dependencies, and set up the workspace.

3. Once inside the container, launch the scenario with the following command:

    To simulate Gazebo world with the platform (robot/robot(s) + sensors) 
    ```bash
    ROBOT_MODEL=mobile_manipulator ros2 launch scenario_bringup platform_with_world_sim.launch.py
    ```
    or

    ```bash
    ros2 launch scenario_bringup platform_with_world_sim.launch.py use_base:=true use_arm:=true x_pose:=19.0 y_pose:=-24.15 yaw:=-83.07888
    ``` 
    
**Simulation world with strawberry plants**

[Strawberry Harvesting World v01](https://github.com/user-attachments/assets/238959a4-01b7-4c06-aaf1-92095951ec3f)

**Simulation world with platform**

[Strawberry Harvesting World with Hunter Platform v01](https://github.com/user-attachments/assets/8790b2e0-4e16-4bf9-900a-ec0509c4b939)
