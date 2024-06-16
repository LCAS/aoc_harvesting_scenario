#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Update rosdep database
echo "Updating rosdep database..."
rosdep update

# Update package lists
echo "Updating package lists..."
sudo apt-get update

# Navigate to the src directory
cd "$(pwd)/src"

# Import repositories using vcs
echo "Importing repositories with vcs..."
vcs import < ../.devcontainer/repos/dogtooth.repos

# Install dependencies
echo "Installing dependencies with rosdep..."
rosdep install --from-paths . -i -y

echo "Setup complete."
