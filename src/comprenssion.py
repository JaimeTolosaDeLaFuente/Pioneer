#!/usr/bin/env python
import rospy
import sys
from std_msgs.msg import String
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



pub_speak = rospy.Publisher('/comprension_node/say_comprension', String, queue_size=10)

pub_system_stat = rospy.Publisher('/comprension_node/comprension_stat', String, queue_size=10)

pub_navigate = rospy.Publisher('/comprension_node/goalname', String, queue_size=10)

def understand_callback(text):
	print(text.data)
	if 'go to' in text.data:
		if  len([elem for elem in door if elem in text.data]) != 0:
			pub_navigate.publish('door')
			pub_system_stat.publish(True)
			print('voy a la puerta')
		elif len([elem for elem in black_board if elem in text.data]) != 0:
			pub_navigate.publish('black_board')
			pub_system_stat.publish(True)
			print('voy a la pizarra')
		elif len([elem for elem in circle if elem in text.data]) != 0:
			pub_navigate.publish('circle')
			pub_system_stat.publish(True)
			print('voy a al centro')
		else:
			print("Comprension no entiende")
			pub_speak(True)

	elif 'stop' in text.data:
		pub_navigate('stop')
		pub_system_stat.publish(True)
		print('stop')
	else:
		print("Comprension no entiende")
		pub_speak(True)



def main():
	global rospy

	rospy.init_node('comprension_node', anonymous=True)

	rospy.sleep(1)

	rospy.Subscriber('speach_recognition_node/activate_speach', String, understand_callback)

	rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
