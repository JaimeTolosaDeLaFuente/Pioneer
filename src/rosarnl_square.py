#!/usr/bin/env python
import rospy
import sys
from std_msgs.msg import String
import speech_recognition as sr
from gtts import gTTS
import pyglet
import os 

# TODO: Add goals id
goals = ["Goal1", "Goal2","Goal3"]


# TODO: Create the publisher to publish the topic with the next goal
pub = rospy.Publisher('/rosarnl_node/goalname', String, queue_size=10)

def inicia_micro():
	r = sr.Recognizer()
	with sr.Microphone() as source:
    	print("Say something!")
    	audio = r.listen(source)

def escucha_micro():
	audio = ''
	while audio == '':
		try:
	    # for testing purposes, we're just using the default API key
	    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
	    # instead of `r.recognize_google(audio)`
	    	audio = r.recognize_google(audio)
		except sr.UnknownValueError:
	    	speak('I dont understand you ')
		except sr.RequestError as e:
	    	print("Could not request results from Google Speech Recognition service; {0}".format(e))
	return audio
def speak(text):
	tts = gTTS(text)
	filename = '/tmp/temp.mp3'
	tts.save(filename)

	music = pyglet.media.load(filename,streaming = False)
	music.play()

	sleep(music.duration)
	os.remove(filename)

def state_callback(data):
	global goals
	rospy.loginfo("ARNL path state: " + data.data)
  
	if data.data == 'REACHED_GOAL':
		if goals:           #There are more goals
			pub.publish(goals.pop(0))
		else:               #Empty goal
			rospy.loginfo('Final goal reached.')
			rospy.signal_shutdown('Final goal reached.')


def main():
	global goals

	inicia_micro()
	# Initialise node gain_controller
	rospy.init_node('rosarnl_tourgoals_node', anonymous=True)

	rospy.sleep(2) # Seelp for 2 sec

	# TODO: Subscribe to the robot planner state
	rospy.Subscriber('rosarnl_node/arnl_path_state', String, state_callback)

	text = escucha_micro()
	# TODO: Send the robot to the first goal
	pub.publish(text)

	# Return control to ROS
	rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)