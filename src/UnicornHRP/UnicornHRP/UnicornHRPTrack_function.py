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
        #Initialize publishers
        super().__init__('unicorn_hrp_track')
        self.Unicorn_angle_publisher_ = self.create_publisher(Float32, 'angle_test', 10)
        self.Unicorn_point_publisher_ = self.create_publisher(Point, 'point_test', 10)
        self.Unicorn_reverse_publisher_ = self.create_publisher(Float32, 'reverse_test', 10)
        self.Unicorn_soft_reset_publisher_ = self.create_publisher(Float32, 'soft_reset', 10)
        self.Unicorn_update_linear_velocity_publisher_ = self.create_publisher(Float32, 'linear_velocity', 10)

        #Message variables
        self.angle_message = Float32()
        self.point_message = Point()
        self.reverse_message = Float32()
        self.soft_reset_message = Float32()
        self.linear_velocity_message = Float32()

        #Keep current state
        self.current_state = 0 #0=idle, 1=executing, 2=finished, 3=error

        #Variable to keep index of current point
        self.index = -1
        self.first_command_sent = False
        self.track_finished = False

        #Points, (point=-200,reverse=200 / distance, angle=[-180,180] / x-coord / y-coord)
        
        self.points = np.array([[-200,  5.0,    0.0,    0.6],
                                [-200,  6.0,    -1.0,   0.4],
                                [-200,  7.5,    -1.0,   0.4],
                                [-200,  7.5,    0.0,    0.4],
                                [15.0,  0.0,    0.15,   0.0],
                                [-200,  1.0,    0.15,   0.6],
                                [-200,  0.0,    0.15,   0.4],
                                [-200,  0.1,    -1.5,   0.4],
                                [-200,  0.0,    0.15,   0.4],
                                [-200,  -2.0,   0.15,   0.4],
                                [-200,  -2.0,   0.8,    0.4],
                                [-90.0, 0,      0,      0.0],
                                [200,   0.5,    0.0,    0.0],
                                [-200,  -2.0,   0.0,    0.4],
                                [-200,  0.0,    0.0,    0.4],
                                [-200,  0.0,    0.6,    0.4],
                                [0.0,   0,      0,      0.0]])
        '''                       
        self.points = np.array([[-200,  2.0,    0.0],
                                [200,   2.0,   0.0]])
                    '''        

        #Let other nodes set up their subscriptions
        print("Initializing...")
        time.sleep(0.5)

        #Soft reset our node
        self.soft_reset_message.data = 1.0
        self.Unicorn_soft_reset_publisher_.publish(self.soft_reset_message)
        time.sleep(1.0)

        #Initialize subscriptions after everything else has been initialized (nessecary)
        self.HRP_subscription = self.create_subscription(Int16, 'unicorn_current_state', self.current_state_callback,10)
        self.HRP_subscription

        velocity_message_period = 1.0  # seconds
        self.velocity_message = self.create_timer(velocity_message_period, self.velocity_message_callback)

########################################################################################################

##################################### CALLBACKS ########################################################
    #Publish new command to HRP
    def current_state_callback(self, msg):
        self.current_state = msg.data
        if self.current_state == 2 and self.index < self.points.shape[0]-1:
            self.index += 1
            self.publish_new_command(self.points[self.index,:])
        elif self.current_state == 0 and not self.first_command_sent and self.index < self.points.shape[0]-1:
            self.index += 1
            self.first_command_sent == True
            self.publish_new_command(self.points[self.index,:])
        elif self.index == self.points.shape[0]-1:
            self.track_finished = True

    #Show user information in command window
    def velocity_message_callback(self):
        print("\033c")
        print("################# DEBUG INFO #################")

        if self.current_state == 0:
            print("Current state: Idle")
        elif self.current_state == 1:
            print("Current state: Executing")
        elif self.current_state == 2:
            print("Current state: Finished")
        elif self.current_state == 3:
            print("Current state: Error")
        else:
            print("Current state: Faulty state")

        print("Current point index", self.index, " / ", self.points.shape[0]-1)
        print("current point: [", self.points[self.index,1], ",", self.points[self.index,2], "]")
        #print('Current point: "%s"' %self.points[self.index,1:2])

            
        if self.points[self.index,0] == -200 and self.current_state == 1:
            print('Current command type: Moving')
        elif self.points[self.index,0] == 200 and self.current_state == 1:
            print('Current command type: Reversing')
        elif self.current_state == 1:
            print('Current command type: Turning')
        else:
            print('Current command type: None')
        
        if self.track_finished:
            print("Track finished: True")
        else:
            print("Track finished: False")

        print("##############################################")

########################################################################################################

##################################### OTHER FUNCTIONS ##################################################
    def publish_new_command(self,command):
        #Publish point
        if command[0] == -200:
            self.linear_velocity_message.data = command[3]
            self.Unicorn_update_linear_velocity_publisher_.publish(self.linear_velocity_message)
            self.point_message.x = command[1]
            self.point_message.y = command[2]
            self.point_message.z = 0.0
            self.Unicorn_point_publisher_.publish(self.point_message)
            #print('Publishing point: "%s"' %self.point_message) 
        #Publish reverse
        elif command[0] == 200:
            self.reverse_message.data = command[1]
            self.Unicorn_reverse_publisher_.publish(self.reverse_message)
            #print('Publishing reverse: "%s"' %self.reverse_message) 
        #Publish angle
        else:
            self.angle_message.data = command[0]
            self.Unicorn_angle_publisher_.publish(self.angle_message)
            #print('Publishing angle: "%s"' %self.angle_message)

########################################################################################################

def main(args=None):
    rclpy.init(args=args)

    unicorn_hrp_track = UnicornHRP_TRACK()

    rclpy.spin(unicorn_hrp_track)

    unicorn_hrp_track.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
