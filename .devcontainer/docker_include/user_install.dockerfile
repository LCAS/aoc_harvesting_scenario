# Install external repos 
COPY .devcontainer/repos ${COLCON_WS}/src/repos

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Clone the Livox-SDK2 repository, build, and install
RUN echo "Installing livox_sdk2..." && \
    git clone --branch v0.0.0 --depth 1 https://github.com/LCAS/Livox-SDK2.git "$REPO_DIR/Livox-SDK2" && \
    cd "$REPO_DIR/Livox-SDK2" && \
    mkdir -p build && \
    cd build && \
    rm -rf * && \
    cmake .. && \
    make -j$(nproc) && \
    sudo make install && \
    echo "livox_sdk2 installed successfully." && \
    cd "$REPO_DIR" && \
    rm -rf "$REPO_DIR/Livox-SDK2"

USER $USER

# Copy the script to checkout public git repos and make it executable
COPY .devcontainer/scripts/install_external_ros_packages.sh ${COLCON_WS}/src/install_external_ros_packages.sh
# Make the script executable and run it, then remove it
RUN /bin/bash -c '${COLCON_WS}/src/install_external_ros_packages.sh ${COLCON_WS}' && \
    sudo rm -f ${COLCON_WS}/src/install_external_ros_packages.sh && \
    sudo rm -f -r ${COLCON_WS}/src/repos

USER root