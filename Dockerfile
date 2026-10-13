FROM ros:jazzy-ros-base-noble
ARG HOST_UID
ARG HOST_GID
RUN apt-get update && apt-get install -y --no-install-recommends \
    portaudio19-dev libasound2-plugins python3-pip python3-venv \
    python3-colcon-common-extensions python3-rosdep \
    python3-numpy python3-yaml python3-pytest python3-setuptools \
    ros-jazzy-rclpy ros-jazzy-std-msgs ros-jazzy-ament-index-python \
    ros-jazzy-launch ros-jazzy-launch-ros \
    && rm -rf /var/lib/apt/lists/*
RUN test -n "$HOST_UID" && test -n "$HOST_GID" \
    && (getent group "$HOST_GID" || groupadd --gid "$HOST_GID" voice) \
    && if getent passwd "$HOST_UID"; then \
         task_user=$(getent passwd "$HOST_UID" | cut -d: -f1); \
         usermod --home /home/voice --shell /bin/bash "$task_user"; \
       else useradd --uid "$HOST_UID" --gid "$HOST_GID" --home-dir /home/voice --shell /bin/bash voice; fi \
    && mkdir -p /home/voice && chown "$HOST_UID:$HOST_GID" /home/voice
RUN python3 -m venv --system-site-packages /opt/voice-venv
COPY requirements-dev.txt requirements.txt /tmp/voice-deps/
RUN /opt/voice-venv/bin/pip install -r /tmp/voice-deps/requirements-dev.txt
ENV PATH="/opt/voice-venv/bin:${PATH}"
ENV HOME=/home/voice
ENV ROS_LOCALHOST_ONLY=1
WORKDIR /workspace
USER ${HOST_UID}:${HOST_GID}
CMD ["bash"]
