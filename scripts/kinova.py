#! /usr/bin/env python
import rospy
from kinova_msgs.msg import PoseVelocity
from geometry_msgs.msg import Vector3, Point, Quaternion

import math
import argparse

class Kinova():

    def rebase(self, msg):
        if not msg.data:
            return

        position = [0.346, 0.439, 0.061]
        orientation = [-0.15, -0.691, -0.706, -0.004]

        client = actionlib.SimpleActionClient('/j2n6s300_driver/pose_action/tool_pose', kinova_msgs.msg.ArmPoseAction)
        client.wait_for_server()

        goal = kinova_msgs.msg.ArmPoseGoal()
        goal.pose.header = std_msgs.msg.Header(frame_id=('j2n6s300_link_base'))
        goal.pose.pose.position = geometry_msgs.msg.Point(
            x=position[0], y=position[1], z=position[2])
        goal.pose.pose.orientation = geometry_msgs.msg.Quaternion(
            x=orientation[0], y=orientation[1], z=orientation[2], w=orientation[3])

        rospy.logwarn('goal.pose in client 1: {}'.format(goal.pose.pose)) # debug

        client.send_goal(goal)

        if client.wait_for_result(rospy.Duration(10.0)):
            return #client.get_result()
        client.cancel_all_goals()
        rospy.logerr('the cartesian action timed-out')
        return #None

    def __init__(self):
        self.pub = rospy.Publisher('/j2n6s300_driver/in/cartesian_velocity', PoseVelocity, queue_size=10)
        rospy.Subscriber("/speeds", Vector3, self.set_vel)
        rospy.Subscriber("/rebase", Vector3, self.rebase)
        rospy.init_node('kinova', anonymous=True)

    def set_vel(self, msg):
        self.x = 0.1*msg.x
        self.y = 0.1*msg.y
        self.z = 0.1*msg.z

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
