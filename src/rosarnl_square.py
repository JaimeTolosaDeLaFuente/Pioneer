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
#faces
import pcl
import struct
import ctypes

from sensor_msgs.msg import PointCloud, PointCloud2, PointField
import sensor_msgs.point_cloud2 as pc2



# Add goals id
door=['door','work']
circle=['center','circle']
black_board = ['Blackboard','blackboard','white board']
#finish = False
rospy = None
face = False


# Create the publisher to publish the topic with the next goal
pub = rospy.Publisher('/rosarnl_node/goalname', String, queue_size=10)





def face_cloud_callback(data):
	global face
	#Comprobar formato
	print(str(data.to_list()))
	print(data.size)
	#Si detecta a alguien escucha
	if data.size > 0:
		face = True


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
	rospy.loginfo("ARNL path state: " + data.data)
	if data.data == 'REACHED_GOAL':
		speak("I am at the goal")
	


def understand(text):
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

	elif 'stop' in text:
		speak('I am going to stop')
		print('stop')
		rospy.ServiceProxy("/rosarnl_node/stop",Stop) #No funciona	
	elif 'finish' in text:
		print('Voy a terminar porque sois un poco pesaos') #No funciona
		rospy.signal_shutdown('Quit')


def main():
	global rospy

	rospy.init_node('rosarnl_tourgoals_node', anonymous=True)

	rospy.sleep(1)
	print("sale sleep")

	#Subscribe to the robot planner state
	rospy.Subscriber('rosarnl_node/arnl_path_state', String, state_callback)

    #Subscribe to the /face_detector/faces_cloud topic
    rospy.Subscriber('face_detector/faces_cloud', PointCloud, face_cloud_callback)



	while face:
		text = escucha_micro()
		understand(text)


	#Return control to ROS
	#rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
