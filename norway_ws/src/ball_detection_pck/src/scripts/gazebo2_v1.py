#!/usr/bin/env python

import sys
import rospy
import smach
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image , LaserScan
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from ball_detection_pck.msg import ball_location 
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion as efq
class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.__integral = 0.0
        self.prev_error = 0.0
    
    def update(self, actual, target, dt):
        error = abs(target - actual)
        d = self.kd * (error - self.prev_error) / dt
        self.__integral += self.ki * error * dt
        self.prev_error = error
        #print self.__integral
        self.__integral = 0 if self.__integral > 0.2 else self.__integral
        
        return self.__integral + self.kp*error + d


class Yellow_follow(smach.State):
    
    def check(self, veri):
        
        self.Lidar = {
          "front":  min(min(veri.ranges[330:390]),30),#min(min(veri.ranges[0:30]),30,min(veri.ranges[340:360])), 40 degree
          "right":  min(min(veri.ranges[117:123]),30),
          "front-right":min(min(veri.ranges[185:330]),30),
          } 


    def __init__(self):
        self.a = 0
        smach.State.__init__(self, outcomes=["MIDDLE", "LOST", "ERROR"]) 
        self.lost_track = False
        self.centerfound = False
        self.Lidar = {
          "front":  30,
          "right":  30,
          "front-right":30,
          } 
    def move_to_object(self,data):
        rospy.Subscriber("/laser/scan", LaserScan, self.check)
        if not data.isyellowfound: 
            self.lost_track = True
            return 
        if data.isredfound and data.isgreenfound:
            self.centerfound = True
            return
        tw = Twist()

        target = (-data.yellow_location+500)/700
        tw.angular.z = target

        if self.Lidar["front-right"] < 2:
            self.a += 1
            rospy.loginfo(self.a)
            tw.angular.z = 0
        if target < 0.2:
            tw.linear.x = 0.3

        self.cmd_pub.publish(tw)

    def execute(self, userdata):
        self.lost_track = False
        self.centerfound = False
        rospy.wait_for_message("/camera_data", ball_location)
        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.image_sub = rospy.Subscriber("/camera_data", ball_location , self.move_to_object)
        rate = rospy.Rate(20.0)
        while not rospy.is_shutdown():
           if self.centerfound:
              return "MIDDLE"
           if self.lost_track:
               return "LOST"
           rate.sleep()

        return "ERROR" 


class MiddleFollow(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["FINISHED", "ERROR", "YELLOW", "BLACK"])
        self.lost_track = False 
        self.yellow = False
        self.black = False
        rospy.loginfo("middle")
    def move_to_object(self, data):
        check  = False if data.isredfound and data.isgreenfound else True
        if data.isblackfound and check:
            self.black = True
            return
        if data.isyellowfound and check:
            self.yellow = True
            return
        if not data.isredfound or not data.isgreenfound:
            self.lost_track = True
            return 

        tw = Twist()
        tw.angular.z = -data.middle/700
            
        if data.middle < 25:
            tw.linear.x = 0.4

        self.cmd_pub.publish(tw)

    def execute(self,userdata):
        
        self.yellow = False
        self.lost_track = False
        self.black = False
        rospy.loginfo('Executing state middle')
        rospy.wait_for_message("/camera_data", ball_location)
        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.image_sub = rospy.Subscriber("/camera_data", ball_location , self.move_to_object)
        rate = rospy.Rate(20.0)
        while not rospy.is_shutdown():
            if self.black:
                return "BLACK"
            if self.yellow:
                return "YELLOW"
            if self.lost_track:
                return "ERROR"
            rate.sleep()

        return "FINISHED"

class Recenter(smach.State):
    
    def __init__(self):
        
        smach.State.__init__(self, outcomes=['MIDDLE', 'ERROR', 'YELLOW', "BLACK"])
        self.tw = Twist()
        self.tw.linear.x = 0.4
        self.tw.angular.z = 0
        self.controller = PIDController(0.1, 0.1, 1/20)
        self.centerfound = False
        self.yellow = False
        self.black = False
        self.check1 = False
        self.roll = 0
        self.pitch = 0 
        self.yaw = 0
        rospy.loginfo("recenter")  
    def get_yaw(self , data):
        orientation_q = data.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (self.roll, self.pitch, self.yaw) = efq(orientation_list)
    def center(self,data):
        rospy.Subscriber("/imu", Imu , self.get_yaw)
        self.tw.linear.x = 0.4
        if data.isyellowfound:
            self.yellow = True
            return
        if data.isblackfound:
            self.black = True
            return
        if not data.isredfound and data.isgreenfound:
            if Black.Blackfinished:
                self.tw.angular.z = self.controller.update(self.yaw, 0.12,  1.0 / 30.0)
            else:
                self.tw.angular.z = self.controller.update(self.yaw, -0.12, 1.0 / 30.0)
        elif not data.isgreenfound and data.isredfound:
            if Black.Blackfinished:
                self.tw.angular.z = self.controller.update(self.yaw, -0.12, 1.0 / 30.0)
            else:
                self.tw.angular.z = self.controller.update(self.yaw, 0.12, 1.0 / 30.0)

        elif  data.isgreenfound and data.isredfound:
            self.centerfound =True
            return
        self.cmd_pub.publish(self.tw)
    def execute(self, userdata):
        self.yellow = False
        self.centerfound = False
        self.black = False
        self.tw.angular.z = 0
        rospy.loginfo('Executing state Recenter')
        rospy.wait_for_message("/camera_data", ball_location)
        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.image_sub = rospy.Subscriber("/camera_data", ball_location , self.center)
        self.tw.linear.x = 0
        rate= rospy.Rate(20)
      
        while not rospy.is_shutdown():
            if self.black:
                return "BLACK"
            if self.yellow:
                return "YELLOW"
            if self.centerfound:
                return "MIDDLE"
            rate.sleep()
            """
         if self.lost_track:

            return "ERROR"
            """
        return "FINISHED"


class Black(smach.State):
    Blackfinished = False
    def __init__(self):
        smach.State.__init__(self, outcomes=['MIDDLE', 'ERROR'])
        self.tw = Twist()
        self.tw.linear.x = 0.4
        self.tw.angular.z = 0
        self.loopbegin = False
        self.centerfound = False
        self.check1 = False
        self.Lidar = {
          "front":  30,
          "right":  30,
          "front-right":30,
          } 
    def check(self, veri):
        print("basladi")
        self.Lidar = {
          "front":  min(min(veri.ranges[330:390]),30),#min(min(veri.ranges[0:30]),30,min(veri.ranges[340:360])), 40 degree
          "right":  min(min(veri.ranges[117:123]),30),
          "front-right":min(min(veri.ranges[185:330]),30),
          } 

    def move_to_object(self,data):
        
        print("basladi")
       
        if data.isredfound and data.isgreenfound:
            self.centerfound = True
            return
        
        target = (-data.black_location+550)/700
        self.tw.angular.z = target
        if target < 0.2:
            print("los gehts")
            self.tw.linear.x = 0.3
            self.tw.linear.z = 0.0
        if self.Lidar["front-right"] < 1.2 or self.loopbegin:
            rospy.loginfo("lets begin")
            self.loopbegin = True
            self.tw.linear.x = 0.1
            self.tw.angular.z = 0.0
            if self.Lidar["right"] < 3:
                Black.Blackfinished = True
                self.check1 = True
            if self.Lidar["right"] > 2 and self.check1:
                self.tw.linear.x = 0
                self.tw.angular.z = -0.13
        self.cmd_pub.publish(self.tw)
        
            
    
    def execute(self , userdata):
        self.centerfound = False
        rospy.wait_for_message("/camera_data", ball_location)
        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        rospy.Subscriber("/laser/scan", LaserScan, self.check)
        self.image_sub = rospy.Subscriber("/camera_data", ball_location , self.move_to_object)
        rate = rospy.Rate(20.0)
        while not rospy.is_shutdown():
            
            if self.centerfound:
                self.tw.angular.z = 0
                return "MIDDLE"
            rate.sleep()

        return "ERROR"

def main():

    sm_top = smach.StateMachine(outcomes=["FINISHED", "ERROR"])
    with sm_top:

       smach.StateMachine.add('MIDDLE', MiddleFollow(), 
                                 transitions={'FINISHED':'FINISHED','ERROR':'RECENTER', 'YELLOW': 'YELLOW', 'BLACK': 'BLACK'}) 
       smach.StateMachine.add('RECENTER', Recenter(), 
                                       transitions={"MIDDLE": 'MIDDLE', 'ERROR': 'ERROR', 'YELLOW': 'YELLOW', 'BLACK': 'BLACK'})
       smach.StateMachine.add('YELLOW', Yellow_follow(), 
                              transitions={"MIDDLE": 'MIDDLE','LOST':'RECENTER' , 'ERROR': 'ERROR'})
       smach.StateMachine.add('BLACK', Black(), 
                              transitions={"MIDDLE": 'MIDDLE','ERROR':'ERROR'})
 


    outcome = sm_top.execute()
"""
def center(data):
   print("---")
def deneme():
   print("asda")
   rospy.Subscriber("/camera_data", ball_location , center)
   print("asdas")
   rate= rospy.Rate(20)
   
   print("****")
   rate.sleep()
   print("here")
   print("here2")
"""
if __name__ == '__main__':
    rospy.init_node("stsa")
    main()
