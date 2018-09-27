import numpy as np
import sys
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from dbw_mkz_msgs.msg import ThrottleReport
from dbw_mkz_msgs.msg import SteeringReport
from cv_bridge import CvBridge, CvBridgeError 
from message_filters import TimeSynchronizer, Subscriber,ApproximateTimeSynchronizer
import message_filters
import cv2
import time
import os


file_name = 'training_data.npy'

if os.path.isfile(file_name):
    print('File exists, loading previous data!')
    training_data = list(np.load(file_name))
else:
    print('File does not exist, starting fresh!')
    training_data = []

class image_converter:

    def __init__(self):
 
        self.bridge = CvBridge()
        self.tss = ApproximateTimeSynchronizer([Subscriber("/fusion/front_camera/image_raw",Image),Subscriber('/fusion/steering_report',SteeringReport),Subscriber('/fusion/throttle_report',ThrottleReport)],10, 0.2, allow_headerless=False)
        self.tss.registerCallback(self.callback_img)


    def callback_img(self,Image,SteeringReport,ThrottleReport):
        i=0
        try:
            screen = self.bridge.imgmsg_to_cv2(Image, "bgr8")
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (150,200))
            steering=SteeringReport.steering_wheel_angle_cmd
            throttle=ThrottleReport.pedal_cmd
        except CvBridgeError as e:
            print(e)
            last_time = time.time()
        output=[steering,throttle]

        training_data.append([screen,output])
        print len(training_data),steering,throttle
        
        if len(training_data) % 100 == 0:
            print(len(training_data))
            np.save(file_name,training_data)
            print 'saved'

def main(args):
    ic = image_converter()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    file_name = 'training_data11.npy'

    if os.path.isfile(file_name):
        print('File exists, loading previous data!')
        training_data = list(np.load(file_name))
    else:
        print('File does not exist, starting fresh!')
        training_data = []
    main(sys.argv)