#!/usr/bin/env python3
"""Subscribes to /servo_angle and forwards each value to an Arduino over serial."""

import sys

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

import serial


class SerialBridge(Node):

    def __init__(self):
        super().__init__('serial_bridge')

        # Port/baudrate are configurable so the same node works on different setups.
        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baudrate', 9600)
        self.port = self.get_parameter('port').get_parameter_value().string_value
        self.baudrate = self.get_parameter('baudrate').get_parameter_value().integer_value

        self.serial_conn = None
        self._open_serial()

        self.subscription = self.create_subscription(
            Int32, 'servo_angle', self.listener_callback, 10)

    def _open_serial(self):
        """Try to open the serial port once. Raises on failure so the caller decides."""
        self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
        self.get_logger().info(f'Opened serial port {self.port} @ {self.baudrate} baud')

    def listener_callback(self, msg: Int32):
        angle = msg.data
        # Arduino reads with Serial.readStringUntil('\n'), so terminate with \n.
        line = f'{angle}\n'
        try:
            self.serial_conn.write(line.encode('utf-8'))
            self.get_logger().info(f'Sent angle over serial: {angle}')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to write to serial port: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        # If the port can't be opened at startup, fail fast with a clear
        # message rather than crashing later with a confusing traceback.
        node = SerialBridge()
    except serial.SerialException as e:
        print(f'[serial_bridge] Could not open serial port: {e}', file=sys.stderr)
        rclpy.shutdown()
        sys.exit(1)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.serial_conn is not None and node.serial_conn.is_open:
            node.serial_conn.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
