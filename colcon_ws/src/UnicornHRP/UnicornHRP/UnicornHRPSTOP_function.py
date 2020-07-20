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

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
#from geometry_msgs.msg import PoseWithCovariance
#from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point

from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Vector3

class UnicornHRP_STOP(Node):

##################################### INIT ##############################################################
    def __init__(self):
        #Initialize publish and subscriptions
        super().__init__('unicorn_hrp_stop')
        self.HRP_publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        #Variable to keep the current linear and angular velocity
        self.HRPmsg = Twist()

        #Initialize velocity and command window update callbacks
        self.HRPmsg.linear.x = 0.0 
        self.HRPmsg.linear.y = 0.0
        self.HRPmsg.linear.z = 0.0
        self.HRPmsg.angular.x = 0.0  
        self.HRPmsg.angular.y = 0.0
        self.HRPmsg.angular.z = 0.0

        velocity_update_period = 0.01  # seconds
        self.velocity_update = self.create_timer(velocity_update_period, self.velocity_update_callback)

########################################################################################################

##################################### CALLBACKS ########################################################
    #Publish udated velocity to HRP
    def velocity_update_callback(self):
        self.HRP_publisher_.publish(self.HRPmsg)
        print("\033c")
        print("STOPPING!")

########################################################################################################

def main(args=None):
    rclpy.init(args=args)

    unicorn_hrp_stop = UnicornHRP_STOP()

    rclpy.spin(unicorn_hrp_stop)

    unicorn_hrp_stop.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
