#!/usr/bin/env python3
"""Reads servo angles from the terminal and publishes them to /servo_angle."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class InputPublisher(Node):

    def __init__(self):
        super().__init__('input_publisher')
        # Publisher for the validated servo angle (0-180).
        self.publisher_ = self.create_publisher(Int32, 'servo_angle', 10)

    def run(self):
        """Blocking loop: prompt the user, validate, publish. Runs until Ctrl+C."""
        self.get_logger().info('Enter a servo angle (0-180). Press Ctrl+C to exit.')
        while rclpy.ok():
            try:
                raw = input('Angle> ')
            except EOFError:
                # Input stream closed (e.g. piped input ran out) - stop cleanly.
                break

            # Validate that the input is an integer.
            try:
                angle = int(raw)
            except ValueError:
                self.get_logger().warn(f"'{raw}' is not a valid integer, skipping.")
                continue

            # Validate the range required by the servo.
            if angle < 0 or angle > 180:
                self.get_logger().warn(f'{angle} is out of range (0-180), skipping.')
                continue

            msg = Int32()
            msg.data = angle
            self.publisher_.publish(msg)
            self.get_logger().info(f'Published angle: {angle}')


def main(args=None):
    rclpy.init(args=args)
    node = InputPublisher()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
