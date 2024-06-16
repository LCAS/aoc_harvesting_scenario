import os

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    dogtooth_pltf_dir = get_package_share_directory('dogtooth_pltf_gazebo')

    use_sim_time = LaunchConfiguration('use_sim_time', default='True')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value=use_sim_time, description='Use simulation (Gazebo) clock if true'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(dogtooth_pltf_dir, 'launch', 'launch_sim.launch.py')),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),
    ])