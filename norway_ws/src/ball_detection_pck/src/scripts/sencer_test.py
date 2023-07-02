#!/usr/bin/env python
import rospy
import time

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
        self.imu_sub = rospy.Subscriber("/mavros/imu/data", Imu, self.imu_callback)
        self.controller = PIDController(1.35, 0.0001, 0.8)
        self.cmd_pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel_unstamped", Twist, queue_size=1)
        self.joy_sub = rospy.Subscriber("/joy", Joy, self.joy_callback)
        self.fwd_cmd = 0.0

    def imu_callback(self, data):
        orientation_q = data.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = efq(orientation_list)
        
        print yaw
        diff = shortest_angular_distance(yaw, -0.110612555346)
        tw = Twist()
	#diff = 0 if diff < 0.01 else diff 
        tw.angular.z = self.controller.update(0.0,diff / 6.0, 1.0 / 30.0)
        tw.linear.x = self.fwd_cmd
        self.cmd_pub.publish(tw)

    def joy_callback(self, data):
        self.fwd_cmd = -data.axes[2]


if __name__ == "__main__":
    rospy.init_node("sencer_node")
    a = ControllerNode()
    rospy.spin()
