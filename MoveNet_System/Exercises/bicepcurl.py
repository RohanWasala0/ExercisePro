import numpy as np

"""
 keypoints 
 (in the order of: [0nose, 1left eye, 2right eye, 3left ear, 4right ear, 
                    5left shoulder, 6right shoulder, 7left elbow, 8right elbow, 
                    9left wrist, 10right wrist, 11left hip, 12right hip, 13left knee, 
                    14right knee, 15left ankle, 16right ankle])
 1 rep = 1 left + 1 right bicepcurl
"""
from MoveNet_System.utilities import trainer

class bicepcurl():
    def __init__(self, keypoints, exinfo):
        self.keypoints = keypoints[0,0,:,:].numpy()
        self.exinfo = exinfo
        pass

    def calculate(self, frame_size):
        #print(self.keypoints)
        try:
            hip_visibility = [np.mean(self.keypoints[:11,2]), np.mean(self.keypoints[:12,2])]
            eye_visibility = self.keypoints[1, 2]
            if eye_visibility >=0.3 and hip_visibility[0] >= 0.6 and hip_visibility[1] >= 0.6:
                shoulder = [(self.keypoints[5, 1], self.keypoints[5, 0]),(self.keypoints[6, 1], self.keypoints[6, 0])]
                elbow = [(self.keypoints[7, 1], self.keypoints[7, 0]),(self.keypoints[8, 1], self.keypoints[8, 0])]
                wrist = [(self.keypoints[9, 1], self.keypoints[9, 0]),(self.keypoints[10, 1], self.keypoints[10, 0])]

                leftangles = trainer.findAngle(shoulder[0], elbow[0], wrist[0])
                self.exinfo['internal_info'][0] = self.exinfo['internal_info'][0][1:] + [elbow[0][1] * frame_size[0]]
                self.exinfo['angles'][0] = leftangles
                if max(self.exinfo['internal_info'][0]) - min(self.exinfo['internal_info'][0]):
                    if leftangles > 150:
                        self.exinfo['internal_info'][2][0] = 1
                    elif leftangles < 30 and self.exinfo['internal_info'][2][0] == 1:
                        self.exinfo['internal_info'][2][0] = 0
                        self.exinfo['count'][0] += 1

                rightangles = trainer.findAngle(shoulder[1], elbow[1], wrist[1])
                self.exinfo['internal_info'][1] = self.exinfo['internal_info'][1][1:] + [elbow[1][1] * frame_size[0]]
                self.exinfo['angles'][1] = rightangles
                if max(self.exinfo['internal_info'][1]) - min(self.exinfo['internal_info'][1]):
                    if rightangles > 150:
                        self.exinfo['internal_info'][2][1] = 1
                    elif rightangles < 30 and self.exinfo['internal_info'][2][1] == 1:
                        self.exinfo['internal_info'][2][1] = 0
                        self.exinfo['count'][1] += 1
                
                self.exinfo['notification'] = "perfect"
            else:
                self.exinfo['notification'] = "please stand back"
        except Exception as e:
            print("fail",e)
            pass
        pass
    def give_data(self):
        return self.exinfo


