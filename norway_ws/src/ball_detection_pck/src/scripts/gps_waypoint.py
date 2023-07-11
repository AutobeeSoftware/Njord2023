#!/usr/bin/env python

import smach
import smach_ros
import rospy
from mavros_msgs.msg import GlobalPositionTarget
from time import sleep
from sensor_msgs.msg import NavSatFix
import math
from geographic_msgs.msg import GeoPoseStamped
from tf.transformations import euler_from_quaternion as efq
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from angles import shortest_angular_distance

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

class Waypoint():
    
    waypoints = [(41.1026,43.123213),
                (41.1026 , 5)]
    
    def __init__(self,number):
        self.yaw , self.roll, self.pitch = 0 , 0 ,0
        location= GeoPoseStamped()
        self.controller = PIDController(2.35, 0.0001, 0.8)
        self.cmd_pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel_unstamped", Twist, queue_size=1)
        tp_error_radius = 0
        #location.velocity.x = 0.3
        #location.coordinate_frame=6
        location.pose.position.latitude, location.pose.position.longitude = Waypoint.waypoints[number]
        while self.cmd_pub.get_num_connections() == 0 and not rospy.is_shutdown():
            print"...connecting"
            sleep(.1)
        self.msg = rospy.wait_for_message("/mavros/global_position/raw/fix",NavSatFix)
        print self.get_distance_meters(location.pose.position,self.msg)
        while self.get_distance_meters(location.pose.position,self.msg) > tp_error_radius and not rospy.is_shutdown():
            rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, self.check)
            rospy.Subscriber("/mavros/imu/data", Imu, self.imu_callback)
            self.go_to()
            sleep(.05)
            print self.get_distance_meters(location.pose.position,self.msg)
            
        return

        
    def get_distance_meters(self,targetLocation,currentLocation):
            dLat=targetLocation.latitude - currentLocation.latitude
            dLon=targetLocation.longitude - currentLocation.longitude
            self.distance_x = dLon*1.113195e5
            self.distance_y = dLat*1.113195e5
            return math.sqrt((dLon*dLon)+(dLat*dLat))*1.113195e5
    def go_to(self):
        tw = Twist()
        angle = math.atan2(self.distance_y,self.distance_x)
        target_angle = -angle                                            # BURAYI TEKRAR KONTROL ET
        diff = shortest_angular_distance(self.yaw, target_angle)
        print "diff:" , diff 
        tw.angular.z = self.controller.update(0.0, diff/7, 1.0 / 20.0)
        tw.linear.x = 0.7 - diff/2 if (0.7 - diff*2/5) > 0 else 0 
        self.cmd_pub.publish(tw)



    def get_angle(self, msg):
        orientation_q = msg.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (self.roll, self.pitch, self.yaw) = efq(orientation_list)
        print "yaw ====",self.yaw

        return self.yaw

    def imu_callback(self, data):
        self.yaw = self.get_angle(data)

    def check(self,data):
        self.msg = data







rospy.init_node('sexy_node')
Waypoint(1)
