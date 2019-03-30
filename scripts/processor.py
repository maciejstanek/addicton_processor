#!/usr/bin/env python

import rospy

from std_msgs.msg import Int32
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Vector3

dose_level = 0
params = [
    {
        "latency": 0,
        "inertia": 0,
    },
    {
        "latency": 10,
        "inertia": 10,
    },
    {
        "latency": 30,
        "inertia": 30,
    },
    {
        "latency": 100,
        "inertia": 100,
    },
]
def get_param(param):
    global params
    global dose_level
    return params[dose_level][param]

speeds = Vector3()
latency_queue = []
inertia_queue = []

def alcohol_latency(speeds):
    global latency_queue
    global params
    global dose_level
    latency_queue.append(Vector3(speeds.x, speeds.y, speeds.z))
    ret = Vector3()
    for i in range(2):
        # Repeat one more time to cut down the queue after decreasing dose level
        if len(latency_queue) > get_param("latency"):
            ret = latency_queue.pop(0)
    return ret

def alcohol_inertia(speeds):
    global inertia_queue
    global params
    global dose_level
    inertia_queue.append(Vector3(speeds.x, speeds.y, speeds.z))
    for i in range(2):
        # Repeat one more time to cut down the queue after decreasing dose level
        if len(inertia_queue) > get_param("inertia"):
            inertia_queue.pop(0)
    xs = [i.x for i in inertia_queue]
    ys = [i.y for i in inertia_queue]
    zs = [i.z for i in inertia_queue]
    xavg = sum(xs) / len(xs) if len(xs) > 0 else 0
    yavg = sum(ys) / len(ys) if len(ys) > 0 else 0
    zavg = sum(zs) / len(zs) if len(zs) > 0 else 0
    return Vector3(xavg, yavg, zavg)

def rotate_vector(v):
    rvec = Vector3()
    rvec.x =  1.0000000 * v.x +  0.0000000 * v.y +  0.0000000 * v.z
    rvec.y =  0.0000000 * v.x +  1.0000000 * v.y +  0.0000000 * v.z
    rvec.z =  0.0113733 * v.x +  0.0368313 * v.y +  0.9992568 * v.z

    return rvec

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
        #speeds_processed = alcohol_inertia(speeds)
        speeds_processed = rotate_vector(speeds_processed)
        pub_speeds.publish(speeds_processed)
        pub_dose.publish(dose_level)
        rate.sleep()


