#!/bin/bash

set -e -x  # Exit immediately if a command exits with a non-zero status

cd ${COLCON_WS}

# Source the ROS setup script
source /opt/ros/humble/setup.bash

# Build the workspace with colcon
colcon build 