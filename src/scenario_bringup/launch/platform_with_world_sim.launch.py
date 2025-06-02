from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
import os 
from ament_index_python.packages import get_package_share_directory
from launch.actions import SetEnvironmentVariable
from launch.substitutions import Command, EnvironmentVariable, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from pathlib import Path
from launch.actions import SetEnvironmentVariable
from launch.actions import DeclareLaunchArgument
import sys

def generate_launch_description():

    if ("ROBOT_MODEL" not in os.environ) :
        print("ROBOT_MODEL must be set before execuing this launch file")
        sys.exit(0) 
    
    ROBOT_MODEL = os.environ['ROBOT_MODEL']
    
    scenario_bring_up_dir = get_package_share_directory('scenario_bringup')
    launch_file_dir = os.path.join(scenario_bring_up_dir, 'launch')  

    world_file = os.path.join(scenario_bring_up_dir, 'worlds', 'gazebo_riseholme_harvesting_01.world')
    # world_file = os.path.join(scenario_bring_up_dir, 'worlds', 'empty_world.world')
    # world_file = PathJoinSubstitution([FindPackageShare("dogtooth_gazebo"), "worlds", "terrain_1.world"],)
    
    robot_gazebo_dir = os.path.join(get_package_share_directory(ROBOT_MODEL + '_pltf_gazebo'), 'launch')
    robot_launch = "launch_sim.launch.py"

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default='25.5')
    y_pose = LaunchConfiguration('y_pose', default='2.5')
    # x_pose = LaunchConfiguration('x_pose', default='-15.2')
    # y_pose = LaunchConfiguration('y_pose', default='2.7')
    # x_pose = LaunchConfiguration('x_pose', default='13.2')
    # y_pose = LaunchConfiguration('y_pose', default='7.06')
    roll = LaunchConfiguration('roll', default='0.0')
    pitch = LaunchConfiguration('pitch', default='0.0')
    yaw = LaunchConfiguration('yaw', default='-83.07888')
    world_path = LaunchConfiguration('world_path', default=world_file)

    health_monitor_params_file = LaunchConfiguration('health_monitor_params_file', default=os.path.join(scenario_bring_up_dir, 'config'
            , 'robots', ROBOT_MODEL + '_platform', 'generic', 'cfg_topics_monitor.yaml'))

    if 'GAZEBO_MODEL_PATH' in os.environ:
        model_path =  os.environ['GAZEBO_MODEL_PATH'] + ':' + os.path.join(scenario_bring_up_dir, 'models')
    else:
        model_path =  os.path.join(scenario_bring_up_dir, 'models')

    # Launch them all!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument(
            'x_pose',
            default_value=x_pose,
            description='Start pose, x'),
        DeclareLaunchArgument(
            'y_pose',
            default_value=y_pose,
            description='Start pose, y'),
        DeclareLaunchArgument(
            'roll',
            default_value='0.0',
            description='Start roll angle'),
        DeclareLaunchArgument(
            'pitch',
            default_value='0.0',
            description='Start pitch angle'),
        DeclareLaunchArgument(
            'yaw',
            default_value=yaw,
            description='Start yaw angle'),
        DeclareLaunchArgument(
            'world_path',
            default_value=world_path,
            description='Gazebo sim world'),
        DeclareLaunchArgument(
            'with_gui',
            default_value='true',
            description='Run Gazebo Sim GUI'),
        SetEnvironmentVariable(name='GAZEBO_MODEL_PATH', value=model_path),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([robot_gazebo_dir, '/', robot_launch]),
            launch_arguments={
                    'world_path': world_path, 
                    'x_pose': x_pose,
                    'y_pose': y_pose,
                    'roll': roll,
                    'pitch': pitch,
                    'yaw': yaw,
                    'use_sim_time': use_sim_time
                }.items(),
        ),
    ])
