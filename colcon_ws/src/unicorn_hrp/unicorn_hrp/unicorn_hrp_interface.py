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

from hrp_msgs.msg import HrpMove as UnicornMove

class UnicornHRP_TRACK(Node):

##################################### INIT ##############################################################
    def __init__(self):
        #Initialize publishers
        super().__init__('unicorn_hrp_track')
        self.Unicorn_soft_reset_publisher_ = self.create_publisher(Float32, 'unicorn_hrp_soft_reset', 10)
        self.Unicorn_hrp_move_publisher_ = self.create_publisher(UnicornMove, 'unicorn_hrp_move', 10)

        #Message variables
        self.soft_reset_message = Float32()
        self.unicorn_hrp_move_message = UnicornMove()

        #Keep current state
        self.current_state = 0 #0=idle, 1=executing, 2=finished, 3=error

        #Variable to keep index of current point
        self.index = -1
        self.first_command_sent = False
        self.track_finished = False

        #Points, (x-coord / y-coord / angle=[-180,180] (200 dont care about angle, -200 reverse) / linear-velocity / angular-velocity / linear-velocity during turn)
        
        self.points = np.array([[5.0,    0.0,    200],
                                [6.0,    -1.0,   200],
                                [7.5,    -1.0,   200],
                                [7.5,    0.0,    200],
                                [7.5,    0.0,     15],
                                [1.0,    0.15,   200],
                                [0.0,    0.15,   200],
                                [0.1,    -1.5,   200],
                                [0.0,    0.0,    200],
                                [-2.0,   0.0,    200],
                                [-2.0,   0.8,    200],
                                [-2.0,   0.8,    -90],
                                [0.5,    0.0,   -200],
                                [-2.0,   -0.15,  200],  
                                [0.0,    -0.15,  200],
                                [0.0,    0.6,    200],
                                [0.0,    0.6,      0]])
        '''
        self.points = np.array([[0.5,   0.0,    -200],
                                [0.0,   0.0,    90],
                                [0.0,   0.0,    0]])'''
                                

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
            #self.publish_new_command(self.points[self.index,:])
            self.publish_move_message(self.points[self.index,:])
        elif self.current_state == 0 and not self.first_command_sent and self.index < self.points.shape[0]-1:
            self.index += 1
            self.first_command_sent == True
            #self.publish_new_command(self.points[self.index,:])
            self.publish_move_message(self.points[self.index,:])
        elif self.index == self.points.shape[0]-1:
            self.track_finished = True

    #Show user information in command window
    def velocity_message_callback(self):
        print("\033c")
        print("################# USER INFO ################")

        if self.current_state == 0:
            print("Current state: Idle")
        elif self.current_state == 1:
            print("Current state: Executing")
        elif self.current_state == 2:
            print("Current state: Finished")
        elif self.current_state == 3:
            print("Current state: Blocked")
        elif self.current_state == 4:
            print("Current state: Stopped")
        else:
            print("Current state: Faulty state")

        print("Current point index", self.index, " / ", self.points.shape[0]-1)
        print("current point: [", self.points[self.index,0], ",", self.points[self.index,1], "]")
        #print('Current point: "%s"' %self.points[self.index,1:2])

        if self.points[self.index,0] == 200 and self.current_state == 1:
            print('Current command type: Moving')
        elif self.points[self.index,0] == -200 and self.current_state == 1:
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
    def publish_move_message(self,data):
        self.unicorn_hrp_move_message.x = data[0]
        self.unicorn_hrp_move_message.y = data[1]
        self.unicorn_hrp_move_message.angle = data[2]
        self.Unicorn_hrp_move_publisher_.publish(self.unicorn_hrp_move_message)

########################################################################################################

def main(args=None):
    rclpy.init(args=args)

    unicorn_hrp_track = UnicornHRP_TRACK()

    rclpy.spin(unicorn_hrp_track)

    unicorn_hrp_track.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
