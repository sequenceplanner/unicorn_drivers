# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
#from geometry_msgs.msg import PoseWithCovariance
#from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point

import subprocess
import platform

def clear():
    subprocess.Popen( "cls" if platform.system() == "Windows" else "clear", shell=True)

HRPmsg = Twist()

class UnicornHRPTest(Node):

    def __init__(self):
        super().__init__('unicorn_hrp_test')
        self.HRP_publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.HRP_subscription = self.create_subscription(Odometry, 'odom', self.listener_callback,10)
        self.HRP_subscription

        self.curPoint = Point()
        self.move()

        #timer_period = 0.5  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        #self.i = 0

    def velocity_update_callback(self):        
        self.HRP_publisher_.publish(HRPmsg)

    def velocity_message_callback(self):
        print("\033c")
        print('Linear: "%s"' % HRPmsg.linear)
        print('Angular: "%s"' % HRPmsg.angular)
        print('Odometry: "%s"' % self.curPoint)
        #self.get_logger().info('Linear: "%s"' % HRPmsg.linear)
        #self.get_logger().info('Angular: "%s"' % HRPmsg.angular)
        #self.get_logger().info('Odometry data: "%s"' % self.curPoint)


    def listener_callback(self, msg):
        self.curPoint = msg.pose.pose.position
        #self.get_logger().info('Odometry data: "%s"' % currentPos)
        #print('Odometry data: "%s"' % self.curPoint)

    def move(self):
        velocity_update_period = 0.01  # seconds
        self.velocity_update = self.create_timer(velocity_update_period, self.velocity_update_callback)
        velocity_message_period = 0.5  # seconds
        self.velocity_message = self.create_timer(velocity_message_period, self.velocity_message_callback)
        
        HRPmsg.linear.x = 0.0
        HRPmsg.linear.y = 0.0
        HRPmsg.linear.z = 0.0
        HRPmsg.angular.x = 0.0
        HRPmsg.angular.y = 0.0
        HRPmsg.angular.z = 0.0

        #while currentPos.x < 1:
        
            

def main(args=None):
    rclpy.init(args=args)

    unicorn_hrp_test = UnicornHRPTest()

    rclpy.spin(unicorn_hrp_test)

    unicorn_hrp_test.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
