from launch import LaunchDescription
from launch.actions import GroupAction, DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess, RegisterEventHandler
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration, Command, FindExecutable, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.event_handlers import OnProcessStart
from launch.event_handlers import OnProcessExit
from launch.events import TimerEvent
from launch.actions import TimerAction
from ament_index_python.packages import get_package_share_directory
import os
import xacro
from launch.event_handlers import OnProcessStart
from moveit_configs_utils import MoveItConfigsBuilder
from launch.conditions import IfCondition

import yaml
from launch.actions import SetEnvironmentVariable

def generate_launch_description():
    ld = LaunchDescription()
    
    scenario_bring_up_dir = get_package_share_directory('scenario_bringup')

    if 'GAZEBO_MODEL_PATH' in os.environ:
        model_path = os.environ['GAZEBO_MODEL_PATH'] + ':' + os.path.join(scenario_bring_up_dir, 'models')
    else:
        model_path = os.path.join(scenario_bring_up_dir, 'models')
    set_model_path_env = SetEnvironmentVariable(name='GAZEBO_MODEL_PATH', value=model_path)

    # world_file = os.path.join(scenario_bring_up_dir, 'worlds', 'gazebo_riseholme_interactive_perception_01.world') # for interactive perception studies
    # world_file = os.path.join(scenario_bring_up_dir, 'worlds', 'gazebo_riseholme_with_interactable_plant_02.world') # working version of the dynamic environment (at the beginning of row)
    # world_file = os.path.join(scenario_bring_up_dir, 'worlds', 'gazebo_riseholme_with_interactable_plant_01.world') # working version of the dynamic environment (end of row)
    world_file = os.path.join(scenario_bring_up_dir, 'worlds', 'gazebo_riseholme_with_static_plants.world') # working version of the static environment
    # world_file = os.path.join(scenario_bring_up_dir, 'worlds', 'gazebo_riseholme_no_plants.world') # without plants

    x_arg = DeclareLaunchArgument(
        'x_pose', 
        default_value='0.0', 
        description='X position of the robot')
    y_arg = DeclareLaunchArgument(
        'y_pose', 
        default_value='0.0', 
        description='Y position of the robot')
    z_arg = DeclareLaunchArgument(
        'z_pose', 
        default_value='0.01', 
        description='Z position of the robot')
    R_arg = DeclareLaunchArgument(
        'roll', 
        default_value='0.0', 
        description='Roll orientation of the robot')
    P_arg = DeclareLaunchArgument(
        'pitch', 
        default_value='0.0', 
        description='Pitch orientation  of the robot')
    Y_arg = DeclareLaunchArgument(
        'yaw', 
        default_value='1.45', 
        description='Yaw orientation  of the robot')
    arm_name_arg = DeclareLaunchArgument(
        'name', 
        default_value='ur', 
        description='Name of the arm')
    arm_type_arg = DeclareLaunchArgument(
        'ur_type', 
        default_value='ur5', 
        description='Type of UR arm')
    safety_lim_arg = DeclareLaunchArgument(
        'safety_limits', 
        default_value='true', 
        description='Enable safety limits')
    arm_tf_prefix_arg = DeclareLaunchArgument(
        'tf_prefix', 
        default_value='', 
        description='TF prefix for the arm')
    mobile_base_prefix_arg = DeclareLaunchArgument(
        'prefix', 
        default_value='', 
        description='prefix for the mobile base')
    use_gazebo_arg = DeclareLaunchArgument(
        'use_gazebo', 
        default_value='true', 
        description='Use Gazebo simulation')
    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz', 
        default_value='true', 
        description='Use RViz tool')
    use_base_arg = DeclareLaunchArgument(
        'use_base', 
        default_value='true', 
        description='Include the base in the simulation')
    use_arm_arg = DeclareLaunchArgument(
        'use_arm', 
        default_value='true',
        description='Include the arm in the simulation')
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')

    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')
    z_pose = LaunchConfiguration('z_pose', default='0.01')
    roll = LaunchConfiguration('roll', default='0.0')
    pitch = LaunchConfiguration('pitch', default='0.0')
    yaw = LaunchConfiguration('yaw', default='1.45')

    use_rviz = LaunchConfiguration('use_rviz', default='true')
    use_gazebo = LaunchConfiguration('use_gazebo', default='true')
    use_base = LaunchConfiguration('use_base', default='true')
    use_arm = LaunchConfiguration('use_arm', default='true')
    tf_prefix = LaunchConfiguration('tf_prefix', default='')
    prefix = LaunchConfiguration('prefix', default='')
    safety_limits = LaunchConfiguration('safety_limits', default='true')
    ur_type = LaunchConfiguration('ur_type', default='ur5')
    name = LaunchConfiguration('name', default='ur')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]),
        " ",
        PathJoinSubstitution([
            FindPackageShare("mobile_manipulator_pltf_bringup"),
            "config", "ur.urdf.xacro"
        ]),
        " ",
        "is_sim:=", use_sim_time,
        " ",
        "use_base:=", use_base,
        " ",
        "use_arm:=", use_arm,
        " ",
        "name:=", name,
        " ",
        "ur_type:=", ur_type,
        " ",
        "safety_limits:=", safety_limits,
        " ",
        "tf_prefix:=", tf_prefix,
        " ",
        "prefix:=", prefix,
        " ",
        "sim_gazebo:=", use_gazebo,
    ])

    # Build MoveIt config
    moveit_config = (
        MoveItConfigsBuilder("mobile_manipulator", package_name="mobile_manipulator_pltf_bringup")
        .robot_description_semantic(file_path="config/ur.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .planning_scene_monitor(
            publish_robot_description=True,
            publish_robot_description_semantic=True,
            publish_planning_scene=True
        )
        .planning_pipelines(
            pipelines=["ompl", "chomp", "pilz_industrial_motion_planner"]
        )
        .to_moveit_configs()
    )

    # Inject robot_description manually
    # moveit_config.robot_description = {
    #     "robot_description": robot_description_content
    # }
    moveit_config.robot_description["robot_description"] = robot_description_content

    # Include Gazebo launch file
    gazebo_launch_file = os.path.join(
        get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
        launch_arguments={
            'use_sim_time': 'true',
            'debug': 'false',
            'gui': 'true',
            'paused': 'true',
            'world' : world_file
        }.items()
    )

    rviz_config_path = os.path.join(
        get_package_share_directory("mobile_manipulator_pltf_bringup"),
        "config",
        "moveit.rviz",
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_path],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
            {'use_sim_time': use_sim_time}
        ],
        condition=IfCondition(use_rviz)
    )

    # spawn the robot
    spawn_the_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'mobile_manipulator',
            '-topic', 'robot_description',
            '-x', x_pose,
            '-y', y_pose,
            '-z', z_pose,
            '-R', roll,
            '-P', pitch,
            '-Y', yaw,
        ],
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        condition=IfCondition(use_gazebo)
    )

    # controller manager
    joint_controllers_file = os.path.join(
        get_package_share_directory('mobile_manipulator_pltf_description'), 'config', 'ur5_controllers_gripper.yaml'
    )
    controller_manager_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[moveit_config.robot_description, joint_controllers_file],
        output='screen',
        remappings=[
            ("~/robot_description", "/robot_description"),
        ],
    )

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[moveit_config.robot_description, {'use_sim_time': use_sim_time}],
        output='screen'
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output="screen",
    )

    ackermann_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["ackermann_like_controller", "--controller-manager", "/controller_manager"],
        output="screen",
        condition=IfCondition(use_base)
    )

    arm_trajectory_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_trajectory_controller", "--controller-manager", "/controller_manager"],
        output="screen",
        condition=IfCondition(use_arm)
    )

    gripper_position_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["gripper_position_controller", "--controller-manager", "/controller_manager"],
        output="screen",
        condition=IfCondition(use_arm)
    )

    sensor_yaml_path = os.path.join(
        get_package_share_directory("mobile_manipulator_pltf_bringup"),
        "config",
        "sensors_3d.yaml"
    )

    with open(sensor_yaml_path, "r") as f:
        sensor_config = yaml.safe_load(f)


    use_sim_time={"use_sim_time": True}
    config_dict = moveit_config.to_dict()
    config_dict.update(use_sim_time)

    config_dict["move_group"] = {
        **config_dict.get("move_group", {}),
        "sensors": sensor_config["sensors"],                   
        "default_sensor": sensor_config["default_sensor"],     
        "octomap_frame": "base_link",                               
        "octomap_resolution": 0.02,
        "max_range": 5.0
    }

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[config_dict],
        arguments=["--ros-args", "--log-level", "info"],
    )

    delay_joint_state_broadcaster = RegisterEventHandler(
        OnProcessStart(
            target_action=controller_manager_node,
            on_start=[joint_state_broadcaster_spawner],
        )
    )

    delay_base_controller = RegisterEventHandler(
            OnProcessStart(
                target_action=joint_state_broadcaster_spawner,
                on_start=[ackermann_controller_spawner]
            )
        )

    delay_arm_controller = RegisterEventHandler(
            OnProcessStart(
                target_action=joint_state_broadcaster_spawner,
                on_start=[arm_trajectory_controller_spawner]
            )
        )

    delay_gripper_controller = RegisterEventHandler(
            OnProcessStart(
                target_action=joint_state_broadcaster_spawner,
                on_start=[gripper_position_controller_spawner]
            )
        )

    delay_rviz_node = RegisterEventHandler(
        OnProcessStart(
            target_action=robot_state_publisher,
            on_start=[rviz_node],
        )
    )

    # Launch Description
    ld.add_action(x_arg)
    ld.add_action(y_arg)
    ld.add_action(z_arg)
    ld.add_action(R_arg)
    ld.add_action(P_arg)
    ld.add_action(Y_arg)
    ld.add_action(use_arm_arg)
    ld.add_action(use_base_arg)
    ld.add_action(use_gazebo_arg)
    ld.add_action(use_rviz_arg)
    ld.add_action(use_sim_time_arg)
    ld.add_action(arm_tf_prefix_arg)
    ld.add_action(mobile_base_prefix_arg)
    ld.add_action(safety_lim_arg)
    ld.add_action(arm_type_arg)
    ld.add_action(arm_name_arg)
    ld.add_action(set_model_path_env)
    ld.add_action(gazebo)
    ld.add_action(controller_manager_node)  # has to be loaded first
    ld.add_action(move_group_node)
    ld.add_action(spawn_the_robot)
    ld.add_action(robot_state_publisher)
    # delay of the controllers
    ld.add_action(delay_joint_state_broadcaster)
    ld.add_action(delay_arm_controller)
    ld.add_action(delay_gripper_controller)
    ld.add_action(delay_base_controller)
    ld.add_action(delay_rviz_node)

    return ld

