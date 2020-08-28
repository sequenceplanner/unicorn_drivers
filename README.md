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
  * hrp_msgs
    Custom ROS messages

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

* Pyserial
  Needed for serial communication with the microcontroller hardware.

* Screen
  Used for the hrp_start.sh script that starts up the system.

By default Ubuntu does not allow users access to system serial ports. To solve this we need to add the current user to the dialout group:

```bash
sudo usermod -a -G dialout $USER
```

