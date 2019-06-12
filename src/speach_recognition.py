#!/usr/bin/env python
import rospy
import sys
from std_msgs.msg import String, Bool
import speech_recognition as sr
import pyglet
import os
import time
from scipy.io import wavfile
import pygame
from rosarnl.srv import *


# Create the publisher to publish the topic with the next goal
pub_speach = rospy.Publisher('speach_recognition_node/activate_speach', String, queue_size=10)
pub_error = rospy.Publisher('speach_recognition_node/speach_recognition_error', Bool, queue_size=10)



def escucha_micro_callback(data):
	r = sr.Recognizer()
	time.sleep(1)
	print(data.data)
	with sr.Microphone() as source:
		#speak('Say something!')
		print('Say something!')
		try:
			audio = r.listen(source,10)
		except sr.WaitTimeoutError:
			print('OHHHH DIOS MIO NO TE HE ENTENDIDO')
			audio = None
			pub_error.publish(True)

			
	print("Okey")
	text = ''
	#fs, data = wavfile.read('pruebasonido.wav')
	try:
		if audio != None:
			text = r.recognize_google(audio)
	except sr.UnknownValueError :
		print("Error 1 - No entiende nada")
		pub_error.publish(True)

	except sr.RequestError as e:
		print ("Error 2 - Could not request results from Google Speech Recognition service")

	print('->' + str(text))
	if text != '':
		pub_speach.publish(text)


def main():

	rospy.init_node('speach_recognition_node', anonymous=True)
	rospy.sleep(1)

	#Subscribe to speak
	rospy.Subscriber('speak_node/activate_speach_recognition', Bool, escucha_micro_callback)

	rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
