#!/usr/bin/env python

import rospy

from std_msgs.msg import Int32
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Vector3

dose_level = 0
params = [
    {
        "latency_queue_len": 0,
    },
    {
        "latency_queue_len": 10,
    },
    {
        "latency_queue_len": 30,
    },
    {
        "latency_queue_len": 100,
    },
]
speeds = Vector3()
latency_queue = []

def alcohol_latency(speeds):
    global latency_queue
    global params
    global dose_level
    latency_queue.append(Vector3(speeds.x, speeds.y, speeds.z))
    ret = Vector3()
    for i in range(2):
        # Repeat one more time to cut down the queue after decreasing dose level
        if len(latency_queue) > params[dose_level]["latency_queue_len"]:
            ret = latency_queue.pop(0)
    return ret

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

def fnc_callback(msg):
    global speeds
    global dose_level
    speeds.x = msg.axes[3]
    speeds.y = msg.axes[4]
    speeds.z = msg.axes[1]
    if msg.buttons[0] == 1:
        dose_level = 0
    elif msg.buttons[1] == 1:
        dose_level = 1
    elif msg.buttons[2] == 1:
        dose_level = 2
    elif msg.buttons[3] == 1:
        dose_level = 3
    # Else do not change level
   
if __name__ == '__main__':
    rospy.init_node('processor')
    pub_speeds=rospy.Publisher('speeds', Vector3, queue_size=1)
    pub_dose=rospy.Publisher('dose', Int32, queue_size=1)
    sub=rospy.Subscriber('joy', Joy, fnc_callback)

    rate = rospy.Rate(100)
    while not rospy.is_shutdown():
        speeds_processed = alcohol_latency(speeds)
        speeds_processed = rotate_vector(speeds_processed)
        pub_speeds.publish(speeds_processed)
        pub_dose.publish(dose_level)
        rate.sleep()


