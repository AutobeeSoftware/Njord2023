#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
from angles import shortest_angular_distance
from tf.transformations import euler_from_quaternion as efq 


class PID_Controller:
    def __init__(self, kp, ki, kd):
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd
        
    def update(self, theta_des, theta_act, dt):
        error_int = 0
        e = theta_des - theta_act
        de_dt = -theta_act/dt
        error_int = error_int + e*dt
        
        u = self.Kp*e + self.Ki*error_int + self.Kd*de_dt
        
        return u

class ControllerNode:
    def __init__(self):
        self.imu_sub = rospy.Subscriber("/mavros/imu/data", Imu, self.imu_callback)
        self.controller = PID_Controller(1.35, 0.0001, 0.8)
        self.cmd_pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel_unstamped", Twist, queue_size=1)
    def imu_callback(self, data):
        orientation_q = data.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, self.yaw) = efq(orientation_list)
        print(self.yaw)
        
        self.diff = shortest_angular_distance(self.yaw, 0.0)       
        print("Diff: ", self.diff)
	
        self.location_callback()
    def location_callback(self):
        tw = Twist()
        tw.angular.z = self.controller.update(0.0, self.diff/100, 1.0/30.0)
        self.cmd_pub.publish(tw)


if __name__ == "__main__":
        rospy.init_node("hakan_node")
        a=ControllerNode()
        rospy.spin()
