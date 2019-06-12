#!/usr/bin/env python
import rospy
import sys
from std_msgs.msg import String,Bool
import speech_recognition as sr
from gtts import gTTS
import pyglet
import os
import time
from scipy.io import wavfile
import pygame
from rosarnl.srv import *



# Add goals id
door=['door','work']
circle=['center','circle']
black_board = ['Blackboard','blackboard','white board']



pub_speak = rospy.Publisher('/comprension_node/say_comprension', Bool, queue_size=10)

pub_system_stat = rospy.Publisher('/comprension_node/comprension_stat', Bool, queue_size=10)

pub_navigate = rospy.Publisher('/comprehension_node/goalname', String, queue_size=10)

def understand_callback(text):
	print(text.data)
	if 'go to' in text.data:
		if  len([elem for elem in door if elem in text.data]) != 0:
			pub_navigate.publish('door')
			pub_system_stat.publish(True)
			print('I go to the door')
		elif len([elem for elem in black_board if elem in text.data]) != 0:
			pub_navigate.publish('black_board')
			pub_system_stat.publish(True)
			print('I go to the blackboard')
		elif len([elem for elem in circle if elem in text.data]) != 0:
			pub_navigate.publish('circle')
			pub_system_stat.publish(True)
			print('I go to the center')
		else:
			print("comprehension can not understand")
			pub_speak.publish(True)

	elif 'stop' in text.data:
		pub_navigate.publish('stop')
		pub_system_stat.publish(True)
		print('stop')
	else:
		print("comprehension can not understand")
		pub_speak.publish(True)



def main():
	global rospy

	rospy.init_node('comprehension_node', anonymous=True)

	rospy.sleep(1)

	rospy.Subscriber('speech_recognition_node/activate_speech', String, understand_callback)

	rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
