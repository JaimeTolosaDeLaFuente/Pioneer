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


activate = True

# Create the publisher to publish the topic with the next goal
pub_speach_recognition = rospy.Publisher('speak_node/activate_speach_recognition', Bool, queue_size=10)
pub_system_stat = rospy.Publisher('speak_node/speak_stat', Bool, queue_size=10)

def activate_timer():
    global activate
    activate = True


def face_callback(data):
    global activate
    #Cuando llega una cara te dice que hables y pasa a escuchar
    if activate = True:
        if data == True:
            activate = False
            pub_system_stat.publish(False)   #Desactiva envio de datos de detection
            timer = Timer(2, activate_timer)  #En dos segundo se reactia "activate"
            print("Speak: Te escucho")
            speak("Te escucho")
            pub_speach_recognition.publish(True)


def say_comprension_callback():
    #Cuando no entiende lo que has dicho
    print("Speak: No te he entendido, repite")
    speak("No te he entendido, repite")
    pub_speach_recognition.publish(True)

def say_navigation_callback(text):
    speak(text)

def speak(text):
	tts = gTTS(text)
	filename = '/tmp/temp.mp3'
	tts.save(filename)
	#print('HABLA JO PUTA')
	music = pyglet.media.load(filename)
	music.play()

	time.sleep(music.duration)
	os.remove(filename)


def main():
	global rospy

	rospy.init_node('speak_node', anonymous=True)

	rospy.sleep(1)
	print("sale sleep")

	rospy.Subscriber('system_status_node/face', Bool, face_callback)
    rospy.Subscriber('navigation_node/say_navigation', String, say_navigation_callback)
    rospy.Subscriber('system_status_node/say_comprension', Bool, say_comprension_callback)
    rospy.Subscriber('speach_recognition_node/speach_recognition_error', Bool, say_comprension_callback)

	rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
