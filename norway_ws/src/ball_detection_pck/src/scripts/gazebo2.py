#!/usr/bin/env python

#from rover.msg import ball_location
import sys
import rospy
import smach
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from ball_detection_pck.msg import ball_location 
"""
class Move:
    def __init__(self):

        self.pub=rospy.Publisher('/cmd_vel',Twist,queue_size=10)
        self.rate=rospy.Rate(1)
        self.rot=Twist()
        self.x = 1
        self.cx_r=0
        self.cy_r=0
        
        self.cx_g=0
        self.cy_g=0
        
        self.bridge = CvBridge()
        self.image_received = False

        # Connect image topic
        self.img_topic = "/camera_data"
        self.image_sub = rospy.Subscriber(self.img_topic, ball_location , self.move_to_object)

        # Allow up to one second to connection
        rospy.sleep(1)




    def move_to_object(self,data):
        obj_x = data.middle 
        self.rot.linear.x=0.4
        print("red", data.isredfound)
        print("green",data.isgreenfound)
        if (data.isgreenfound and data.isredfound) :
            self.rot.angular.z = -obj_x/700
            print("orta")
        elif data.isredfound:
            print("-----left-------")
            self.rot.angular.z = 0.2
        elif data.isgreenfound:
            print("----------right-------")
            self.rot.angular.z = -0.2

            
        print(obj_x)
        self.pub.publish(self.rot)

class Yellow(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["FINISHED", "LOST", "ERROR"])
        self.lost_track = False 

    def move_to_object(self,data):
        if not data.isredfound or not data.isgreenfound:
            self.lost_track = True
            return 

        tw = Twist()
        tw.angular.z = -data.middle/700
        
        if data.middlle < 10:
            tw.linear.x = 0.3

        self.cmd_pub.publish(tw)

    def exacute():
        rospy.wait_for_message("/camera_data", ball_location)
        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.image_sub = rospy.Subscriber("/camera_data", ball_location , self.move_to_object)
        rate = rospy.Rate(20.0)
        while not rospy.is_shutdown():
            if self.lost_track:
                return "LOST"
            rate.sleep()

        return "FINISHED"

"""
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
         tw.linear.x = 0.3

      self.cmd_pub.publish(tw)

   def execute(self,userdata):
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
      smach.State.__init__(self, outcomes=['Middle', 'ERROR'])
      self.tw = Twist()
      self.tw.linear.x = 0.2
      self.lost_track = False
      self.centerfound = False
   def center(self,data):
      if not data.isredfound and data.isgreenfound:
         self.tw.angular.z = -0.2
      elif not data.isgreenfound and data.isredfound:
         self.tw.angular.z = 0.2
      elif not data.isgreenfound and not data.isredfound:
         self.lost_track = True
         return
      elif  data.isgreenfound and data.isredfound:
         self.centerfound =True
         return
      self.cmd_pub.publish(self.tw)
   def execute(self, userdata):
      print("while disi")
      rospy.loginfo('Executing state Recenter')
      rospy.wait_for_message("/camera_data", ball_location)
      self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
      self.image_sub = rospy.Subscriber("/camera_data", ball_location , self.center)
      tw = Twist()
      tw.linear.x = 0
      rate= rospy.Rate(20)
      
      while not rospy.is_shutdown():
         if self.centerfound:
            return "Middle"
         rate.sleep()
         """
         if self.lost_track:

            return "ERROR"
         """
      return "FINISHED"

def main():
    sm_top = smach.StateMachine(outcomes=["FINISHED", "ERROR"])
    with sm_top:

         smach.StateMachine.add('ASS', MiddleFollow(), 
                                 transitions={'FINISHED':'FINISHED','ERROR':'RECENTER'}) 
         smach.StateMachine.add('RECENTER', Recenter(), 
                                       transitions={"Middle": 'ASS', 'ERROR': 'ERROR'})
 


    outcome = sm_top.execute()

if __name__ == '__main__':
    rospy.init_node("stsa")
    main()
