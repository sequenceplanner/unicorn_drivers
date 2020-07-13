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

import numpy as np
import time

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point

class UnicornHRP_TRACK(Node):

##################################### INIT ##############################################################
    def __init__(self):
        #Initialize publish and subscriptions
        super().__init__('unicorn_hrp_track')
        self.Unicorn_angle_publisher_ = self.create_publisher(Float32, 'angle_test', 10)
        self.Unicorn_point_publisher_ = self.create_publisher(Point, 'point_test', 10)
        self.HRP_subscription = self.create_subscription(Int16, 'unicorn_point_reached', self.point_reached_callback,10)
        self.HRP_subscription = self.create_subscription(Float32, 'angle_test', self.angle_test_callback,10)
        self.HRP_subscription

        #Message variables
        self.angle_message = Float32()
        self.point_message = Point()

        #Variable to keep index of current point
        self.index = 0
        #Points, (point=-200,angle=[-180,180] / x-coord / y-coord)
        self.points = np.array([[-200,  5.0,    0.0],
                                [-200,  6.0,    -1.0],
                                [-200,  7.5,    -1.0],
                                [-200,  7.5,    0.0],
                                [15.0,  0.0,    0.15],
                                [-200,  0.0,    0.15],
                                [-200,  0.1,    -1.5],
                                [-200,  0.0,    0.15],
                                [-200,  -2.0,   0.15],
                                [-200,  -2.0,   1.0],
                                [-90.0, 0,      0]])
        
        time.sleep(0.5)

        #Initialize publisher (make the subscribers subscribe)
        self.publish_new_command([1000.0,1000.0,1000.0])

        #Publish first command
        self.publish_new_command(self.points[self.index,:])
        self.index += 1

########################################################################################################

##################################### CALLBACKS ########################################################
    #Publish udated velocity to HRP
    def point_reached_callback(self, msg):
        print("yes")
        self.publish_new_command(self.points[self.index,:])
        self.index += 1

    def angle_test_callback(self, msg):
        print('Subscribing angle: "%s"' %msg)

########################################################################################################

##################################### OTHER FUNCTIONS ##################################################
    def publish_new_command(self,command):
        #Initialize
        if command[0] == 1000:
            self.point_message.x = command[1]
            self.point_message.y = command[2]
            self.point_message.z = 0.0
            self.angle_message.data = command[0]
            self.Unicorn_point_publisher_.publish(self.point_message)
            self.Unicorn_angle_publisher_.publish(self.angle_message)
            print('Initialized')
        #Publish point
        elif command[0] == -200:
            self.point_message.x = command[1]
            self.point_message.y = command[2]
            self.point_message.z = 0.0
            self.Unicorn_point_publisher_.publish(self.point_message)
            print('Publishing point: "%s"' %self.point_message) 
        #Publish angle
        else:
            self.angle_message.data = command[0]
            self.Unicorn_angle_publisher_.publish(self.angle_message)
            print('Publishing angle: "%s"' %self.angle_message)

########################################################################################################

def main(args=None):
    rclpy.init(args=args)

    unicorn_hrp_track = UnicornHRP_TRACK()

    rclpy.spin(unicorn_hrp_track)

    unicorn_hrp_track.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
