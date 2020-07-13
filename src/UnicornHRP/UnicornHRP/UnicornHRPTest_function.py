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
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
#from geometry_msgs.msg import PoseWithCovariance
#from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point

from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Vector3

class UnicornHRPTest(Node):

##################################### INIT ##############################################################
    def __init__(self):
        #Initialize publish and subscritestptions
        super().__init__('unicorn_hrp_test')
        self.HRP_publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.Unicorn_point_publisher_ = self.create_publisher(Int16, 'unicorn_point_reached', 10)
        self.HRP_subscription = self.create_subscription(Odometry, 'odom', self.odometry_callback,10)
        self.HRP_subscription = self.create_subscription(Float32, 'angle_test', self.angle_test_callback,10)
        self.HRP_subscription = self.create_subscription(Point, 'point_test', self.point_test_callback,10)
        self.HRP_subscription

        #Variable to keep the current coordinate
        self.current_coordinate = Point()
        self.current_coordinate_HRP = Point()
        self.coordinate_translation = Point()

        #Variable to keep the current linear and angular velocity
        self.HRPmsg = Twist()

        #Variable to keep current orientation
        self.current_orientation_rpy = Vector3()
        self.current_orientation_rpy_HRP = Vector3()
        self.angle_translation = Vector3()

        #Variable to keep goal cooardinate and yaw angle
        self.goal_coordinate = Point()
        self.goal_angle = 0

        #Other constants
        self.linear_velocity = 0.4
        self.angular_velocity = 0.8
        self.angular_velocity_turn = 0.5
        self.angular_velocity_proportional_gain = 0.001
        self.angular_velocity_integral_gain = 0.0001
        self.angle_tolerance = 10
        self.angle_tolerance_turn = 5
        self.angle_tolerance_maximum = 30
        self.point_tolerance = 0.25
        self.current_working_counter = 0
        self.calculate_HRP_offset = True
        self.integral_term = 0.0
        self.proportional_term = 0.0
        self.angular_error = 0.0
        self.angle_difference_stop = 1.0
        self.perform_only_turn = False
        self.within_tolerance = True
        self.current_function=0
        self.angle_outside=0
        
        #Feedback when reaching point
        self.reached_point = False
        self.reached_point_message = Int16()
  
        #Initialize velocity and command window update callbacks
        self.HRPmsg.linear.x = 0.0 
        self.HRPmsg.linear.y = 0.0
        self.HRPmsg.linear.z = 0.0
        self.HRPmsg.angular.x = 0.0  
        self.HRPmsg.angular.y = 0.0
        self.HRPmsg.angular.z = 0.0

        velocity_update_period = 0.01  # seconds
        self.velocity_update = self.create_timer(velocity_update_period, self.velocity_update_callback)
        velocity_message_period = 0.5  # seconds
        self.velocity_message = self.create_timer(velocity_message_period, self.velocity_message_callback)

        #Run program
        #self.moveToPoint(4.0,-1.0)
        #self.turn(50)

        #timer_period = 0.5  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        #self.i = 0

########################################################################################################

##################################### CALLBACKS ########################################################
    #Publish udated velocity to HRP
    def velocity_update_callback(self):  
        
        #Calculate the difference between the goal angle and current orientation
        angle_difference_calc = self.goal_angle - self.current_orientation_rpy.z
        if angle_difference_calc > 180:
            angle_difference_calc -=360
        elif angle_difference_calc < -180:
            angle_difference_calc +=360 
        self.angular_error = angle_difference_calc #For the PI regulator
        self.angle_difference = abs(angle_difference_calc)

        #If the robot are within the tolerance, try to travel straight, if it ends up too far off begin to turn again
        if self.angle_difference <= self.angle_tolerance and not self.within_tolerance:
            self.within_tolerance = True
        elif self.angle_difference > self.angle_tolerance_maximum:
            self.within_tolerance = False
            self.angle_outside = self.current_orientation_rpy.z

        #Perform only a turn
        if self.angle_difference > self.angle_tolerance_turn and self.perform_only_turn:
            self.perform_turn(self.angular_velocity_turn, self.current_orientation_rpy.z, self.goal_angle)
            self.current_function=1

        #If the robot is outside the angle tolerance it needs to turn in the right direction before moving
        elif self.angle_difference > self.angle_tolerance and not self.within_tolerance:
            self.perform_turn(self.angular_velocity, self.current_orientation_rpy.z, self.goal_angle)
            self.current_function=2
            self.integral_term = 0.0

        #If the robot has arrived at the target point
        elif abs(self.goal_coordinate.x-self.current_coordinate.x) < self.point_tolerance and abs(self.goal_coordinate.y-self.current_coordinate.y) < self.point_tolerance:
            self.HRPmsg.linear.x = 0.0
            self.HRPmsg.angular.z = 0.0
            self.integral_term = 0.0
            self.perform_only_turn = False
            self.within_tolerance = False
            self.current_function=3

            #Publish that the robot has reached the point
            if self.reached_point:
                self.reached_point = False
                self.reached_point_message.data = 1
                self.Unicorn_point_publisher_.publish(self.reached_point_message)

        #If the robot is within the angle tolerance, move to the target point
        else: 
            self.HRPmsg.linear.x = self.linear_velocity

            #PI regulator for adjusting the traveling angle closer to the goal angle
            self.proportional_term = self.angular_velocity_proportional_gain * self.angular_error
            
            self.integral_term  += self.angular_velocity_integral_gain * self.angular_error
            if self.integral_term > 0.6:
                self.integral_term = 0.6
            elif self.integral_term < -0.6:
                self.integral_term = -0.6

            #Reset the integral term instantly if we are close enough to the goal angle
            if self.angle_difference < self.angle_difference_stop:
                self.integral_term = 0.0

            self.HRPmsg.angular.z = self.proportional_term + self.integral_term
            self.current_function=4

        #Publish new velocity
        self.HRP_publisher_.publish(self.HRPmsg)

    #Show user information in command window
    def velocity_message_callback(self):
        print("\033c")
        print('Linear: "%s"' % self.HRPmsg.linear)
        print('Angular: "%s"' % self.HRPmsg.angular)
        print('Odometry HRP: "%s"' % self.current_coordinate_HRP)
        print('Odometry: "%s"' % self.current_coordinate)
        print('Coordinate translation: "%s"' % self.coordinate_translation)
        print('Goal coordinate: "%s"' % self.goal_coordinate)
        print('RPY HRP: "%s"' % self.current_orientation_rpy_HRP)
        print('RPY: "%s"' % self.current_orientation_rpy)
        print('Angle translation: "%s"' % self.angle_translation)
        print('Goal angle: "%s"' % self.goal_angle)
        print('Calculate_HRP_offset: "%s"' % self.calculate_HRP_offset)
        print('Old coords: "%s"' %self.old_coords)
        print('R: "%s"' % self.R)
        print('New coords: "%s"' %self.new_coords)
        print('Current function: "%s"' %self.current_function)
        print('Within tolerance: "%s"' %self.within_tolerance)
        print('Angle when triggering outside tolerance: "%s"' %self.angle_outside)
        print('Angle difference abs: "%s"' %self.angle_difference)
        print('Integral term: "%s"' %self.integral_term)
        print('Proportional term: "%s"' %self.proportional_term)
        print('Angle error: "%s"' %self.angular_error)
        

        #self.get_logger().info('Linear: "%s"' % HRPmsg.linear)
        #self.get_logger().info('Angular: "%s"' % HRPmsg.angular)
        #self.get_logger().info('Odometry data: "%s"' % self.curPoint)

    #Update current coordinates and orientation from HRP on callback
    def odometry_callback(self,msg):
        #Get HRP position
        self.current_coordinate_HRP = msg.pose.pose.position
        
        #Get HRP orientation by converting pose in quaternions to roll pitch yaw
        rpy_angles = self.quaternion_to_euler_deg(msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, 
            msg.pose.pose.orientation.z, msg.pose.pose.orientation.w)
        self.current_orientation_rpy_HRP.x = rpy_angles[0]
        self.current_orientation_rpy_HRP.y = rpy_angles[1]
        self.current_orientation_rpy_HRP.z = rpy_angles[2]

        #First time calculate the translation and rotation offset between HRP and our own coordinate system
        if self.calculate_HRP_offset == True:
            self.calculate_HRP_offset = False
            self.coordinate_translation = self.current_coordinate_HRP
            #self.angle_translation = self.current_orientation_rpy_HRP
            self.angle_translation.x = self.current_orientation_rpy_HRP.x
            self.angle_translation.y = self.current_orientation_rpy_HRP.y
            self.angle_translation.z = self.current_orientation_rpy_HRP.z
            print("First time offset")

        #Calculate orientation using the rotation offset
        self.current_orientation_rpy.x = self.calculate_translated_angles(self.current_orientation_rpy_HRP.x, self.angle_translation.x)
        self.current_orientation_rpy.y = self.calculate_translated_angles(self.current_orientation_rpy_HRP.y, self.angle_translation.y)
        self.current_orientation_rpy.z = self.calculate_translated_angles(self.current_orientation_rpy_HRP.z, self.angle_translation.z)

        #Current coordinate with the translation offset to get to our own coordinate system
        current_coordinate_trans_x = self.current_coordinate_HRP.x - self.coordinate_translation.x
        current_coordinate_trans_y = self.current_coordinate_HRP.y - self.coordinate_translation.y
        current_coordinate_trans_z = self.current_coordinate_HRP.z - self.coordinate_translation.z

        new_coordinates = self.perform_rpy_rotation(current_coordinate_trans_x,current_coordinate_trans_y,current_coordinate_trans_z,self.angle_translation.x,self.angle_translation.y,self.angle_translation.z)
        self.current_coordinate.x = new_coordinates[0]
        self.current_coordinate.y = new_coordinates[1]
        self.current_coordinate.z = new_coordinates[2]

    def angle_test_callback(self,msg):
        self.turn(msg.data)
        self.reached_point = True

    def point_test_callback(self,msg):
        self.moveToPoint(msg.x,msg.y)
        self.reached_point = True

##################################### MOVEMENT ######################################################s###

    #Move HRP from one point to another
    def moveToPoint(self, target_x_coordinate, target_y_coordinate):
        self.goal_angle = np.rad2deg(np.arctan2(target_y_coordinate-self.current_coordinate.y,target_x_coordinate-self.current_coordinate.x))
        self.goal_coordinate.x = target_x_coordinate
        self.goal_coordinate.y = target_y_coordinate
        self.goal_coordinate.z = 0.0

    #Turn HRP from one angle to another
    def turn(self, target_angle):
        self.goal_angle = target_angle
        self.perform_only_turn = True

    #Perform a turn in the right direction and with desired speed
    def perform_turn(self, velocity, current_orientation, turn_goal_angle):
        # Decide which way to turn by calculating the shortest signed angle
        turn_direction = turn_goal_angle-current_orientation
        if turn_direction >= 180:
            turn_direction -=360
        elif turn_direction <= -180:
            turn_direction +=360 
    
        #Set velocity
        if turn_direction >= 0:
            self.HRPmsg.angular.z = velocity
        else:
            self.HRPmsg.angular.z = -velocity
        self.HRPmsg.linear.x = 0.0

########################################################################################################

##################################### OTHER FUNCTIONS ##################################################

    #Convert quaternions to roll pitch yaw angles in deg
    def quaternion_to_euler_deg(self, x, y, z, w):
        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x**2 + y**2)
        roll = np.rad2deg(np.arctan2(sinr_cosp, cosr_cosp))

        sinp = 2 * (w * y - z * x)
        if abs(sinp) >=1:
            pitch = np.rad2deg(np.sign(sinp) * np.pi/2)
        else:
            pitch = np.rad2deg(np.arcsin(sinp))

        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y**2 + z**2)
        yaw = np.rad2deg(np.arctan2(siny_cosp, cosy_cosp))

        return roll, pitch, yaw

    def calculate_translated_angles(self, current_orientation_HRP, angle_translation_HRP):
        current_orientation = current_orientation_HRP - angle_translation_HRP
        
        if current_orientation >= 180:
            current_orientation -=360
        elif current_orientation <= -180:
            current_orientation +=360

        return current_orientation

    def perform_rpy_rotation(self,x_coord,y_coord,z_coord,r_angle,p_angle,y_angle):
        roll = np.deg2rad(r_angle)
        pitch = np.deg2rad(p_angle)
        yaw = np.deg2rad(y_angle)
        c_r, s_r = np.cos(roll), np.sin(roll)
        c_p, s_p = np.cos(pitch), np.sin(pitch)
        c_y, s_y = np.cos(yaw), np.sin(yaw)

        self.R = np.array((
            (c_y*c_p,   c_y*s_p*s_r-s_y*c_r,    c_y*s_p*c_r+s_y*s_r),
            (s_y*c_p,   s_y*s_p*s_r+c_y*c_r,    s_y*s_p*c_r-c_y*s_r),
            (-s_p,      c_p*s_r,                c_p*c_r)))

        #self.R = np.array((
        #    (c_y,   -s_y,   0),
        #    (s_y,   c_y,    0),
        #    (0,     0,      1)))

        self.old_coords = np.array(((x_coord),(y_coord),(z_coord)))
        self.new_coords = np.matmul(np.transpose(self.R),self.old_coords)

        return self.new_coords


########################################################################################################

def main(args=None):
    rclpy.init(args=args)

    unicorn_hrp_test = UnicornHRPTest()

    rclpy.spin(unicorn_hrp_test)

    unicorn_hrp_test.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
