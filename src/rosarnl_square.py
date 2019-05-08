#!/usr/bin/env python
import rospy
import sys
from std_msgs.msg import String

# TODO: Add goals id
goals = ["Goal1", "Goal2","Goal3"]


# TODO: Create the publisher to publish the topic with the next goal
pub = rospy.Publisher('/rosarnl_node/goalname', String, queue_size=10)


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
	# Initialise node gain_controller
	rospy.init_node('rosarnl_tourgoals_node', anonymous=True)

	rospy.sleep(2) # Seelp for 2 sec

	# TODO: Subscribe to the robot planner state
	rospy.Subscriber('rosarnl_node/arnl_path_state', String, state_callback)

	# TODO: Send the robot to the first goal
	pub.publish(goals.pop(0))

	# Return control to ROS
	rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)