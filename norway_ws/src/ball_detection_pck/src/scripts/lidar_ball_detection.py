#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 17:45:20 2023

@author: hakan
"""

#from _future_ import print_function
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image , LaserScan
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist


class TakePhoto:

    def _init_(self):

        self.pub=rospy.Publisher('/cmd_vel',Twist,queue_size=10)
        self.rate=rospy.Rate(1)
        self.rot=Twist()
        self.x = 1
        self.cx_r=0
        self.cy_r=0
        self.control = 0
        self.cx_g=0
        self.cy_g=0
        self.bridge = CvBridge()
        self.image_received = False
        # Connect image topic
        self.img_topic = "/camera/rgb/image_raw"
        rospy.Subscriber("/scan", LaserScan, self.check)
        self.image_sub = rospy.Subscriber(self.img_topic, Image, self.callback)
        rospy.sleep(1)
    
    def check(self, veri):
        
        print(len(veri.ranges))
        self.Lidar = {
        "front-left":  min(min(veri.ranges[0:10]),30),
        "left":  min(min(veri.ranges[85:95]),30),
        "right":  min(min(veri.ranges[265:275]),30),
        "front-right":min(min(veri.ranges[350:360]),30)
        }


    def callback(self, data):

        # Convert image to OpenCV format
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        self.image_received = True
        self.image = cv_image
        #self.show_image(cv_image)
        self.find_object(cv_image)
        self.move_to_object()

    def show_image(self,img):
        cv2.imshow("Image Window", img)
        cv2.waitKey(3)
        

    def find_object(self,img):
        hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hsv_frame = cv2.resize(hsv_frame,(640,300))

        low_H_R=0
        low_S_R=50
        low_V_R=50
        high_H_R=10
        high_S_R=255
        high_V_R=255
        
        low_H_G = 25
        low_S_G= 52
        low_V_G=72
        high_H_G=102
        high_S_G=255
        high_V_G=255

        mask_frame_red=cv2.inRange(hsv_frame, (low_H_R, low_S_R, low_V_R), (high_H_R, high_S_R, high_V_R))
        cv2.imshow("mask",mask_frame_red)
        #contours, hierarchy = cv2.findContours(mask_frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        _, contours_red, _= cv2.findContours(mask_frame_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        mask_frame_green=cv2.inRange(hsv_frame, (low_H_G, low_S_G, low_V_G), (high_H_G, high_S_G, high_V_G))
        cv2.imshow("mask",mask_frame_green)
        #contours, hierarchy = cv2.findContours(mask_frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        _, contours_green, _= cv2.findContours(mask_frame_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        X_r,Y_r,W_r,H_r=0,0,0,0
        X_g,Y_g,W_g,H_g=0,0,0,0


        for pic, contour_r in enumerate(contours_red):
            area = cv2.contourArea(contour_r)
            
            if(area > 100):
                
                x_r, y_r, w_r, h_r = cv2.boundingRect(contour_r)
                if(w_r*h_r>W_r*H_r):
                    X_r, Y_r, W_r, H_r= x_r, y_r, w_r, h_r

        img = cv2.rectangle(img, (X_r, Y_r),(X_r +W_r, Y_r + H_r),(0, 0, 255), 2)
        self.cx_r =X_r
        self.cy_r = Y_r
        
        for pic, contour_g in enumerate(contours_green):
            area = cv2.contourArea(contour_g)
            
            if(area > 100):
                
                x_g, y_g, w_g, h_g = cv2.boundingRect(contour_g)
                if(w_g*h_g>W_g*H_g):
                    X_g, Y_g, W_g, H_g= x_g, y_g, w_g, h_g

        img = cv2.rectangle(img, (X_g, Y_g),(X_g +W_g, Y_g + H_g),(0, 0, 255), 2)
        self.cx_g =X_g
        self.cy_g = Y_g
        
        print("Cx red: ",self.cx_r)
        print("Cx green: ", self.cx_g)
        cv2.imshow("window", img)
        cv2.waitKey(3)

    def move_to_object(self):
        obj_x=((self.cx_r+self.cx_g)/2)-320
        if self.Lidar["front-left"] < 1 or self.Lidar["front-right"] < 1:
            self.control = 1
            if self.Lidar["front-left"] < 1:
                self.rot.angular.z= 0.1
                self.rot.linear.x=0.2
            elif self.Lidar["front-right"] < 1:
                self.rot.angular.z= -0.1
                self.rot.linear.x=0.4
        elif self.Lidar["left"] > 1 and self.control == 1:
            self.rot.angular.z= -0.1
        elif self.Lidar["right"] > 1 and self.control == 1:
            self.rot.angular.z= 0.1


        elif self.cx_r != 0 and self.cx_g !=0:
        
            self.rot.linear.x=0.4 
            self.rot.angular.z = -obj_x/1000
            self.x = 1
        elif self.cx_r == 0 and self.cx_g !=0:
            self.rot.angular.z = -0.2
        elif self.cx_r != 0 and self.cx_g ==0:
            self.rot.angular.z = 0.2


        print(obj_x)
        self.pub.publish(self.rot)



if __name__ == '__main__':

    # Initialize
    rospy.init_node('take_photo', anonymous=False)
    camera = TakePhoto()

    while not rospy.is_shutdown():
        rospy.sleep(0.1)
        rospy.spin()

    #camera.stop()
