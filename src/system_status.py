#!/usr/bin/env python
import rospy
import sys
from std_msgs.msg import String, Bool
import os
import time


state = True
faces = 0

pub_speak = rospy.Publisher('system_status_node/face', Bool, queue_size=10)


def face_cloud_callback(data):
    global faces
    #Si tiene que detectar, pasa la info
    if state:
        if faces > 5:
            pub_speak.publish(data.data)
            faces = 0
        else:
            faces += 1

def spek_stat_callback(data):
    global state
    #Pasa a modo False
    state = data.data


def comprehension_stat_callback(data):
    global state
    #Pasa a modo True
    state = data.data


def main():

	rospy.init_node('system_status_node', anonymous=True)

	rospy.sleep(1)
    #Subscribe to the /face_detector/faces_cloud topic
    rospy.Subscriber('detection_node/faces', Bool, face_cloud_callback)
    rospy.Subscriber('speak_node/spek_stat', Bool, spek_stat_callback)
    rospy.Subscriber('comprehension_node/comprehension_stat', Bool, comprehension_stat_callback)

	#Return control to ROS
	rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
