# CMake generated Testfile for 
# Source directory: /home/reach-004/Documents/UNICORN-ROS2-CONTROLLER/colcon_ws/src/hrp_msgs
# Build directory: /home/reach-004/Documents/UNICORN-ROS2-CONTROLLER/build/hrp_msgs
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(lint_cmake "/usr/bin/python3" "-u" "/opt/ros/eloquent/share/ament_cmake_test/cmake/run_test.py" "/home/reach-004/Documents/UNICORN-ROS2-CONTROLLER/build/hrp_msgs/test_results/hrp_msgs/lint_cmake.xunit.xml" "--package-name" "hrp_msgs" "--output-file" "/home/reach-004/Documents/UNICORN-ROS2-CONTROLLER/build/hrp_msgs/ament_lint_cmake/lint_cmake.txt" "--command" "/opt/ros/eloquent/bin/ament_lint_cmake" "--xunit-file" "/home/reach-004/Documents/UNICORN-ROS2-CONTROLLER/build/hrp_msgs/test_results/hrp_msgs/lint_cmake.xunit.xml")
set_tests_properties(lint_cmake PROPERTIES  LABELS "lint_cmake;linter" TIMEOUT "60" WORKING_DIRECTORY "/home/reach-004/Documents/UNICORN-ROS2-CONTROLLER/colcon_ws/src/hrp_msgs")
add_test(xmllint "/usr/bin/python3" "-u" "/opt/ros/eloquent/share/ament_cmake_test/cmake/run_test.py" "/home/reach-004/Documents/UNICORN-ROS2-CONTROLLER/build/hrp_msgs/test_results/hrp_msgs/xmllint.xunit.xml" "--package-name" "hrp_msgs" "--output-file" "/home/reach-004/Documents/UNICORN-ROS2-CONTROLLER/build/hrp_msgs/ament_xmllint/xmllint.txt" "--command" "/opt/ros/eloquent/bin/ament_xmllint" "--xunit-file" "/home/reach-004/Documents/UNICORN-ROS2-CONTROLLER/build/hrp_msgs/test_results/hrp_msgs/xmllint.xunit.xml")
set_tests_properties(xmllint PROPERTIES  LABELS "xmllint;linter" TIMEOUT "60" WORKING_DIRECTORY "/home/reach-004/Documents/UNICORN-ROS2-CONTROLLER/colcon_ws/src/hrp_msgs")
subdirs("hrp_msgs__py")
