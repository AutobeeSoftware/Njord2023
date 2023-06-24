#!/usr/bin/env python2

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist

class BallFollower:
    
    def __init__(self):
        rospy.init_node('ball_follower')
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('/camera/image', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel',Twist, queue_size =10)
        self.twist = Twist()
        
    def image_callback(self,msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg,"bgr8")
        hsv_image = cv2.cvtColor(cv_image,cv2.COLOR_BGRHSV)
        lower_yellow = cv2.inRange(hsv_image,(20,100,100),(30,255,255))
        contours, _ = cv2.findcontours(lower_yellow,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            (x,y), radius = cv2.minEnclosingCicle(largest_contour)
            
            if radius > 10:
                cv2.circle(cv_image,(int(x),int(y)),int(radius), (0,255,0),2)
                cv2.putText(cv_image,'Ball',(int(x-radius),int(y-radius)),cv2.FONT_HERSEY_SIMPLEX,0.6,(0,255,0),2)
            
                if x < cv_image.shape[1]/ 2:
                    self.twist.angular.z = 0.5 # Dolasma yonu saat yonunde
                else:
                    self.twist.angular.z =-0.5 # Dolasma yonu saat tersi yonunde
            
            else:
                self.twist.angular.z = 0.0
        
        cv2.imshow('Ball Follower', cv_image)
        cv2.waitKey(1)
        
    def run(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.cmd_vel_pub.publish(self.twist)
            rate.sleep()

if __name__ == '__main__':
    ball_follower = BallFollower()
    ball_follower.run()
                
    