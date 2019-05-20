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

# Add goals id
goals = ["Goal1", "Goal2","Goal3"]
r = None

# Create the publisher to publish the topic with the next goal
pub = rospy.Publisher('/rosarnl_node/goalname', String, queue_size=10)

def inicia_micro():
	global r
	r = sr.Recognizer()
	with sr.Microphone() as source:
			print("Say something!")
			audio = r.listen(source,3)
	print("Okey")
	return audio

def escucha_micro(data):
	global r
	text = ''
	r = sr.Recognizer()
	#fs, data = wavfile.read('pruebasonido.wav')
	try:

			text = r.recognize_google(data)
	except sr.UnknownValueError:
		print("Error 1")
		speak('I dont understand you')
		inicia_micro()
	except sr.RequestError as e:
		print ("Error 2")
		speak("Could not request results from Google Speech Recognition service")
		
	print('->' + str(text))
	return text
def speak(text):
	tts = gTTS(text)
	filename = '/tmp/temp.mp3'
	tts.save(filename)
	print('HABLA JO PUTA')
	music = pyglet.media.load(filename)
	music.play()
	pygame.music.Sound(filaname).play()

	time.sleep(music.duration)
	os.remove(filename)

def state_callback(data):
	global goals
	rospy.loginfo("ARNL path state: " + data.data)
  
	if data.data == 'REACHED_GOAL':
		speak("I am at the goal")

def understand(text):
	if 'go to' in text:
		if 'door' in text:
			pub.publish('door')
			print('voy a la puerta')
		elif 'black board' in text:
			pub.publish('black_board')
			print('voy a la pizarra')
		elif 'circle' in text:
			pub.publish('circle')
			print('voy a al centro')
	elif 'hello' in text:
		speak('hello')
		print('ey')



def main():
	global goals

	audio = inicia_micro()
	rospy.init_node('rosarnl_tourgoals_node', anonymous=True)

	rospy.sleep(1)
	print("sale sleep")
	#Subscribe to the robot planner state
	rospy.Subscriber('rosarnl_node/arnl_path_state', String, state_callback)

	text = escucha_micro(audio)

	understand(text)

	
	#Return control to ROS
	rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
