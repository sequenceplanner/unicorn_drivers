# Note will only work on foxy, will need to be slightly rewritten to launch using eloquent
# See: https://index.ros.org/doc/ros2/Tutorials/Launch-Files/Creating-Launch-Files/

# Will make stdout unaccesible, if required add namespace via ros-args (see readme)

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='unicorn_hrp',
            namespace='/hrp/hrp1',
            executable='unicorn_hrp_controller',
            name='hrp_interface'
        )
    ])