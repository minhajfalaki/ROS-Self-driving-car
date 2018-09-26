# ROS-car-autonomy

This project drive a simulated car in gazebo. Car i used is taken from dbw_mkz ros simulation. Images from the camera is taken and a CNN model is created and trained to predict steering and throttle output.

This project was done on Ubuntu 16.04 and uses Tensorflow, tflearn, numpy and ROS kinetic.
The model is inspired from Alexnet model.

To install the car simulation.
1. bash <(wget -q -O - https://bitbucket.org/DataspeedInc/ros_binaries/raw/default/scripts/setup.bash)
2. sudo apt-get install ros-kinetic-dbw-mkz-simulator
