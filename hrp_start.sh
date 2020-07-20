#!/bin/bash

# requires permission to be set up for user to access usb serial. Done via:
# sudo usermod -a -G dialout $USER

echo "HRP Autostart - sets up am_driver_safe and ros1_bridge"
# setting up named screen windows
screen -AdmS ros-hrp -t ros-bash bash
screen -S ros-hrp -X screen -t am_driver bash
screen -S ros-hrp -X screen -t ros1_bridge bash
screen -S ros-hrp -X screen -t teleop bash
# launching am driver with loop off:
screen -S ros-hrp -p am_driver -X stuff 'source /opt/ros/melodic/setup.bash
source ./catkin_ws/devel/setup.bash
roslaunch am_driver_safe automower_hrp.launch startWithoutLoop:=false
'
echo "Starting am_driver..."
sleep 10
screen -S ros-hrp -p teleop -X stuff 'source /opt/ros/melodic/setup.bash
source ./catkin_ws/devel/setup.bash
rosrun am_driver hrp_teleop.py
'
echo "Starting teleop..."
screen -S ros-hrp -p ros1_bridge -X stuff 'source /opt/ros/melodic/setup.bash
source /opt/ros/eloquent/setup.bash
ros2 run ros1_bridge dynamic_bridge --bridge-all-topics
'

# link: https://unix.stackexchange.com/questions/74785/how-to-open-tabs-windows-in-gnu-screen-execute-commands-within-each-one
#echo "test script"
#screen -AdmS myshell -t tab0 bash
#screen -S myshell -X screen -t tab1
#screen -S myshell -p tab1 -X stuff 'ls\n'
