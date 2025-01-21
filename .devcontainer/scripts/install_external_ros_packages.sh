#!/bin/bash

set -e -o pipefail

# Function to handle cleanup if script fails
cleanup() {
    echo "Error occurred during execution. Cleaning up..."
}
trap cleanup ERR

# Update rosdep and system packages
rosdep update
sudo apt-get update

WS=$1
echo "WS dir: ${WS}"

# Remove and recreate external_packages
if [ -d "${WS}/src/external_packages" ]; then
    echo "Removing existing external_packages directory..."
    rm -rf "${WS}/src/external_packages"
fi
mkdir -p "${WS}/src/external_packages"
cd "${WS}/src/external_packages"

# Import repositories
echo "Importing repositories with vcs..."
vcs import --force < "${WS}/src/repos/external.repos"

# Install dependencies
echo "Installing dependencies..."
rosdep install -r -y -i --from-paths .

echo "Setup complete."
