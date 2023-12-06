import mediapipe as mp 
import numpy as np
import cv2

class _master():
    def __init__(self, Frame):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.Frame = Frame
        self.notification = "place holder"

        with self.mp_pose.Pose(
            static_image_mode=False,
			min_detection_confidence=0.5,
			min_tracking_confidence=0.5,
			model_complexity=1,
        )as pose:
            self.result = pose.process(Frame)

    def landmark_array(self):
        np_structure = [('id', int), ('value', '2float64'), ('visibility', float)]
        if self.result.pose_landmarks:
            landmarks_ = np.array([(id, (lm.x, lm.y), lm.visibility) for id, lm in enumerate(self.result.pose_landmarks.landmark)], dtype=np_structure)
        else:
            landmarks_ = np.array((0, (0, 0), 0), dtype=np_structure)
        return landmarks_

    def landmark_drew(self):
        self.mp_drawing.draw_landmarks(
            self.Frame, self.result.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
			self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
		    self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=3)
        )
        _, buffer = cv2.imencode('.jpg', self.Frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
        return buffer.tobytes()