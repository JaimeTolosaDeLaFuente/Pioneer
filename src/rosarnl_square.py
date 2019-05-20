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
finish = False
door=['door','work']
circle=['center','circle']
black_board = ['Blackboard','blackboard','white board']
finish = False
# Create the publisher to publish the topic with the next goal
pub = rospy.Publisher('/rosarnl_node/goalname', String, queue_size=10)
stop = rospy.Publisher('/rosarnl_node/goalname', String, queue_size=10)

def escucha_micro():
	r = sr.Recognizer()
	time.sleep(1)
	with sr.Microphone() as source:
		speak('Say something!')
		print('Say something!')
		audio = r.listen(source,5)
	print("Okey")
	text = ''
	#fs, data = wavfile.read('pruebasonido.wav')
	try:
		
		text = r.recognize_google(audio)
	except sr.UnknownValueError :
		print("Error 1")
		speak('I dont understand you')
	except sr.RequestError as e:
		print ("Error 2")
		speak("Could not request results from Google Speech Recognition service")
		
	print('->' + str(text))
	return text

def speak(text):
	tts = gTTS(text)
	filename = '/tmp/temp.mp3'
	tts.save(filename)
	#print('HABLA JO PUTA')
	music = pyglet.media.load(filename)
	music.play()

	time.sleep(music.duration)
	os.remove(filename)

def state_callback(data):
	global goals, state,finish
	rospy.loginfo("ARNL path state: " + data.data)
	if data.data == 'REACHED_GOAL':
		speak("I am at the goal")
	


def understand(text):
	global audio,door,circle,black_board, finish
	if 'go to' in text:
		if  len([elem for elem in door if elem in text]) != 0:
			pub.publish('door')
			print('voy a la puerta')
		elif len([elem for elem in black_board if elem in text]) != 0:
			pub.publish('black_board')
			print('voy a la pizarra')
		elif len([elem for elem in circle if elem in text]) != 0:
			pub.publish('circle')
			print('voy a al centro')

	elif 'hello' in text:
		speak('hello')
		print('ey')
	elif 'finish' in text:
		print('Voy a terminar porque sois un poco pesaos')
		finish = True


def main():
	global goals, finish

	rospy.init_node('rosarnl_tourgoals_node', anonymous=True)

	rospy.sleep(1)
	print("sale sleep")
	#Subscribe to the robot planner state
	rospy.Subscriber('rosarnl_node/arnl_path_state', String, state_callback)
	while True:

		text = escucha_micro()
		understand(text)
		if finish == True:
			#rospy.ServiceProxy("/rosarnl_node/stop",Stop)
			rospy.signal_shutdown('Quit')	


	#Return control to ROS
	rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
