import rospy
import sys
import os 
import time
import rosarnl.srv import *
from std_msgs.msg import String
from std_msgs.msg import Empty
#from Pionner.msg import Navigate_Comprenssion 


pub = rospy.Publisher('/rosarnl_node/goalname',String,queue_size = 10)
pub_speak = rospy.Publisher('speak_node/Say_Navigation',String,queue_size = 10)


door=['door','work']
circle=['center','circle']
black_board = ['Blackboard','blackboard','white board']

def state_callback(data):
    rospy.loginfo("ARNL path state: " + data.data)
	if data.data == 'REACHED_GOAL':
        pub_speak.publish('I stop')

def navigation_callback(data):
    if data == 'stop':
        rospy.ServiceProxy("/rosarnl_node/stop",Empty) #Debería de funcionar
    elif data == 'door':
        pub.publish('door')
        pub_speak.publish('Go to the door')
    elif len([elem for elem in black_board if elem in text]) != 0:
        pub.publish('black_board')
        pub_speak.publish('Go to the blackboard')
    elif len([elem for elem in circle if elem in text]) != 0:
        pub.publish('circle')
        pub_speak.publish('Go to the circle')
    elif data == 'hello':
        pub_speak.publish('Hello bro')




def main():

    global rospy

	rospy.init_node('navigation_node', anonymous=True)

	rospy.sleep(1)
	print("sale sleep")

    rospy.Subscriber('rosarnl_node/arnl_path_state', String, state_callback)

    rospy.Subscriber('comprenssion_node/Navigate_Comprenssion',Navigate_Comprenssion,navigation_callback)
    #Return control to Ros
    rospy.spin()    

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
