#!/usr/bin/env python

import rospy
import sys
import os
import time
from std_msgs.msg import String
from std_msgs.msg import Empty
#from Pionner.msg import Navigate_Comprenssion


pub = rospy.Publisher('rosarnl_node/goalname',String,queue_size = 10)
pub_speak = rospy.Publisher('navigation_node/say_navigation',String,queue_size = 10)


def state_callback(data):

	rospy.loginfo("ARNL path state: " + data.data)
	if data.data == 'REACHED_GOAL':
		pub_speak.publish('Goal reached')

def navigation_callback(data):
	print(data.data)
	if data.data == 'stop':
		rospy.ServiceProxy("/rosarnl_node/stop",Empty) #Debería de funcionar
		pub_speak.publish('I stop')

	else:
		pub.publish(data.data)
		msg = 'Going to' + str(data.data)
		pub_speak.publish(msg)

def main():

	global rospy

	rospy.init_node('navigation_node', anonymous=True)

	rospy.sleep(1)
	print("sale sleep")

	rospy.Subscriber('rosarnl_node/arnl_path_state', String, state_callback)

	rospy.Subscriber('comprension_node/goalname',String,navigation_callback)
	#Return control to Ros
	rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
