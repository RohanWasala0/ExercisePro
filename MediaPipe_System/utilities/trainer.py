import numpy as np
import cv2
import mediapipe as mp


def findAngle(p1, p2, p3, limit=True):
	p1 = np.array(p1)
	p2 = np.array(p2)
	p3 = np.array(p3)

	x1, y1 = p1[0], p1[1]
	x2, y2 = p2[0], p2[1]
	x3, y3 = p3[0], p3[1]

	angle_in_radians = np.arctan2(y3 - y2, x3 - x2) - np.arctan2(y1 - y2, x1 - x2)
	angle_in_degrees = np.abs(angle_in_radians * 180.0/np.pi)

	if angle_in_degrees > 180.0 and limit:
		angle_in_degrees = 360.0 - angle_in_degrees

	return int(angle_in_degrees)


def findDistance(p1, p2):
	p1 = np.array(p1)
	p2 = np.array(p2)

	x1, y1 = p1[0], p1[1]
	x2, y2 = p2[0], p2[1]

	return ((x1 - x2) ** 2) + ((y1 - y2) ** 2)


def makeBar(image, variable, lower_lim, upper_lim, pos_x, pos_y, first_bound=20, second_bound=60, upper_bound_bar=200):
	"""
	Makes a dynamic bar on an image based on a variable and its limits.
	:param image: Image on which bar is to be made
	:param variable: Variable which influences the height of the bar
	:param lower_lim: Lower interpolation limit for variable
	:param upper_lim: Upper interpolation limit for variable
	:param pos_x: X position of the bar
	:param pos_y: Y position of the bar
	:param first_bound: First % bound for the bar
	:param second_bound: Second % bound for the bar
	:param upper_bound_bar: highest point for the bar
	:return: nothing
	"""
	percentage = np.interp(variable, (lower_lim, upper_lim), (0, 100))

	bar = np.interp(variable, (lower_lim, upper_lim), (upper_bound_bar, pos_y))

	if int(percentage) < first_bound:
		cv2.line(image, (pos_x, int(bar)), (pos_x, pos_y),
				 (0, 255, 0), 30)
		cv2.circle(image, (pos_x, int(bar)), 35, (0, 255, 0), -1)
		cv2.circle(image, (pos_x, int(bar)), 35, 0, 1)
	elif first_bound <= int(percentage) < second_bound:
		cv2.line(image, (pos_x, int(bar)), (pos_x, pos_y),
				 (0, 255, 255), 30)
		cv2.circle(image, (pos_x, int(bar)), 35, (0, 255, 255), -1)
		cv2.circle(image, (pos_x, int(bar)), 35, 0, 1)
	else:
		cv2.line(image, (pos_x, int(bar)), (pos_x, pos_y),
				 (255, 0, 0), 30)
		cv2.circle(image, (pos_x, int(bar)), 35, (255, 0, 0), -1)
		cv2.circle(image, (pos_x, int(bar)), 35, 0, 1)

	if int(percentage) == 0:
		cv2.putText(
			image, str(100 - int(percentage)), (pos_x - 30, int(bar) + 10),
			cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA
		)
	elif int(percentage) > 90:
		cv2.putText(
			image, str(100 - int(percentage)), (pos_x - 10, int(bar) + 10),
			cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA
		)
	else:
		cv2.putText(
			image, str(100 - int(percentage)), (pos_x - 20, int(bar) + 10),
			cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA
		)

def stopfunc(landmarks, counter):
	"""
	function to detect stop sign (an L made with arms). Checks for the arms being held in an L for some short duration.
	The counter taken as input is updated and is used to keep track of when the "stop" signal should be given
	:param landmarks: landmarks after processing by mediapipe pose
	:param counter: counter for the duration for which arms must be held
	:return: boolean indicating stop and updated counter
	"""
	mp_pose = mp.solutions.pose
	left_shoulder = [
		landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
		landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
	]
	left_wrist = [
		landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
		landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y
	]
	right_shoulder = [
		landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
		landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
	]
	right_wrist = [
		landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
		landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y
	]
	isLleft = ((80 < findAngle(left_wrist, left_shoulder, right_wrist) < 100) and (left_wrist[1] < landmarks[0].y))
	isLright = ((80 < findAngle(right_wrist, right_shoulder, left_wrist) < 100) and (right_wrist[1] < landmarks[0].y))
	isStop = isLright or isLleft

	if isStop and counter < 30:
		return False, counter + 1
	elif isStop and counter == 30:
		return True, 0
	else:
		return False, 0
