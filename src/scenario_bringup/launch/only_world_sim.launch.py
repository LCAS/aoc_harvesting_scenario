from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os 
from ament_index_python.packages import get_package_share_directory
from launch.actions import SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch.actions import SetEnvironmentVariable
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    
    # Define world file
    scenario_bring_up_dir = get_package_share_directory('scenario_bringup')
    world_file = os.path.join(scenario_bring_up_dir, 'worlds', 'gazebo_world.world')
    world_path = LaunchConfiguration('world_path', default=world_file)

    # Gazebo Models
    if 'GAZEBO_MODEL_PATH' in os.environ:
        model_path =  os.environ['GAZEBO_MODEL_PATH'] + ':' + os.path.join(scenario_bring_up_dir, 'models')
    else:
        model_path =  os.path.join(scenario_bring_up_dir, 'models')

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={'world': world_path}.items()
    )

    # Launch them all!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument(
            'world_path',
            default_value=world_path,
            description='Gazebo sim world'),
        SetEnvironmentVariable(name='GAZEBO_MODEL_PATH', value=model_path),
        gazebo
    ])