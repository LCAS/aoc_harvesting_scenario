cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(detach_plugin)

find_package(gazebo REQUIRED)

include_directories(${GAZEBO_INCLUDE_DIRS})
link_directories(${GAZEBO_LIBRARY_DIRS})

add_library(detach_plugin SHARED src/detach_plugin.cpp)
target_link_libraries(detach_plugin ${GAZEBO_LIBRARIES})
