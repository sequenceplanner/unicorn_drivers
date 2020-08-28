# Unicorn HRP Controller

ROS and ROS2 packages for controller unicorn demo with HRP and SP. Also includes microcontroller code for controlling lights, actuators and distance sensors.

## Repository content

* catkin_ws
  * Contains a subset of the code from the [Husqvarna Research Platform](https://github.com/HusqvarnaResearch/hrp) repository.
    Gazebo simulation parts have been removed and only the necessary packages for control of the HRP hardware remain.
  
* colcon_ws
  * hw_controller:
    
    ROS2 node that communicates via serial to the microcontroller that is responsible for interfacing with the garbage tipper, garbage sensors (detects if there is garbage placed on the platform), distance sensors for collision avoidance and LED light strips for status indication.
    
  * unicorn_hrp:
    
    ROS2 node that controls the HRP hardware
    
  * hrp_msgs:
    
    Custom ROS messages
  
* hw-interface

  * Holds code for the microcontroller that interfaces directly with the additional sensors and actuators added to the HRP. Is controlled by the ROS 2 node hw_controller.

## Installation

The current system has been tested on either a Nvidia Jetson Nano or Jetson Xavier NX. The following dependencies need to be installed for the system to work properly:

* ROS2 eloquent [guide](https://index.ros.org/doc/ros2/Installation/Eloquent/Linux-Install-Debians/)

* ROS melodic [guide](http://wiki.ros.org/melodic/Installation/Ubuntu)

* ROS Bridge
  
Used to run a dynamic bridge that translates topics between the ROS2 and ROS. Can be installed by running:
  
  ```bash
  sudo apt-get update
  sudo apt install ros-eloquent-ros1-bridge
```
  
* [Pyserial](https://pypi.org/project/pyserial/) 
  
Needed for serial communication with the microcontroller hardware.
  
* GNU Screen 
  
  Used for the hrp_start.sh script that starts up the system
  Check out this [Quick Reference](https://gist.github.com/jctosta/af918e1618682638aa82) on how to use Screen.

By default Ubuntu does not allow users access to system serial ports. To solve this we need to add the current user to the dialout group:

```bash
sudo usermod -a -G dialout $USER
```

## Startup

Preparing the HRP for startup

1. Make sure the power switch is in the on position
2. Open the lid and enter code 1111
3. Wait for the HRP to initialize and then press start and close the lid when prompted to

Run the startup shell script from the repository root folder

```bash
./hrp_startup.sh
```

This will launch and automatically connect to a screen sessions with the following windows:

0. ros-bash
   
   Regular terminal window with bash and ROS sourced
   
1. am_driver

   Driver used to communicate with the HRP hardware

2. ros1_bridge

   Bridge used to bidirectionally translate topics from ROS2 and ROS

3. teleop

   Teleoperation and status of the HRP hardware

4. ros2_hw_controller

   ROS2 node for interfacing with microcontroller 

5. ros2_hrp_controller

   ROS2 node for interfacing with am_driver

Troubleshooting:

* am_driver is configured to launch with LOOP_OFF (the HRP in regular operation detects a wire signal to prevent it from going outside a specific area) but this does not always take effect. If this is the case navigate to the teleop window in screen and set LOOP_OFF manually



