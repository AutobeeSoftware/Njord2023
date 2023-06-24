#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 19:50:58 2023

@author: hakan
"""

import sys
import rospy
import smach
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image, LaserScan
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from ball_detection_pck.msg import ball_location 



class MiddleFollow(smach.State):
   def __init__(self):
      smach.State.__init__(self, outcomes=["FINISHED", "ERROR"])
      self.lost_track = False 
    
   def move_to_object(self, data):
      self.last_detection_recv = rospy.Time.now()
      if not data.isredfound or not data.isgreenfound:
         self.lost_track = True
         return 

      tw = Twist()
      tw.angular.z = -data.middle/700
            
      if data.middle < 10:
         tw.linear.x = 0.4

      self.cmd_pub.publish(tw)

   def execute(self,userdata):
      self.lost_track = False
      rospy.loginfo('Executing state middle')
      rospy.wait_for_message("/camera_data", ball_location)
      self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
      self.image_sub = rospy.Subscriber("/camera_data", ball_location , self.move_to_object)
      rate = rospy.Rate(20.0)
      while not rospy.is_shutdown():
         if self.lost_track:
            return "ERROR"
         rate.sleep()

      return "FINISHED"

class Recenter(smach.State):
   def __init__(self):
      smach.State.__init__(self, outcomes=['MIDDLE', 'ERROR'])
      self.tw = Twist()
      self.tw.linear.x = 0.4
      self.tw.angular.z = 0
      self.lost_track = False
      self.centerfound = False
   def center(self,data):
      if not data.isredfound and data.isgreenfound:
         self.tw.angular.z = 0.2
      elif not data.isgreenfound and data.isredfound:
         self.tw.angular.z = -0.2
      elif not data.isgreenfound and not data.isredfound:
         self.lost_track = True
         return
      elif not data.isgreenfound and not data.isredfound:
         self.lost_track = True
         return
      elif  data.isgreenfound and data.isredfound:
         self.centerfound =True
         return
      self.cmd_pub.publish(self.tw)
   def execute(self, userdata):
      self.centerfound = False
      self.lost_track = False
      rospy.loginfo('Executing state Recenter')
      rospy.wait_for_message("/camera_data", ball_location)
      self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
      self.image_sub = rospy.Subscriber("/camera_data", ball_location , self.center)
      self.tw.linear.x = 0
      self.tw.angular.z = 0
      
      rate= rospy.Rate(20)
      
      while not rospy.is_shutdown():
         if self.centerfound:
            return "MIDDLE"
         rate.sleep()
         """
         if self.lost_track:

            return "ERROR"
         """
      return "FINISHED"
  
class DontHitVesselLeft(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=["RECENTER", "ERROR"])
        self.tw = Twist()
        self.tw.linear.x = 0.4
        self.lost_track = False
        self.centerfound = False
        self.Lidar = {
        "left":  30,
        "right":  30,
        } 
        
    def check(self, veri):
      self.Lidar = {
        "left":  veri.ranges[0:135],    #min(min(veri.ranges[0:135]),30),
        "right": veri.ranges[225:360]   #min(min(veri.ranges[225:360]),30)
        }
    def move_to_object(self, data):
        self.last_detection_recv = rospy.Time.now()
        self.min_left_angle = self.Lidar["left"].index(min(self.Lidar["left"]))
        rospy.loginfo(self.min_left_angle)
        self.m_l_a = False
        self.min_right_angle = 360 - self.Lidar["right"].index(min(self.Lidar["right"]))
        self.m_r_a = False
        rospy.loginfo(self.min_right_angle)
        rospy.loginfo("inagnle")
        if data.isredfound or data.isgreenfound:
           self.centerfound = True
           return 
    
        tw = Twist()
        tw.angular.z = -data.middle/700
                
        if data.middle < 10:
           tw.linear.x = 0.4
        
        if self.min_left_angle > 0 and  min(min((self.Lidar["right"]),30))>5:
            self.m_l_a = True
            self.m_r_a = False
            tw.angular.z = 1/self.min_left_angle
        elif min(min((self.Lidar["left"]),30)) > 5 and self.min_right_angle > 0:
            self.m_l_a = False
            self.m_r_a = True
            tw.angular.z = -1/self.min_right_angle
        elif min(min((self.Lidar["left"]),30)) < 5 and min(min((self.Lidar["right"]),30)) < 5:
            self.m_l_a = True
            self.m_r_a = True
        elif min(min((self.Lidar["left"]),30)) > 5 and  min(min((self.Lidar["right"]),30))>5:
            self.m_l_a = False
            self.m_l_a = False
            
        self.cmd_pub.publish(tw)
    """
    def angle(self):
        #rospy.Subscriber("/scan", LaserScan, self.check)
        self.min_left_angle = self.Lidar["left"].index(min(self.Lidar["left"]))
        rospy.loginfo(self.min_left_angle)
        self.m_l_a = False
        self.min_right_angle = 360 - self.Lidar["right"].index(min(self.Lidar["right"]))
        self.m_r_a = False
        rospy.loginfo(self.min_right_angle)
        rospy.loginfo("inagnle")
    """
    def execute(self, userdata):
        self.lost_track = False
        self.centerfound = False
        rospy.wait_for_message("/camera_data", ball_location)
        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        rospy.Subscriber("/scan", LaserScan, self.check)
        self.image_sub = rospy.Subscriber("/camera_data", ball_location , self.move_to_object)
        rate = rospy.Rate(20.0)
        
        while not rospy.is_shut_shutdown():
            if self.m_l_a == False and self.m_r_a == False:
                return "RECENTER"
            elif self.m_l_a == True and self.m_l_a == True:
                return "RECENTER"
            rate.sleep()
        return "ERROR"
def main():
    sm_top = smach.StateMachine(outcomes=["FINISHED", "ERROR"])
    with sm_top:

         smach.StateMachine.add('MIDDLE', MiddleFollow(), 
                                 transitions={'FINISHED':'FINISHED','ERROR':'RECENTER'}) 
         smach.StateMachine.add('RECENTER', Recenter(), 
                                       transitions={"MIDDLE": 'MIDDLE', 'ERROR': 'ERROR'})
         smach.StateMachine.add('DONTHITVESSELLEFT', DontHitVesselLeft(),
                                transitions={'RECENTER':'RECENTER', 'ERROR':'ERROR'})


    outcome = sm_top.execute()

if __name__ == '__main__':
    rospy.init_node("stsa")
    main()
