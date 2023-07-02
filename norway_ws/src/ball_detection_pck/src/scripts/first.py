#!/usr/bin/env python


from __future__ import print_function
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image , LaserScan
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist

def check(veri):
      Lidar = {
        "front":  min(min(veri.ranges[0:30]),30,min(veri.ranges[340:360])),
        "left":  min(min(veri.ranges[445:455]),30),
        "front-right":min(min(veri.ranges[280:340]),30),
        }
      print(Lidar["left"])
      print(veri.ranges[445:455].index(min(veri.ranges[445:455])))

def main():
      rospy.init_node("aass")
      rospy.Subscriber("/sick_lms_1xx/scan", LaserScan, check)
      rospy.spin()
main()
