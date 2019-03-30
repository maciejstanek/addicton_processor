#!/usr/bin/env python

import rospy

from std_msgs.msg import Int32
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Vector3

latency_queue = []
latency_queue_len = 100

def alcohol_latency(speeds):
    global latency_queue
    global latency_queue_len
    latency_queue.append(Vector3(speeds.x, speeds.y, speeds.z))
    if len(latency_queue) > latency_queue_len:
        return latency_queue.pop(0)
    return Vector3()

# latency_queue = []
# latency_queue_len = 100
# 
# def alcohol_slide(speeds):
#     global slide_queue
#     global slide_queue_len
#     slide_queue.append(speeds)
#     if len(latency_queue) > latency_queue_len:
#         latency_queue.pop(0)
#     # x = [i for i in 

speeds = Vector3()

def fnc_callback(msg):
    global speeds
    speeds.x = msg.axes[3]
    speeds.y = msg.axes[4]
    speeds.z = msg.axes[1]
   
if __name__ == '__main__':
    rospy.init_node('processor')
    pub=rospy.Publisher('speeds', Vector3, queue_size=1)
    sub=rospy.Subscriber('joy', Joy, fnc_callback)

    rate = rospy.Rate(100)
    while not rospy.is_shutdown():
        speeds_processed = alcohol_latency(speeds)
        pub.publish(speeds_processed)
        rate.sleep()


