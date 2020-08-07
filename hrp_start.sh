#!/bin/bash

# requires permission to be set up for user to access usb serial. Done via:
# sudo usermod -a -G dialout $USER

echo "HRP Autostart - sets up am_driver_safe and ros1_bridge"
# setting up named screen windows
screen -AdmS ros-hrp -t ros-bash bash
screen -S ros-hrp -X screen -t am_driver bash
screen -S ros-hrp -X screen -t ros1_bridge bash
screen -S ros-hrp -X screen -t teleop bash
screen -S ros-hrp -X screen -t ros2_hw_controller bash
screen -S ros-hrp -X screen -t ros2_hrp_controller bash
# launching ros2 first:
echo "Starting ros2 hw_controller..."
screen -S ros-hrp -p ros2_hw_controller -X stuff 'source /opt/ros/eloquent/setup.bash
source ./colcon_ws/install/setup.bash
^l
ros2 run hw_controller hw_controller
'
sleep 1
echo "Starting ros2 hrp controller..."
screen -S ros-hrp -p ros2_hrp_controller -X stuff 'source /opt/ros/eloquent/setup.bash
source ./colcon_ws/install/setup.bash
^l
ros2 run unicorn_hrp unicorn_hrp_controller --ros-args -r __ns:=/hrp/hrp1
'
sleep 2
# launching am driver with loop off:
screen -S ros-hrp -p am_driver -X stuff 'source /opt/ros/melodic/setup.bash
source ./catkin_ws/devel/setup.bash
^l
roslaunch am_driver_safe automower_hrp.launch startWithoutLoop:=false __ns:=/hrp/hrp1
'
echo "Starting am_driver..."
screen -S ros-hrp -p teleop -X stuff 'source /opt/ros/melodic/setup.bash
source ./catkin_ws/devel/setup.bash
^l
rosrun am_driver hrp_teleop.py __ns:=/hrp/hrp1
'
sleep 3
# allowing time for roscore to start with am_driver
echo "Starting teleop..."
screen -S ros-hrp -p ros1_bridge -X stuff 'source /opt/ros/melodic/setup.bash
source /opt/ros/eloquent/setup.bash
^l
ros2 run ros1_bridge dynamic_bridge --bridge-all-topics
'
echo "Reattaching to newly created screen session in 5s..."
sleep 5
screen -r ros-hrp

# link: https://unix.stackexchange.com/questions/74785/how-to-open-tabs-windows-in-gnu-screen-execute-commands-within-each-one
#echo "test script"
#screen -AdmS myshell -t tab0 bash
#screen -S myshell -X screen -t tab1
#screen -S myshell -p tab1 -X stuff 'ls\n'
