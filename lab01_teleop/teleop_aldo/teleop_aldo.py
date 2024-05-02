import sys
import select
import tty
import termios
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class TeleopAldo(Node):
    def __init__(self):
        super().__init__('teleop_aldo')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.feedback_ = """
        Teleop Aldo Initialized!
        Use 'W' to move forward,
        'A' to move left,
        'S' to rotate 180 degrees,
        'D' to move right,
        'X' to brake,
        'Q' to quit.
        """
        print(self.feedback_)
        self.key_mapping = {'w': [0.1, 0.0], 's': [0.0, 0.5], 'a': [0.0, 0.1], 'd': [0.0, -0.1]}
        self.twist = Twist()
        self.rotation_start_time = None
        # o tempo estimado para virar o robo nestas condicoes e de 3.6.
        self.rotation_duration = 3.6

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def teleop(self):
        self.settings = termios.tcgetattr(sys.stdin)
        while rclpy.ok():
            key = self.getKey()
            if key in self.key_mapping.keys():
                self.twist.linear.x += self.key_mapping[key][0]
                self.twist.angular.z += self.key_mapping[key][1]
                self.publisher_.publish(self.twist)
                print(f"Published Twist: {self.twist}")
            elif key.lower() == 's':
                self.rotation_start_time = time.time()
                self.twist.linear.x = 0.0
                self.twist.angular.z = 0.5
                self.publisher_.publish(self.twist)
                print("Rotacionando 180 graus!")
            elif key.lower() == 'x':
                self.twist.linear.x = 0.0
                self.twist.angular.z = 0.0
                self.publisher_.publish(self.twist)
                print("Brake aplicado!")
            elif key.lower() == 'q':
                print("Saindo de Teleop Aldo!")
                break

            if self.rotation_start_time is not None:
                if time.time() - self.rotation_start_time >= self.rotation_duration:
                    self.twist.angular.z = 0.0
                    self.publisher_.publish(self.twist)
                    self.rotation_start_time = None
                    print("Rotacionando 180 graus!")

    def run(self):
        self.teleop()


def main(args=None):
    rclpy.init(args=args)
    teleop_aldo = TeleopAldo()
    teleop_aldo.run()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
