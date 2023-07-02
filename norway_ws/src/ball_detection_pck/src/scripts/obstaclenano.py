#!/usr/bin/env python

from ball_detection_pck.msg import ball_location
import smach
import rospy
import smach_ros
import time
import scipy 
import numpy as np
from mavros_msgs.msg import OverrideRCIn
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion as efq
from sensor_msgs.msg import Imu
from angles import shortest_angular_distance
from std_msgs.msg import Float32
import math
from sensor_msgs.msg import Image , LaserScan
from mavros_msgs.srv import SetMode, SetModeRequest

class PIDController: 
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.__integral = 0.0
        self.prev_error = 0.0
    
    def update(self, actual, target, dt):
        error = target - actual
        d = self.kd * (error - self.prev_error) / dt
        self.__integral += self.ki * error * dt
        self.prev_error = error
        
        return self.__integral + self.kp*error + d

class Rotate():
   def __init__(self,degree,way,linear):
      print("Start rotate state")
      msg = rospy.wait_for_message("/mavros/imu/data",Imu)
      print("asda")
      controller = PIDController(2.35, 0.0001, 0.8)
      initial_yaw = self.get_angle(msg)
      self.yaw = 0.0
      cmd_pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel_unstamped", Twist, queue_size=1)
      imu_sub = rospy.Subscriber("/mavros/imu/data", Imu, self.imu_callback)
      settle_time = 2.0
      angle_region_threshold = 0.2 
      target_angle = initial_yaw + math.radians(degree) if way == 1 else initial_yaw - math.radians(degree)

      print ("initial_yaw", initial_yaw, "target_yaw", target_angle)

      last_time = rospy.Time.now()
      rate = rospy.Rate(20)
      while not rospy.is_shutdown() and (rospy.Time.now() - last_time).to_sec() < settle_time:
         diff = shortest_angular_distance(self.yaw, target_angle)
         print("yaw", self.yaw, "target", target_angle, "err", diff)
         if abs(diff) >= angle_region_threshold:
             last_time = rospy.Time.now()
             
         
         tw = Twist()
         tw.angular.z = controller.update(0.0, diff/5, 1.0 / 20.0)
         tw.linear.x = linear
         cmd_pub.publish(tw)
         rate.sleep()
   def get_angle(self, msg):
      orientation_q = msg.orientation
      orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
      (roll, pitch, yaw) = efq(orientation_list)
      return yaw

   def imu_callback(self, data):
      self.yaw = self.get_angle(data)

class MiddleFollow(smach.State):
   def __init__(self):
      smach.State.__init__(self, outcomes=["FINISHED", "ERROR"])
      self.lost_track = False 
      rospy.loginfo("middle")
   def move_to_object(self, data):
      check  = False if data.isredfound and data.isgreenfound else True
      if not data.isredfound or not data.isgreenfound:
         self.lost_track = True
         return 

      tw = Twist()
      tw.angular.z = -data.middle/700
            
      if data.middle < 25:
         tw.linear.x = 0.4

      self.cmd_pub.publish(tw)

   def execute(self,userdata):
      self.lost_track = False
      rospy.loginfo('Executing state middle')
      rospy.wait_for_message("/camera_data", ball_location)
      self.cmd_pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel_unstamped", Twist, queue_size=1)
      self.image_sub = rospy.Subscriber("/camera_data", ball_location , self.move_to_object)
      rate = rospy.Rate(20.0)
      while not rospy.is_shutdown():

         if self.lost_track:
            return "ERROR"
         rate.sleep()

      return "FINISHED"

class Start(smach.State):
   def check(self, veri):
      self.Lidar = {
        "front":  min(min(veri.ranges[0:30]),30,min(veri.ranges[340:360])),
        "left":  min(min(veri.ranges[445:455]),30),
        "front-right":min(min(veri.ranges[280:340]),30),
        }
      #print  self.Lidar["left"]
      #print veri.ranges[440:460].index(min(veri.ranges[440:460]))
      self.tw.linear.x = 0.5
      self.cmd_pub.publish(self.tw)
      if self.Lidar["left"] < 1.2  or self.let:
         #print("here")
         self.let = True

         if self.Lidar["left"] > 1.2 :
            self.calculate = True
         return 

      self.cmd_pub.publish(self.tw)
   def __init__(self):
      smach.State.__init__(self, outcomes=["CALCULATE",'FINISHED'])
      self.lost_track = False 
      self.Lidar = {
        "front":  30,
        "left":  30,
        "front-right":30,
        }   
      self.let = False
      self.calculate = False
      self.tw = Twist()
   def execute(self,userdata):
      self.lost_track = False
      rospy.loginfo('Executing state start')
      rospy.wait_for_message("/sick_lms_1xx/scan", LaserScan)
      self.cmd_pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel_unstamped", Twist, queue_size=1)
      rospy.Subscriber("/sick_lms_1xx/scan", LaserScan, self.check)
      rate = rospy.Rate(50.0)
      while not rospy.is_shutdown():
         if self.calculate:
            return "CALCULATE"
         rate.sleep()

      return "FINISHED"

class Recenter(smach.State):
   def __init__(self):
      smach.State.__init__(self, outcomes=['MIDDLE','FINISHED'])
      self.tw = Twist()
      self.tw.linear.x = 0.4
      self.tw.angular.z = 0

      self.centerfound = False
      self.yellow = False
      self.black = False
      self.check1 = False
      self.calculate = False
      rospy.loginfo("recenter")
   def center(self,data):
      self.tw.linear.x = 0.4
      if data.isyellowfound:
         self.yellow = True
         return
      if data.isblackfound:
         self.black = True
         return
      if not data.isredfound and data.isgreenfound:
         self.tw.angular.z = -0.18
      elif not data.isgreenfound and data.isredfound:
         self.tw.angular.z = 0.18
      elif not data.isredfound and not data.isgreenfound:
         self.tw.angular.z = 0
      elif data.isgreenfound and data.isredfound:
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
      self.cmd_pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel_unstamped", Twist, queue_size=1)
      self.image_sub = rospy.Subscriber("/camera_data", ball_location , self.center)
      self.tw.linear.x = 0
      rate= rospy.Rate(20)
      
      while not rospy.is_shutdown():
         if self.centerfound:
            return "MIDDLE"
         if self.calculate:
            return "CALCULATE"
         rate.sleep()

      return "FINISHED"


class Calculate(smach.State):
   def __init__(self):
      smach.State.__init__(self, outcomes=['WAIT','RUN','ERROR'])
      self.tw = Twist()
      self.action = False
      self.tw.linear.x = 0.4
      self.tw.angular.z = 0
      self.cordinatsy = []
      self.cordinatsx = []
      self.liste = 0
      self.Lidar = {
        "front":  30,
        "right":  30,
        "front-right":30,
        } 
      self.Lidarindex = {
        "front-left":  0,
        "right": 0,
        "front":0,
        }
   def check(self, veri):
      value = min(i for i in veri.ranges[300:400] if 1<= i <=30)
      print "calc",value
      self.Lidar = {
        "front-left" : value , 
        "right":  min(min(veri.ranges[268:272]),30),
        "front-right":min(min(veri.ranges[280:340]),30),
        } 
      self.Lidarindex = {
        "front-left":  veri.ranges[300:400].index(value),
        "right":  min(min(veri.ranges[70:110]),30),
        "front":min(min(veri.ranges[280:340]),30),
        }
      if self.liste <150 and self.liste % 3 == 0 :
         self.linearfit()
      else:

         m , b = np.polyfit(self.cordinatsx, self.cordinatsy,1)
         print "b", b
         Calculate.rotation = m
         print "slope", Calculate.rotation
         self.method = 'WAIT' #if intercept > 0 else 'RUN'
         self.action = True 
      self.liste += 1
   def linearfit(self):
       y = self.Lidar["front-left"]*math.sin(math.radians(15 +self.Lidarindex["front-left"]/2))
       x = self.Lidar["front-left"]*math.cos(math.radians(15 +self.Lidarindex["front-left"]/2))
       self.cordinatsy.append(y)
       self.cordinatsx.append(x)
       self.liste += 1
   def execute(self , userdata):
      self.centerfound = False
      self.cmd_pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel_unstamped", Twist, queue_size=1)
      rospy.Subscriber("/sick_lms_1xx/scan", LaserScan, self.check)
      rate = rospy.Rate(5.0)
      self.tw.linear.x = 0.4
      while not rospy.is_shutdown():
         if self.action:
            return self.method
         if self.centerfound:
            self.tw.angular.z = 0
            return "FINISHED"
         rate.sleep()

      return "ERROR"
class Wait(smach.State):
   def __init__(self):
      smach.State.__init__(self, outcomes=['FINISHED', 'ERROR'])
      self.tw = Twist()
      self.tw.linear.x = 0.4
      self.tw.angular.z = 0
      self.loopbegin = False
      self.rotated = False
      self.centerfound = False
      self.check1 = False
      self.action = False
      self.action2 = True
      self.Lidar = {
        "front":  30,
        "right":  30,
        "front-right":30,
        } 
   def check(self, veri):
    
      value = min(i for i in veri.ranges[85:100] if 0.1<= i <=30)
      print "please work",value
      self.Lidar = {
        "right":  value,
        "front-right":min(min(veri.ranges[280:340]),30),
        } 
      self.move_to_object()
   def move_to_object(self):
      print(self.rotated)
      if not self.rotated:
         print("rotatedddddddd")
         Rotate(60 , 1, 0.5)
         self.rotated = True
      self.tw.angular.z = 0
      if self.action2:
         self.tw.linear.x = 0.2
      else:
         self.tw.linear.x = 0.6
      print "-----------------------",self.Lidar["right"]
      self.cmd_pub.publish(self.tw)
      if (self.Lidar["right"] < 5 or self.action) and self.action2:
         self.action = True
         self.tw.linear.x = 0.4
         print "here1"
         self.cmd_pub.publish(self.tw)
         if self.Lidar["right"] > 2:
            print "here2"
            

            Rotate(80 , 0, 0.7)
            self.action2 = False
      self.cmd_pub.publish(self.tw)
   def execute(self , userdata):
      self.cmd_pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel_unstamped", Twist, queue_size=1)
      rospy.Subscriber("/sick_lms_1xx/scan", LaserScan, self.check)

      rate = rospy.Rate(20.0)
      while not rospy.is_shutdown():
         if not self.action2:
            return "FINISHED"
         rate.sleep()

      return "ERROR"

class Run(smach.State):
   def __init__(self):
      smach.State.__init__(self, outcomes=['FINISHED'])
      self.tw = Twist()
      self.finished = False
   def execute(self, userdata):
      self.yellow = False

      self.centerfound = False
      self.black = False
      self.tw.angular.z = 0
      rospy.loginfo('Executing state RUN')
      self.cmd_pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel_unstamped", Twist, queue_size=1)
      Rotate(45,0,0.7)
      print("ROTATED")
      Rotate(45,1,0.7)
      print("ROTATED AGAIN")
      return 'FINISHED'
class SetModeState(smach.State):
    def __init__(self, mode = "MANUAL"):
        smach.State.__init__(self, outcomes=["FINISHED", "ERROR"])
        self.mode = mode

    def execute(self, userdata):
        srv = rospy.ServiceProxy("/mavros/set_mode", SetMode)
        srv.wait_for_service()

        req = SetModeRequest()
        req.custom_mode = self.mode
        resp = srv.call(req)

        if resp.mode_sent:
            return "FINISHED"
        else:
            return "ERROR"
        

      
def main():
   sm_top = smach.StateMachine(outcomes=["FINISHED", "ERROR"])
   sis = smach_ros.IntrospectionServer('server_name', sm_top, '/SM_ROOT')
   with sm_top:
      smach.StateMachine.add('SETMODE', SetModeState(), 
                                 transitions={'FINISHED':'START','ERROR':'ERROR'}) 
      smach.StateMachine.add('START', Start(), 
                                 transitions={'CALCULATE':'CALCULATE','FINISHED':'FINISHED'}) 
      smach.StateMachine.add('CALCULATE', Calculate(), 
                                 transitions={'WAIT':'WAIT','RUN':'RUN','ERROR':'ERROR'}) 
      smach.StateMachine.add('WAIT', Wait(), 
                                 transitions={'FINISHED':'MIDDLE','ERROR':'ERROR'}) 
      smach.StateMachine.add('RUN', Run(), 
                                 transitions={'FINISHED':'MIDDLE'}) 
      smach.StateMachine.add('RECENTER', Recenter(), 
                                 transitions={'MIDDLE':'MIDDLE','FINISHED':'FINISHED'})
      smach.StateMachine.add('MIDDLE', MiddleFollow(), 
                                 transitions={'ERROR':'RECENTER','FINISHED':'FINISHED'})


   sis.start()
   outcome = sm_top.execute()

if __name__ == '__main__':
   rospy.init_node("stsa")
   main()
