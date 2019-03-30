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

def rotate_vector(v):
    rvec = Vector3()
    rvec.x = 0.48808 * v.x + 0.24668 * v.y + 0.05319  * v.z
    rvec.y = 0.1657  * v.x + 0.28382 * v.y + 0.049499 * v.z
    rvec.z = 0.5203  * v.x + 0.67565 * v.y + 0.06884  * v.z

    return rvec

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
        speeds_processed = rotate_vector(speeds_processed)
        pub.publish(speeds_processed)
        rate.sleep()


