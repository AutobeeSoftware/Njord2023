#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
from geometry_msgs.msg import Twist

class BallFollower:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/image", Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

    def image_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
            #return

        # Görüntüyü işleme kodları burada yer alır
        # Örneğin, renk uzayını değiştirip yeşil ve kırmızı renkleri tespit edebilirsiniz

        # Yeşil ve kırmızı renklerin maskesini oluşturun
        hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        green_lower = np.array([50, 100, 100])
        green_upper = np.array([70, 255, 255])
        green_mask = cv2.inRange(hsv_image, green_lower, green_upper)

        red_lower = np.array([0, 100, 100])
        red_upper = np.array([10, 255, 255])
        red_mask1 = cv2.inRange(hsv_image, red_lower, red_upper)

        red_lower = np.array([170, 100, 100])
        red_upper = np.array([180, 255, 255])
        red_mask2 = cv2.inRange(hsv_image, red_lower, red_upper)

        red_mask = cv2.bitwise_or(red_mask1, red_mask2)

        # Yeşil ve kırmızı topların konturunu bulun
        green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Yeşil topların ağırlık merkezini hesaplayın
        green_center = None
        if len(green_contours) > 0:
            green_contour = max(green_contours, key=cv2.contourArea)
            M = cv2.moments(green_contour)
            green_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Kırmızı topların ağırlık merkezini hesaplayın
        red_center = None
        if len(red_contours) > 0:
            red_contour = max(red_contours, key=cv2.contourArea)
            M = cv2.moments(red_contour)
            red_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Aracın hareketini hesaplayın
        if green_center is not None and red_center is not None:
            # Topların ortasını hesaplayın
            target_x = (green_center[0] + red_center[0]) / 2
            target_y = (green_center[1] + red_center[1]) / 2

            # Hareket talimatlarını hesaplayın
            twist_msg = Twist()
            twist_msg.linear.x = 0.2  # Örneğin, sabit bir hızda ileri gitmek için
           ### twist_msg.angular.z = 0.01 * (target_x - cv_image.shape[1] / 2)  # Örneğin, hedefe doğru dönme için

            # Aracın hedefin solunda mı yoksa sağındamı olduğunu kontrol edin
            if target_x < cv_image.shape[1] / 2:
                twist_msg.angular.z = 0.1  # Örneğin, sola dönme
            else:
                twist_msg.angular.z = -0.1  # Örneğin, sağa dönme
            
            # Hareket talimatlarını yayınlayın
            self.cmd_vel_pub.publish(twist_msg)

    def run(self):
        rospy.init_node("ball_follower")
        rospy.spin()

if __name__ == '__main__':
    ball_follower = BallFollower()
    ball_follower.run()
