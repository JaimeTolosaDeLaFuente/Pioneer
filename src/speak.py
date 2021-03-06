#!/usr/bin/env python
import rospy
import sys
from std_msgs.msg import String,Bool
import speech_recognition as sr
from gtts import gTTS
import pyglet
import os
from scipy.io import wavfile
import pygame
from rosarnl.srv import *
#faces
#import pcl
import struct
import ctypes
import time, threading

from sensor_msgs.msg import PointCloud, PointCloud2, PointField
import sensor_msgs.point_cloud2 as pc2


activate = True
pygame.mixer.init()

# Create the publisher to publish the topic with the next goal
pub_speech_recognition = rospy.Publisher('speak_node/activate_speech_recognition', Bool, queue_size=10)
pub_system_stat = rospy.Publisher('speak_node/speak_stat', Bool, queue_size=10)

def activate_timer():
	global activate
	activate = True


def face_callback(data):
	global activate
	#Cuando llega una cara te dice que hables y pasa a escucharp
	if activate == True:
		if data.data == True:
			activate = False
			pub_system_stat.publish(False)   #Desactiva envio de datos de detection
			threading.Timer(2,activate_timer).start() #En dos segundo se reactia "activate"
			print("Speak: I hear you")
			speak("I hear you")
			pub_speech_recognition.publish(True)


def say_comprehension_callback(data):
	#Cuando no entiende lo que has dicho
	print("I can't understamd, can you repeat?")
	speak("I can't understamd, can you repeat?")
	pub_speech_recognition.publish(True)

def say_navigation_callback(text):
	print('Speak:' + str(text.data)
	speak(text.data)

def speak(text):
	tts = gTTS(text)
	filename = '/tmp/temp.mp3'
	tts.save(filename)
	music = pygame.mixer.music.load(filename)
	pygame.mixer.music.play()

	time.sleep(2)
	os.remove(filename)


def main():
	global rospy

	rospy.init_node('speak_node', anonymous=True)

	rospy.sleep(1)

	rospy.Subscriber('system_status_node/face', Bool, face_callback)
	rospy.Subscriber('navigation_node/say_navigation', String, say_navigation_callback)
	rospy.Subscriber('comprension_node/say_comprension', Bool, say_comprension_callback)
	rospy.Subscriber('speech_recognition_node/speech_recognition_error', Bool, say_comprension_callback)

	rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
