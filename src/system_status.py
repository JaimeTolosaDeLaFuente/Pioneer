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
		print(faces)
		if faces > 2:
			print('hola caracola')
			pub_speak.publish(data.data)
			faces = 0
		else:
			faces += 1

def speak_stat_callback(data):
	global state
	#Pasa a modo False
	print('ya no van a entrar mas caritas bonitas')
	state = data.data


def comprension_stat_callback(data):
	global state
	print('ahora si puedo enviar caricas bonica jeje xd lol')
	#Pasa a modo True
	state = data.data


def main():

	rospy.init_node('system_status_node', anonymous=True)

	rospy.sleep(1)
	#Subscribe to the /face_detector/faces_cloud topic
	rospy.Subscriber('detection_node/face', Bool, face_cloud_callback)
	rospy.Subscriber('speak_node/speak_stat', Bool, speak_stat_callback)
	rospy.Subscriber('comprension_node/comprension_stat', Bool, comprension_stat_callback)

	#Return control to ROS
	rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
