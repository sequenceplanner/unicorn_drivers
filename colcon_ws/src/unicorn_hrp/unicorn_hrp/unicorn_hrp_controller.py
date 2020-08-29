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
from rclpy.executors import MultiThreadedExecutor

import time

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

#from unicorn_msgs.msg import UnicornMove
from hrp_msgs.msg import HrpMove as UnicornMove
from hrp_msgs.msg import HrpMeasurementSensor

class UnicornHRPTest(Node):

##################################### INIT ##############################################################
    def __init__(self):
        #Initialize publishers and subscribers
        super().__init__('unicorn_hrp_test')
        self.HRP_publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.Unicorn_current_state_publisher_ = self.create_publisher(Int16, 'unicorn_current_state', 10)
        self.HRP_subscription = self.create_subscription(Odometry, 'odom', self.odometry_callback,10)
        self.HRP_subscription = self.create_subscription(Float32, 'unicorn_hrp_soft_reset', self.soft_reset_callback,10)
        self.HRP_subscription = self.create_subscription(UnicornMove, 'unicorn_hrp_move', self.move_hrp_callback,10)
        self.HRP_subscription = self.create_subscription(Float32, 'unicorn_hrp_stop', self.stop_hrp_callback,100)
        self.HRP_subscription = self.create_subscription(HrpMeasurementSensor, 'unicorn_measurement_sensor', self.measurement_sensor_callback,10)
        self.HRP_subscription

        print("Initializing...")

        self.init_callbacks = True
        self.setup()

    #Initialize variables and callbacks, also runs during soft reset
    def setup(self):
        #Variable to keep the current coordinate
        self.current_coordinate = Point()
        self.current_coordinate_HRP = Point()
        self.coordinate_translation = Point()

        #Variable to keep the current linear and angular velocity
        self.HRPmsg = Twist()

        #Variable to keep old Hrpmove message
        self.oldHrpmove = UnicornMove()

        #Variable to keep current orientation
        self.current_orientation_rpy = Vector3()
        self.current_orientation_rpy_HRP = Vector3()
        self.angle_translation = Vector3()

        #Variable to keep goal cooardinate, yaw angle and total travel distance
        self.goal_coordinate = Point()
        self.goal_angle = 0
        self.travel_distance_total = 0.0

        #Velocity constants
        self.linear_velocity = 0.6
        self.linear_velocity_turn = 0.1 #Velocity to use during turning
        self.linear_velocity_reverse = 0.25
        self.linear_velocity_ramp = 0.2 #Lowest velocity to use for ramp
        self.ramp_distance = 0.75 #Distance for which to ramp up and down in speeed
        self.angular_velocity = 0.8
        self.angular_velocity_turn = 0.6
        self.perform_only_turn = False #Used when only turning, allows the use of a lower angular velocity
        self.reversing = False #Used to keep tack of when the robot is reversing
        self.stop_HRP = False #Used to stop the HRP and keep it from moving

        #PI regulator constants
        self.angular_velocity_proportional_gain = 0.001
        self.angular_velocity_integral_gain = 0.0001
        self.proportional_term = 0.0
        self.integral_term = 0.0 
        self.angular_error = 0.0

        #Tolerances
        self.angle_tolerance = 10 #Tolerance angle when turning (deg), the robot will stop when within
        self.angle_tolerance_turn = 5 #When only turning
        self.angle_tolerance_maximum = 30 #Maximum deviation from goal angle before stopping and turning
        self.angle_tolerance_lin_vel_turn = 45 #Maximum angle difference when using linear velocity while turning
        self.travel_distance_tolerance = 1.0 #Minimum travel distance for when to turn with linear velocity
        self.within_tolerance = True #If the robot is within the allowed angle tolerance
        self.point_tolerance = 0.25 #Tolerance in meters, deviation from set point
        self.point_tolerance_reverse = 0.1 #Tolerance in meters, deviation from set point
        self.reset_integral_term_angle_tolerance = 1.0 #If the robot is close enough to the goal angle, reset the integral term to move stright
        
        #Distance sensors
        self.front_distance_sensor_break = 400 #distance in mm when the robot will break when detecting object in front
        self.side_distance_sensor_break = 200 #distance in mm when the robot will break when detecting objects on the side
        self.distance_sensor_measurement = [10000,10000,10000]
        self.sensors_triggered_tolerance = 10 #Skip first n distance sensor values that indicate blocked, delays the blocked response
        self.sensors_triggered_count = 0 #Counts how many times the sensors has been triggered
        self.full_linear_velocity_detection_factor = 1.0 #Variable to keep the increased detection factor, defualt = 1.0 => same as self.front_distance_sensor_break
        self.full_linear_velocity_detection_multiplier = 1.5 #Increases front_distance_sensor_break by n times when moving at full linear velocity

        #Self unblock
        self.self_unblock_enabled = False #Whenever to reset "blocked" state by itself if the obsticles in front are removed, otherwise the robot needs a new point or a direct command to reset
        self.unblock_self_counter = 0 #Used to count the time before unblocking
        self.unblock_self_time = 2 #Unblock after n seconds if no obsticle left

        #Other constants
        self.init_HRP_offset = True
        self.calculate_HRP_offset = True #Calculate an offset from HRP to our coordinate system
        self.current_function=0 #For user and debug info
        self.angle_outside=0 #DEBUG, shows the current angle when the angle tolerance maximum is triggered
        self.turn_in_end = False #Used to turn in the end if an angle is specified in the UnicornMove message
        self.turn_in_end_angle = 0.0 #Used to save the angle in which to turn 
        self.old_coords = np.array(((0.0),(0.0),(0.0))) #Used for point transformation
        self.new_coords = np.array(((0.0),(0.0),(0.0))) #Used for point transformation
        self.R = np.array((
            (0.0,   0.0,   0.0),
            (0.0,   0.0,   0.0),
            (0.0,   0.0,   0.0))) #Used for point transformation
        
        #Keep current state
        self.current_state = 0 #0=idle, 1=executing, 2=finished, 3=blocked, 4=stopped
        self.current_state_message = Int16()
        self.reached_point = False

        #Initialize velocity and command window update callbacks
        self.HRPmsg.linear.x = 0.0 
        self.HRPmsg.linear.y = 0.0
        self.HRPmsg.linear.z = 0.0
        self.HRPmsg.angular.x = 0.0  
        self.HRPmsg.angular.y = 0.0
        self.HRPmsg.angular.z = 0.0

        #Whenever to publish or not, allowing manual control
        self.do_publish = True
        #Force publish of finished state
        self.publish_finished_state = False
        #Debug information output
        self.debug_output = False
        #User information output
        self.user_output = True

        #Setup callbacks
        if self.init_callbacks == True:
            self.velocity_update_period = 0.01  # seconds
            self.velocity_update = self.create_timer(self.velocity_update_period, self.velocity_update_callback)
            velocity_message_period = 1.0  # seconds
            self.velocity_message = self.create_timer(velocity_message_period, self.velocity_message_callback)
            current_state_update_period = 0.1 # seconds
            self.current_state_update = self.create_timer(current_state_update_period, self.current_state_callback)
            self.init_callbacks = False

        #Run program
        #self.moveToPoint(4.0,-1.0)
        #self.turn(50)

        #timer_period = 0.5  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        #self.i = 0

########################################################################################################

##################################### OUTGOING CALLBACKS ###############################################
    #Publish udated velocity to HRP
    def velocity_update_callback(self):  

        #If HRP is not stopped
        if not self.stop_HRP:
            #Calculate the difference between the goal angle and current orientation
            angle_difference_calc = self.goal_angle - self.current_orientation_rpy.z
            if angle_difference_calc > 180:
                angle_difference_calc -=360
            elif angle_difference_calc < -180:
                angle_difference_calc +=360 
            self.angular_error = angle_difference_calc #For the PI regulator (signed error)
            self.angle_difference = abs(angle_difference_calc) #For the next Chunk of code (nonsigned error)

            #Calculate the distance between the current and goal coordinate
            travel_distance_left = np.sqrt(abs(np.float_power(self.goal_coordinate.x - self.current_coordinate.x,2))+abs(np.float_power(self.goal_coordinate.y - self.current_coordinate.y,2)))

            #Check if current travel distance has increased, if so update total travel distance
            if self.travel_distance_total - travel_distance_left < 0.0:
                self.travel_distance_total = np.sqrt(np.float_power(self.goal_coordinate.x - self.current_coordinate.x,2)+np.float_power(self.goal_coordinate.y - self.current_coordinate.y,2))

            #If the robot are within the tolerance, try to travel straight, if it ends up too far off begin to turn again
            if self.angle_difference <= self.angle_tolerance and not self.within_tolerance:
                self.within_tolerance = True #Prevent robot from turning
            elif self.angle_difference > self.angle_tolerance_maximum:
                self.within_tolerance = False #Allow robot to turn again
                self.angle_outside = self.current_orientation_rpy.z #DEBUG

            #Reverse
            if self.reversing and not (abs(self.goal_coordinate.x-self.current_coordinate.x) < self.point_tolerance_reverse and abs(self.goal_coordinate.y-self.current_coordinate.y) < self.point_tolerance_reverse):
                self.current_function=0 #For user and debug info

                self.HRPmsg.angular.z = 0.0
                self.HRPmsg.linear.x = -self.linear_velocity_reverse

            #Perform only a turn, with different angular speed and zero linear velocity
            elif self.angle_difference > self.angle_tolerance_turn and self.perform_only_turn:
                self.current_function=1 #For user and debug info

                self.perform_turn(self.angular_velocity_turn, self.current_orientation_rpy.z, self.goal_angle)
                
                self.HRPmsg.linear.x = 0.0
                
            #If the robot is outside the angle tolerance it needs to turn in the right direction before moving
            elif self.angle_difference > self.angle_tolerance and not self.within_tolerance:
                self.current_function=2 #For user and debug info
                
                self.perform_turn(self.angular_velocity, self.current_orientation_rpy.z, self.goal_angle)

                #Decide if we want to use linear velocity while turning (smoother turn)
                if self.angle_difference <= self.angle_tolerance_lin_vel_turn and travel_distance_left >= self.travel_distance_tolerance:
                    self.HRPmsg.linear.x = self.linear_velocity_turn
                else:
                    self.HRPmsg.linear.x = 0.0

                #Reset integral term
                self.integral_term = 0.0        

            #If the robot has arrived at the target point
            elif abs(self.goal_coordinate.x-self.current_coordinate.x) < self.point_tolerance and abs(self.goal_coordinate.y-self.current_coordinate.y) < self.point_tolerance:
                self.current_function=3 #For user and debug info
                
                #Stop the robot, reset PI integral term
                self.HRPmsg.linear.x = 0.0
                self.HRPmsg.angular.z = 0.0
                self.integral_term = 0.0
                
                #Reset variables
                self.perform_only_turn = False
                self.within_tolerance = False
                self.reversing = False
                self.sensors_triggered_count = 0
                self.full_linear_velocity_detection_factor = 1.0
                
                #Begin to turn if specified in the UnicornMove message
                if self.turn_in_end:
                    self.turn_in_end = False
                    self.linear_velocity_turn = 0.0
                    self.turn(self.turn_in_end_angle)

                #Publish that the robot has reached the point
                elif not self.reached_point:
                    self.reached_point = True
                    self.publish_finished_state = True
                    self.current_state = 2 #Finished

                else:
                    self.current_state = 0 #Idle

            #If the robot is within the angle tolerance, move to the target point
            else:
                self.current_function=4 #For user and debug info
                
                if self.distance_sensor_measurement[0] < self.front_distance_sensor_break*self.full_linear_velocity_detection_factor or self.distance_sensor_measurement[1] < self.side_distance_sensor_break/2 or self.distance_sensor_measurement[2] < self.side_distance_sensor_break/2:
                    self.sensors_triggered_count += 1 #Multiple measurements needed, prevents accidently triggering the stop function

                    if self.sensors_triggered_count > self.sensors_triggered_tolerance:
                        self.stop_hrp_function(0.0)
                        self.HRPmsg.angular.z = 0.0
                        self.HRPmsg.linear.x = 0.0
                else:
                    self.sensors_triggered_count = 0

                    #Update goal angle for next callback
                    self.goal_angle = np.rad2deg(np.arctan2(self.goal_coordinate.y-self.current_coordinate.y,self.goal_coordinate.x-self.current_coordinate.x))
                    
                    #Ramp up
                    if self.travel_distance_total - travel_distance_left < self.ramp_distance and not (travel_distance_left-self.point_tolerance) < (self.travel_distance_total-self.point_tolerance)/2:
                        self.HRPmsg.linear.x = round(((self.travel_distance_total - travel_distance_left)/self.ramp_distance)*(self.linear_velocity-self.linear_velocity_ramp)+self.linear_velocity_ramp,2)
                        self.full_linear_velocity_detection_factor = 1.0
                    #Ramp down
                    elif travel_distance_left-self.point_tolerance < self.ramp_distance:
                        self.HRPmsg.linear.x = round(((travel_distance_left-self.point_tolerance)/self.ramp_distance)*(self.linear_velocity-self.linear_velocity_ramp)+self.linear_velocity_ramp,2)
                        self.full_linear_velocity_detection_factor = 1.0
                    else:
                        self.HRPmsg.linear.x = self.linear_velocity
                        self.full_linear_velocity_detection_factor = self.full_linear_velocity_detection_multiplier #Set to maximum detection distance

                    #PI regulator for adjusting the traveling angle closer to the goal angle
                    self.proportional_term = self.angular_velocity_proportional_gain * self.angular_error
                    
                    self.integral_term  += self.angular_velocity_integral_gain * self.angular_error
                    if self.integral_term > 0.6:
                        self.integral_term = 0.6
                    elif self.integral_term < -0.6:
                        self.integral_term = -0.6

                    #Reset the integral term instantly if we are close enough to the goal angle
                    if self.angle_difference < self.reset_integral_term_angle_tolerance:
                        self.integral_term = 0.0

                    #Calculate the final angular velocity
                    self.HRPmsg.angular.z = self.proportional_term + self.integral_term
                
            #Publish new velocity
            if self.do_publish:
                self.HRP_publisher_.publish(self.HRPmsg)

            self.unblock_self_counter = 0

        elif self.self_unblock_enabled and self.current_state == 3 and (self.distance_sensor_measurement[0] >= self.front_distance_sensor_break and self.distance_sensor_measurement[1] >= self.side_distance_sensor_break and self.distance_sensor_measurement[2] >= self.side_distance_sensor_break):
            self.unblock_self_counter += 1

            if self.unblock_self_counter >= (self.unblock_self_time/self.velocity_update_period):
                self.stop_hrp_function(1.0)

    #Show user information in command window
    def velocity_message_callback(self):
        if self.debug_output or self. user_output:
            print("\033c")

        if self.debug_output:
            print("################# DEBUG INFO ################")
            
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
            print('Current state: "%s"' %self.current_state)
            print('Publish finished state: "%s"' %self.publish_finished_state)
            
            print("#############################################")
            print("")

        if self.user_output:
            print("################# USER INFO #################")

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

            print("Current point:   x = {:.{}f}".format(self.current_coordinate.x,2), ", y = {:.{}f}".format(self.current_coordinate.y,2), ", angle = {:.{}f}".format(self.current_orientation_rpy.z,2))
            if self.turn_in_end:
                print("Moving to point: x = {:.{}f}".format(self.goal_coordinate.x,2), ", y = {:.{}f}".format(self.goal_coordinate.y,2), ", angle = {:.{}f}".format(self.turn_in_end_angle,2))
            else: 
                print("Moving to point: x = {:.{}f}".format(self.goal_coordinate.x,2), ", y = {:.{}f}".format(self.goal_coordinate.y,2), ", angle = {:.{}f}".format(self.goal_angle,2))

            if self.current_function == 4:
                print('Current command type: Moving')
            elif self.current_function == 0:
                print('Current command type: Reversing')
            elif self.current_function == 1 or self.current_function == 2:
                print('Current command type: Turning')
            else:
                print('Current command type: None')

            sensors = ["no ","no ", "no "]
            if self.distance_sensor_measurement[0] < self.front_distance_sensor_break:
                sensors[0] = "yes"
            if self.distance_sensor_measurement[1] < self.side_distance_sensor_break:
                sensors[1] = "yes"
            if self.distance_sensor_measurement[2] < self.side_distance_sensor_break:
                sensors[2] = "yes"
            
            print("Sensor status: Left: " + sensors[1] + " Front: " + sensors[0] + " Right: " + sensors[2])

            print("#############################################")
        
        #self.get_logger().info('Linear: "%s"' % HRPmsg.linear)
        #self.get_logger().info('Angular: "%s"' % HRPmsg.angular)
        #self.get_logger().info('Odometry data: "%s"' % self.curPoint)

    def current_state_callback(self):
        #Force publish finished state
        if self.publish_finished_state:
            self.publish_finished_state = False
            self.current_state_message.data = 2 #Finished
            self.Unicorn_current_state_publisher_.publish(self.current_state_message)
            self.current_state = 0 #Idle
        else:
            self.current_state_message.data = self.current_state
            self.Unicorn_current_state_publisher_.publish(self.current_state_message)


########################################################################################################

##################################### INCOMMING CALLBACKS ##############################################

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
        if self.calculate_HRP_offset and self.init_HRP_offset:
            self.calculate_HRP_offset = False
            self.init_HRP_offset = False
            self.coordinate_translation = self.current_coordinate_HRP
            self.angle_translation.x = self.current_orientation_rpy_HRP.x
            self.angle_translation.y = self.current_orientation_rpy_HRP.y
            self.angle_translation.z = self.current_orientation_rpy_HRP.z
            print("First time offset = True, using our own orientation and coordinate system")
        elif self.init_HRP_offset: 
            self.init_HRP_offset = False
            self.coordinate_translation = Point()
            self.coordinate_translation.x = 0.0
            self.coordinate_translation.y = 0.0
            self.coordinate_translation.z = 0.0
            self.angle_translation.x = 0.0
            self.angle_translation.y = 0.0
            self.angle_translation.z = 0.0
            print("First time offset = False, keeping HRP orientation and coordinate system")
        
        #Calculate orientation using the rotation offset
        self.current_orientation_rpy.x = self.calculate_orientation_using_offset(self.current_orientation_rpy_HRP.x, self.angle_translation.x)
        self.current_orientation_rpy.y = self.calculate_orientation_using_offset(self.current_orientation_rpy_HRP.y, self.angle_translation.y)
        self.current_orientation_rpy.z = self.calculate_orientation_using_offset(self.current_orientation_rpy_HRP.z, self.angle_translation.z)

        #Current coordinate with the translation offset to get to our own coordinate system
        current_coordinate_trans_x = self.current_coordinate_HRP.x - self.coordinate_translation.x
        current_coordinate_trans_y = self.current_coordinate_HRP.y - self.coordinate_translation.y
        current_coordinate_trans_z = self.current_coordinate_HRP.z - self.coordinate_translation.z

        new_coordinates = self.transform_point(current_coordinate_trans_x,current_coordinate_trans_y,current_coordinate_trans_z,self.angle_translation.x,self.angle_translation.y,self.angle_translation.z)
        self.current_coordinate.x = new_coordinates[0]
        self.current_coordinate.y = new_coordinates[1]
        self.current_coordinate.z = new_coordinates[2]

    def soft_reset_callback(self,msg):
        if msg.data == 1.0:
            print("Soft reset...")
            self.setup()

    def move_hrp_callback(self,msg):

        if msg == self.oldHrpmove:
            return
        else:
            self.oldHrpmove = msg
            self.stop_hrp_function(1.0)

        #If HRP is not stopped
        if not self.stop_HRP:
            self.reached_point = False

            #Don't care what the goal angle will be
            if msg.angle == 200:
                self.moveToPoint(msg.x,msg.y)
    
            #Reverse, use "x coordinate" as distanse
            elif msg.angle == -200:
                self.reverse(msg.x)

            #Drive and turn in the end or only turn if new coordinates are the same as the current        
            else:
                #Only turn
                if (abs(msg.x-self.current_coordinate.x) < self.point_tolerance and abs(msg.y-self.current_coordinate.y) < self.point_tolerance): 
                    self.turn(msg.angle)
                else:
                    self.turn_in_end = True
                    self.turn_in_end_angle = msg.angle
                    self.moveToPoint(msg.x,msg.y)

            self.current_state = 1 #Executing

    def stop_hrp_callback(self,msg):
        print("callback")
        self.stop_hrp_function(msg.data)

    def stop_hrp_function(self,msg):
        #Stop HRP (0.0 for blocked, 0.1 for stopped)
        if msg == 0.0 or msg == 0.1:
            self.goal_coordinate.x = self.current_coordinate.x
            self.goal_coordinate.x = self.current_coordinate.y
            self.goal_angle = self.current_orientation_rpy.z
            self.HRPmsg.angular.z = 0.0
            self.HRPmsg.linear.x = 0.0
            self.HRP_publisher_.publish(self.HRPmsg)
            self.stop_HRP = True
            self.perform_only_turn = False
            self.within_tolerance = False
            self.reversing = False
            
            if msg == 0.0:
               self.current_state = 3 #Blocked
            else:
               self.current_state = 4 #Stopped  

        #Allow HRP to move again
        elif msg == 1.0:
            self.stop_HRP = False
            self.current_state = 0 #Idle

    def measurement_sensor_callback(self,msg):
        if msg.f == -1:
            self.distance_sensor_measurement[0] = 10000
        else:
            self.distance_sensor_measurement[0] = msg.f
        if msg.l == -1:
            self.distance_sensor_measurement[1] = 10000
        else:
            self.distance_sensor_measurement[1] = msg.l

        if msg.r == -1:
            self.distance_sensor_measurement[2] = 10000
        else:
            self.distance_sensor_measurement[2] = msg.r

##################################### MOVEMENT ######################################################s###

    #Move HRP from one point to another
    def moveToPoint(self, target_x_coordinate, target_y_coordinate):
        self.goal_coordinate.x = target_x_coordinate
        self.goal_coordinate.y = target_y_coordinate
        self.goal_angle = np.rad2deg(np.arctan2(self.goal_coordinate.y-self.current_coordinate.y,self.goal_coordinate.x-self.current_coordinate.x))
        self.goal_coordinate.z = 0.0
        #Calculate the total distance between the current and goal coordinate
        self.travel_distance_total = np.sqrt(np.float_power(self.goal_coordinate.x - self.current_coordinate.x,2)+np.float_power(self.goal_coordinate.y - self.current_coordinate.y,2))

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
            if self.distance_sensor_measurement[1] < self.side_distance_sensor_break:
                self.sensors_triggered_count += 1

                if self.sensors_triggered_count > self.sensors_triggered_tolerance:
                    self.stop_hrp_function(0.0)
                    self.HRPmsg.angular.z = 0.0
            else:
                self.sensors_triggered_count = 0
                self.HRPmsg.angular.z = velocity
        else:
            if self.distance_sensor_measurement[2] < self.side_distance_sensor_break:
                self.sensors_triggered_count += 1

                if self.sensors_triggered_count > self.sensors_triggered_tolerance:
                    self.stop_hrp_function(0.0)
                    self.HRPmsg.angular.z = 0.0
            else:
                self.sensors_triggered_count = 0
                self.HRPmsg.angular.z = -velocity
        self.HRPmsg.linear.x = self.linear_velocity_turn

    #Reverse
    def reverse(self, distance):
        self.goal_angle = self.current_orientation_rpy.z
        self.goal_coordinate.x = self.current_coordinate.x - distance*np.cos(np.deg2rad(self.current_orientation_rpy.z))
        self.goal_coordinate.y = self.current_coordinate.y - distance*np.sin(np.deg2rad(self.current_orientation_rpy.z))
        self.reversing = True

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

    #Calculate our orientation using the offset and HRP orientation
    def calculate_orientation_using_offset(self, current_orientation_HRP, angle_translation_HRP):
        current_orientation = current_orientation_HRP - angle_translation_HRP
        
        if current_orientation >= 180:
            current_orientation -=360
        elif current_orientation <= -180:
            current_orientation +=360

        return current_orientation

    #Calculate the transformed point using the new orientation
    def transform_point(self,x_coord,y_coord,z_coord,r_angle,p_angle,y_angle):
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
