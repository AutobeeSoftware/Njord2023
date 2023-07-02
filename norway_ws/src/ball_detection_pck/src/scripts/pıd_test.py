#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import rospy
import time

from mavros_msgs.msg import OverrideRCIn

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion as efq
from sensor_msgs.msg import Imu
from angles import shortest_angular_distance
from std_msgs.msg import Float32
from sensor_msgs.msg import Joy

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
        

class ControllerNode:
    def __init__(self):
        msg = rospy.wait_for_message("/mavros/imu/data",Imu)
        orientation_q = msg.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = efq(orientation_list)
        self.initial_angle = yaw
        self.imu_sub = rospy.Subscriber("/mavros/imu/data", Imu, self.imu_callback)
        self.controller = PIDController(0.4, 0.0, 0.1)
        self.cmd_pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel_unstamped", Twist, queue_size=1)	
        self.fwd_cmd = 0.0

    def imu_callback(self, data):
        orientation_q = data.orientation
	angular_z = data.angular_velocity.z
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = efq(orientation_list)
        
        print yaw
        diff = shortest_angular_distance(yaw, self.initial_angle)
        tw = Twist()
        print diff
	diff = 0 if diff < 0.1 else diff
        tw.angular.z = self.controller.update(0,diff, 1.0 / 30.0)
        self.cmd_pub.publish(tw)

if __name__ == "__main__":
    rospy.init_node("sencer_node")
    a = ControllerNode()
    rospy.spin()
