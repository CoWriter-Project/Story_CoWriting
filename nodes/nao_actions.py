#!/usr/bin/env python
#coding: utf-8

import sys
import time
import numpy as np
import random

import rospy
from geometry_msgs.msg import PointStamped
from std_msgs.msg import String, Empty, Header
from naoqi_bridge_msgs.msg import JointAnglesWithSpeed
import tf

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule


pub_nao_action = rospy.Publisher('joint_angles', JointAnglesWithSpeed, queue_size=1)

def head_move_msg(yaw, pitch, speed):
    msg = JointAnglesWithSpeed()
    h = Header()
    h.stamp = rospy.Time.now()
    msg.header = h
    msg.joint_names = ["HeadYaw", "HeadPitch"]
    msg.joint_angles = [yaw, pitch]
    msg.speed = speed
    return msg

#def onReceiveAction(msg):

if __name__=="__main__":

    rospy.init_node("nao_actions")

    """ Nao Bridge : """

    listener = tf.TransformListener()
    while True:
        test  = listener.getFrameStrings()
        #rospy.loginfo(test)

        if "robot_head" in test and "selection_tablet" in test:
            rospy.loginfo("frames found !!!!!!")
            (pose,rot) = listener.lookupTransform('/robot_head','/selection_tablet' , rospy.Time(0))
            x = pose[0]
            y = pose[1]
            z = pose[2]
            rospy.loginfo("x "+str(x))
            rospy.loginfo("y "+str(y))
            rospy.loginfo("z "+str(z))
            yaw = np.arctan(y/x)
            pitch = np.arctan(-z/x)
            rospy.loginfo("pitch "+str(pitch))
            rospy.loginfo("yaw "+str(yaw))

            msg = head_move_msg(yaw, pitch, 0.6)
            pub_nao_action.publish(msg)

        rospy.sleep(0.5)
    rospy.spin()
