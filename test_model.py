import numpy as np
import cv2
import time
from alexnet import alexnet
import random
import roslib
import check as ck
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import random
import time
from dbw_mkz_msgs.msg import BrakeCmd
from dbw_mkz_msgs.msg import ThrottleCmd
from dbw_mkz_msgs.msg import SteeringCmd
from dbw_mkz_msgs.msg import GearCmd, Gear
from gazebo_msgs.msg import ModelStates
from dbw_mkz_msgs.msg import SteeringReport, BrakeReport, ThrottleReport
from std_msgs.msg import Empty

WIDTH = 130
HEIGHT = 70
LR = 1e-4
EPOCHS = 10
MODEL_NAME = 'ROS-car-fast-{}-{}-{}-epochs-data.model'.format(LR, 'alexnetv2',EPOCHS)

model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)


class image_converter:

    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/fusion/front_camera/image_raw",Image,self.callback)

    def callback(self,data):
        i=0
        try:
            screen = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, (120,160))
        screen = cv2.normalize(screen,screen, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        print "test"
        screen = np.array(screen).reshape(WIDTH,HEIGHT,1)
        predictionx = model.predict([screen])[0]
        motion=predictionx[1]
        turn  =predictionx[0]
        if 0.000001<turn <= 0.01:
            turn1=0
        elif turn<0.000001:
            q=np.log10(turn)
            turn1= q*0.2
        elif 0.01<turn<=0.4:
            turn= 1/(turn*10)

        else:
            turn1= turn*1.3
        motion =motion*.15


        self.pub_throttle_cmd = rospy.Publisher('/fusion/throttle_cmd',ThrottleCmd, queue_size=1)
        self.pub_steering_cmd = rospy.Publisher('/fusion/steering_cmd', SteeringCmd, queue_size=1)

        throttle_command_object = ThrottleCmd()
        throttle_command_object.pedal_cmd = motion
        throttle_command_object.pedal_cmd_type = 1
        throttle_command_object.enable = True
        throttle_command_object.ignore = False
        throttle_command_object.count = 0
        self.pub_throttle_cmd.publish(throttle_command_object)

        steering_command_object = SteeringCmd()
        steering_command_object.steering_wheel_angle_cmd = turn1
        steering_command_object.steering_wheel_angle_velocity = random.uniform(0.0, 8.7)
        steering_command_object.enable = True
        steering_command_object.ignore = False
        steering_command_object.quiet = False
        steering_command_object.count = 0
        self.pub_steering_cmd.publish(steering_command_object)

        print turn,motion


def main(args):
    ic = image_converter()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
  
