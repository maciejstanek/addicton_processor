#! /usr/bin/env python
import rospy
from kinova_msgs.msg import PoseVelocity
from geometry_msgs.msg import Vector3


import math
import argparse

class Kinova():
    def __init__(self):
        self.pub = rospy.Publisher('/j2n6s300_driver/in/cartesian_velocity', PoseVelocity, queue_size=10)
        rospy.Subscriber("/speeds", Vector3, self.set_vel)
        rospy.init_node('kinova', anonymous=True)

    def set_vel(self, msg):
        self.x = msg.x
        self.y = msg.y
        self.z = msg.z

    def run(self):
        rate = rospy.Rate(100)
        while not rospy.is_shutdown():
            vel = PoseVelocity()
            vel.twist_linear_x = self.x
            vel.twist_linear_y = self.y
            vel.twist_linear_z = self.z
            vel.twist_angular_x = 0.0
            vel.twist_angular_y = 0.0
            vel.twist_angular_z = 0.0
            self.pub.publish(vel)
            rate.sleep()


if __name__ == '__main__':
    k = Kinova()
    k.run()
