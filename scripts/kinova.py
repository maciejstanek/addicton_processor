#! /usr/bin/env python
import rospy
from kinova_msgs.msg import PoseVelocity
from geometry_msgs.msg import Vector3


import math
import argparse

def talker():
	pub = rospy.Publisher('/j2n6s300_driver/in/cartesian_velocity', PoseVelocity, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(100)
	while not rospy.is_shutdown():
	#for i in range(5):
		vel = PoseVelocity()
		vel.twist_linear_x = 0.0
		vel.twist_linear_y = 0.0
		vel.twist_linear_z = 0.1
		vel.twist_angular_x = 0.0
		vel.twist_angular_y = 0.0
		vel.twist_angular_z = 0.0
		pub.publish(vel)
		rate.sleep()

if __name__ == '__main__':
	talker()
