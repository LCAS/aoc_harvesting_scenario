#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Function to add a configuration line to .bashrc if it doesn't already exist
add_config_if_not_exist() {
    local config_line="$1"
    local bashrc="$HOME/.bashrc"
    
    if ! grep -F -q "$config_line" "$bashrc"; then
        echo "$config_line" >> "$bashrc"
        echo "Added: $config_line to $bashrc"
    else
        echo "Config line already exists: $config_line"
    fi
}

# Add ROS setup to .bashrc
ros_setup="source /opt/ros/humble/setup.bash"
add_config_if_not_exist "$ros_setup"

# Add local setup to .bashrc
local_setup_file="$(pwd)/install/setup.bash"
local_setup="if [ -r $local_setup_file ]; then source $local_setup_file; fi"
add_config_if_not_exist "$local_setup"

# Source the ROS setup script
source /opt/ros/humble/setup.bash

# Build the workspace with colcon
colcon build --symlink-install --continue-on-error
