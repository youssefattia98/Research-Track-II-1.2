#! /usr/bin/env python

"""
.. module:: case_three
    :platform: Unix
    :synopsis: Python code for keyborad control obstacle avoidance case
.. moduleauthor:: Youssef Attia youssef-attia@live.com

Messages:
    /Twist
    /Vector3
    /LaserScan

"""

import rospy
import numpy
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan

#obstacle avoidnce threashold
threashold = 0.5

#initialize a Twist object for the publisher
init = Vector3(0, 0, 0)
repost = Twist( init, init)

def callingback_map(data):
    """
    This Function is only to set the data as the same value of the repost which is recived from the Twist
    """
    global repost
    repost = data  

def callingback_scans(data):
    """
    This Function is responsible for the obstacle avoidance in which it dvides the 
    data that comes from the laser scanner into three ranges *left, middle and right*
    and then checks:
    1) if something is near to the right then the repost.angular = 0
    2)if something is near to the left then the repost.angular = 0
    3)if something is near to the Front then the  repost.linear = 0
    """
    global repost
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10) #initlaizing the the publisher

    sub_right = data.ranges[0:240]
    sub_mid = data.ranges[240:480]
    sub_left = data.ranges[480:721]
    R = min(sub_right)
    F = min(sub_mid)
    L = min(sub_left)

    case3_flag = rospy.get_param("/obstacle_avoidance")
    
    if case3_flag:
        if R < threashold :
            if repost.angular.z < 0 :  
                repost.angular.z = 0    
        if F < threashold:
            if repost.linear.x > 0 :
                repost.linear.x = 0
        if L < threashold :
            if repost.angular.z > 0 :
                repost.angular.z = 0
    pub.publish(repost)

  
def keyboard_input():
    """
    This Function is to subscribe to the Twist and LaserScan topic and call Service routine functions *callingback_map & callingback_scans*

    """
    #initialize the node
    rospy.init_node('keyboard_remap_node')
    #subscriber to topic remap_cmd_vel    
    rospy.Subscriber("/remap_cmd_vel", Twist, callingback_map)
    #subscriber to topic scan
    rospy.Subscriber("/scan", LaserScan, callingback_scans)
    rospy.spin()
    
#main 
if __name__=="__main__":
    keyboard_input()