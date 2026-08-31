"""Launches input_publisher and serial_bridge together.

Usage:
  ros2 launch serial_demo serial_demo_launch.py
  ros2 launch serial_demo serial_demo_launch.py port:=/dev/ttyACM0 baudrate:=115200
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Expose serial port/baudrate as launch arguments, forwarded to serial_bridge's params.
    port_arg = DeclareLaunchArgument(
        'port', default_value='/dev/ttyUSB0',
        description='Serial port the Arduino is connected to')
    baudrate_arg = DeclareLaunchArgument(
        'baudrate', default_value='9600',
        description='Serial baudrate, must match the Arduino sketch')

    input_publisher_node = Node(
        package='serial_demo',
        executable='input_publisher',
        name='input_publisher',
        output='screen',
        emulate_tty=True,  # needed so input() prompts/echoes correctly when launched
    )

    serial_bridge_node = Node(
        package='serial_demo',
        executable='serial_bridge',
        name='serial_bridge',
        output='screen',
        parameters=[{
            'port': LaunchConfiguration('port'),
            'baudrate': LaunchConfiguration('baudrate'),
        }],
    )

    return LaunchDescription([
        port_arg,
        baudrate_arg,
        input_publisher_node,
        serial_bridge_node,
    ])
