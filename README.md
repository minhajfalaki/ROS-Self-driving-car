# ROS-car-autonomy

This project gazebo simulated car autonomous. Car i used is taken from dbw_mkz ros simulation. Images from the camera is taken and a CNN model is created and trained to predict steering and throttle output.

This project was done on Ubuntu 16.04 and uses Tensorflow, tflearn, numpy and ROS kinetic.
The model is inspired from Alexnet model.

To install the car simulation.(more details about the simulator is given in the simulator_manual_v1_2_0.pdf)
1. bash <(wget -q -O - https://bitbucket.org/DataspeedInc/ros_binaries/raw/default/scripts/setup.bash)
2. sudo apt-get install ros-kinetic-dbw-mkz-simulator

An additional car.launch file was created for making our environment with simple road and car.
![car_image](/minhajf/Pictures/gazebo_car.png)

