#!/usr/bin/env python
import rospy
import sys
from std_msgs.msg import String
import os
import time
from rosarnl.srv import *
#faces
import pcl
from sensor_msgs.msg import PointField
#PointCloud, PointCloud2,

# Create the publisher to publish the topic with the next goal
pub = rospy.Publisher('detection_node/face', Bool, queue_size=10)

detect = True

def face_cloud_callback(data):
	#Comprobar formato
	print(str(data.to_list()))
	print(data.size)
	#Si detecta a alguien escucha
    if detect == True:
    	if data.size > 0:
    		pub.publish(True)
        else:
            pub.publish(False)


def main():

	rospy.init_node('detection_node', anonymous=True)

	rospy.sleep(1)
    #Subscribe to the /face_detector/faces_cloud topic
    rospy.Subscriber('face_detector/faces_cloud', PointCloud, face_cloud_callback)

	#Return control to ROS
	rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
