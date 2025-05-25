
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml
from launch.conditions import IfCondition

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import SetParameter
import yaml

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='True')
    robot_bring_up_dir = get_package_share_directory('aoc_strawberry_scenario_bringup')
    
    ROBOT_MODEL = os.environ['ROBOT_MODEL']
    ROBOT_NAME = os.environ['ROBOT_NAME']
    rviz_config_dir = os.path.join(robot_bring_up_dir, 'rviz'
                                 , 'robots', ROBOT_MODEL + '_platform', ROBOT_NAME + '_nav2_default_view.rviz')
    print("Rviz config file {} ".format(rviz_config_dir))
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time', default_value=use_sim_time, description='Use simulation (Gazebo) clock if true'),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'),
        Node(
            package='rviz_2d_overlay_plugins',
            executable='string_to_overlay_text',
            name='string_to_overlay_text_1',
            output='screen',
            parameters=[
                {"string_topic": "/robot_behaviour/min_distance_to_boundary"},
                {"fg_color": "r"}, # colors can be: r,g,b,w,k,p,y (red,green,blue,white,black,pink,yellow)
            ],
        ),
        Node(
            package='rviz_2d_overlay_plugins',
            executable='string_to_overlay_text',
            name='string_to_overlay_text_2',
            output='screen',
            parameters=[
                {"string_topic": "/robot_operation_current_status"},
                {"fg_color": "g"}, # colors can be: r,g,b,w,k,p,y (red,green,blue,white,black,pink,yellow)
            ],
        ),
    ])
