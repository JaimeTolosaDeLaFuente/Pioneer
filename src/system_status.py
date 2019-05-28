#!/usr/bin/env python
import rospy
import sys
from std_msgs.msg import String, Bool
import os
import time


state = True

pub_speak = rospy.Publisher('system_status_node/face', Bool, queue_size=10)


def face_cloud_callback(data):
	#Si tiene que detectar, pasa la info
	print('hola soy sumorenico 19')
	if state:
		print('hola')
		pub_speak.publish(data)


def spek_stat_callback(data):
	global state
	#Pasa a modo False
	state = data


def say_comprension_callback():
	global state
	#Pasa a modo True
	state = detect



def main():

	rospy.init_node('system_status_node', anonymous=True)

	rospy.sleep(1)
	#Subscribe to the /face_detector/faces_cloud topic
	rospy.Subscriber('detection_node/face', Bool, face_cloud_callback)
	rospy.Subscriber('speak_node/speak_stat', Bool, spek_stat_callback)
	rospy.Subscriber('comprension_node/comprension_stat', String, spek_stat_callback)

	#Return control to ROS
	rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
