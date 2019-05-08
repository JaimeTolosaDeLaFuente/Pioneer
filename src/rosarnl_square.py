#!/usr/bin/env python
import rospy
import sys
import csv
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped, Pose2D
from tf.transformations import euler_from_quaternion

N_GOALS = 4
N_SQUARES = 20

# TODO: Add the goals
goals = ['Goal1', 'Goal2', 'Goal3','Goal0']

current_goal = 0    # Index of the current goal in the goals array
n_squares = 0       # Number of completed square

outfile = "poses"        # Output filename

poses = []              # Variable to store the poses at the end of the movements
current_x = 0           # Current x based on the published pose
current_y = 0           # Current y based on the published pose
current_theta = 0       # Current theta based on the published pose


# TODO: Create the publisher to publish the topic with the next goal
pub = rospy.Publisher('/rosarnl_node/goalname', String, queue_size=10)


def save_current_pose():
	'''
		Store the current pose of the robot in the poses vector.
	'''

	# TODO: Store the current pose of the robot in the poses vector
	global poses
	pos = Pose2D()
	pos.x = current_x
	pos.y = current_y
	pos.theta = current_theta
	poses.append(pos)


def write_poses_to_file(filename):
	'''
		Save the stored poses to a csv file.
		
		Argse:
			filename: file name of output file.
	'''
	with open(filename+".csv", 'w') as f:
		pose_writer = csv.writer(
			f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		pose_writer.writerow(['x', 'y', 'yaw'])
		for pos in poses:
			pose_writer.writerow([pos.x, pos.y, pos.theta])


def state_callback(data):
	global current_goal,goals,pub,n_squares
	rospy.loginfo("ARNL path state: " + data.data)
	print(data.data)
	#print('hola he entrado')
	# TODO: If the state is "REACHED_GOAL":
	if data.data == "REACHED_GOAL":
	#   - Save the current pose
		save_current_pose()
	#   - Update the current goal	
		current_goal = (current_goal+1)%4
	#   - Chech if we finished:
		if current_goal == 0:
			n_squares = n_squares+1
		
		#       - If we have reached the last goal, we have completed a square (update the number of completed squares)
			if n_squares == 20:	
			#       - If we have completed 20 squares, we have finished. Use 'writePosesToFile(outfile)' to write the output and 'ros::shutdown()' to finish.
				write_poses_to_file(outfile)
				rospy.signal_shutdown('Se termino la ejecucion')
		#   - Send the robot to the next goal (publish the appropriate message)
		pub.publish(goals[current_goal])

def pose_callback(data):
	
	# TODO: Assign the published pose to the global variables
	current_x = data.pose.pose.position.x
	current_y = data.pose.pose.position.y
	_, _, current_theta = euler_from_quaternion([data.pose.pose.orientation.x, data.pose.pose.orientation.y, data.pose.pose.orientation.y, data.pose.pose.orientation.z, data.pose.pose.orientation.w]) # It is in radians and the quaternion has to be a list type


def main():
	global pub,goals,outfile
	# Check for filename param
	if len(sys.argv) != 2:
		rospy.loginfo(
			"Wrong number of parameters. Please, use: rosrun ar_lab4_solution rosaria_square.py <file>")
		sys.exit(0)
	rospy.loginfo("Output file: " + sys.argv[1])

	# TODO: Init node
	rospy.init_node('rosarnl_square_node', anonymous=True)

	# TODO: Subscribe to the robot planner state
	rospy.Subscriber('rosarnl_node/arnl_path_state', String,state_callback)

	# TODO: Subscribe to the robot localized position
	rospy.Subscriber('/rosarnl_node/amcl_pose', PoseWithCovarianceStamped, pose_callback)
 
	# TODO: Send the robot to the first goal
	rospy.sleep(3)
	print(goals[0])
	pub.publish(goals[0])

	# Return control to ROS
	rospy.spin()


if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
