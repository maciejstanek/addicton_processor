#!/usr/bin/env python

import rospy
import numpy as np

from std_msgs.msg import Int32
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Vector3

dose_level = 0
params = [
    {
        "latency": 0,
        "inertia": 1,
        "spasm": 0,
        "drift": 0,
    },
    {
        "latency": 10,
        "inertia": 30,
        "spasm": 0,
        "drift": 0.02,
    },
    {
        "latency": 20,
        "inertia": 70,
        "spasm": 0,
        "drift": 0.05,
    },
    {
        "latency": 40,
        "inertia": 150,
        "spasm": 0.2,
        "drift": 0.1,
    },
]
def get_param(param):
    global params
    global dose_level
    return params[dose_level][param]

speeds = Vector3()
latency_queue = []
inertia_queue = []
inertia_len = []
drift_a = 0.0
drift_b = 0.0
spasm_a = 0.0
spasm_b = 0.0

def alcohol_drift(speeds, i):
    amp = get_param("drift")
    move = int(abs(speeds.x) > 1e-3 or abs(speeds.y) > 1e-3)
    speeds.x += amp * drift_a * np.sin(0.01*i) * move
    speeds.y += amp * drift_b * np.cos(0.01*i) * move
    return speeds

def alcohol_spasm(speeds):
    amp = get_param("spasm")
    speeds.x += amp * spasm_a
    speeds.y += amp * spasm_b
    return speeds

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
        if len(inertia_queue) > inertia_len:
            inertia_queue.pop(0)
    xs = [i.x for i in inertia_queue]
    ys = [i.y for i in inertia_queue]
    zs = [i.z for i in inertia_queue]
    xavg = sum(xs) / len(xs) if len(xs) > 0 else 0
    yavg = sum(ys) / len(ys) if len(ys) > 0 else 0
    zavg = sum(zs) / len(zs) if len(zs) > 0 else 0
    rospy.logwarn("dbg: {}".format(len(inertia_queue)))
    return Vector3(xavg, yavg, zavg)

def fnc_callback(msg):
    global speeds
    global dose_level
    speeds.x = -msg.axes[3]
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
    i = 0
    while not rospy.is_shutdown():
        speeds_processed = alcohol_latency(speeds)
        speeds_processed = alcohol_drift(speeds_processed, i)
        speeds_processed = alcohol_inertia(speeds_processed)
        speeds_processed = alcohol_spasm(speeds_processed)
        pub_speeds.publish(speeds_processed)
        pub_dose.publish(dose_level)
        rate.sleep()
	if i % 50 == 0:
            inertia_len = np.random.randint(get_param("inertia")+1)+1
        if i % 3 == 0:
            spasm_a = 2*np.random.rand()-1
            spasm_b = 2*np.random.rand()-1
        if i % 150 == 0:
            drift_a = 2*(np.random.rand()+0.1)-1.1
            drift_b = 2*(np.random.rand()+0.1)-1.1
        i += 1
