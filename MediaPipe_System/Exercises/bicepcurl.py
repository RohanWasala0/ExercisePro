import numpy as np

from MediaPipe_System.exercise_master import _master
from MediaPipe_System.utilities.trainer import findAngle

class bicepcurl(_master):
    def __init__(self, frame):
        super().__init__(frame)
        self.landmarks = self.landmark_array()
        self.notifications = "Loading"

    def calculate_exercise(self, information):
        self.angles = [1, 1]
        self.count = information[3]
        try:
            arm_visibility = [
                np.mean(self.landmarks['visibility'][:self.mp_pose.PoseLandmark.LEFT_HIP.value+1]),
                np.mean(self.landmarks['visibility'][:self.mp_pose.PoseLandmark.RIGHT_HIP.value+1])
            ]

            eye = self.landmarks[self.mp_pose.PoseLandmark.LEFT_EYE.value]['visibility'] if self.landmarks[self.mp_pose.PoseLandmark.LEFT_EYE.value] is not [] else []

            if  eye >= 0.8  and arm_visibility[0] >= 0.8 and arm_visibility[1] >= 0.8:
                shoulder = [
                    self.landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]['value'], 
                    self.landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]['value']
                ]
                elbow = [
                    self.landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value]['value'],
                    self.landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value]['value']
                ]
                wrist = [
                    self.landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value]['value'], 
                    self.landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]['value']
                ]
                for a in range(2):
                    left_angle = findAngle(shoulder[a], elbow[a], wrist[a])
                    information[a] = information[a][1:] + [elbow[a][1] * self.Frame.shape[1]]
                    self.angles[a] = left_angle
                    #print(left_angle, information[2])
                    if max(information[a]) - min(information[a]) < 20:
                        if left_angle > 150:
                            information[2][a] = 1
                        elif left_angle < 30 and information[2][a] == 1:
                            information[2][a] = 0
                            self.count[a] += 1

                self.notifications = "Perfect"
            else:
                self.notifications = "Please stand further back"
        except:
            pass
        return information

    def give_information(self):
        _result_data = {}
        _result_data["angles"] = self.angles
        _result_data["notifications"] = self.notifications
        _result_data["count"] = self.count
        return _result_data