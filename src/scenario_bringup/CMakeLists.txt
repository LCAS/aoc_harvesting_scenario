cmake_minimum_required(VERSION 3.8)
project(scenario_bringup)

# Default to C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)

install(DIRECTORY
  config launch params rviz worlds models
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
