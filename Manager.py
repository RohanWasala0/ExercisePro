"""
 keypoints 
 (in the order of: [0nose, 1left eye, 2right eye, 3left ear, 4right ear, 
                    5left shoulder, 6right shoulder, 7left elbow, 8right elbow, 
                    9left wrist, 10right wrist, 11left hip, 12right hip, 13left knee, 
                    14right knee, 15left ankle, 16right ankle])
"""
import cv2
import tensorflow_hub as hub
import copy

from MoveNet_System import DataAcquisition as da
from MoveNet_System import Display as dis
from MoveNet_System import ExerciseAnalyzer as ea

from MoveNet_System.Exercises import bicepcurl

model = hub.load("https://www.kaggle.com/models/google/movenet/frameworks/tensorFlow2/variations/singlepose-thunder/versions/3/saved_model.pd")
all_exercises = {
    'bicepcurl': {
        'execute': lambda a, b: bicepcurl.bicepcurl(a, b), 
        'information': {'angles': [0, 0], 'count': [0, 0], 'internal_info': [[1, 100, 200, 300, 400, 500], [1, 100, 200, 300, 400, 500],[0,0]], 'notification': ""},
        'noof_guidebar': 2,
        'card_info': 1
    }
}

class Manager():
    def __init__(self, selected_cam) -> None:
        self.DataStorage = {}
        self.DataStorage.update({'MoveNet' : model.signatures['serving_default'],})
        self.CameraManager(selected_cam)
        self.DataStorage.update({'Frame_size': (int(self.DataStorage['Capture'].get(3)), int(self.DataStorage['Capture'].get(4))),})

        self.OBJdata = da.DataAcquisition(self.DataStorage['Capture'], self.DataStorage['MoveNet'])
        self.OBJexercise = ea.ExerciseAnalyzer()
        self.OBJdisplay = dis.Display()

        pass

    def CameraManager(self, selected_cam):
        self.DataStorage.update({'Capture' : cv2.VideoCapture(selected_cam),})
        pass
    
    def SelectSet(self, exercises, reps):
        sets = {
            'name of exercise': exercises,
            'reps': reps
        }
        self.DataStorage.update({'Set': sets,})
        pass

    def LoopforData(self):
        self.OBJdata.StoreFrame()
        self.OBJdata.FrameAnalyze()
        self.DataStorage.update(self.OBJdata.Data())
        pass

    def LoopforFrameDisplay(self):
        return self.OBJdisplay.DisplayFrame(self.DataStorage['Frame'], self.DataStorage['Keypoint'])
    
    def ChangeExercise(self):
        if len(self.DataStorage['Set']['name of exercise']) != 0 and len(self.DataStorage['Set']['reps']) != 0:
            self.DataStorage.update(self.OBJdata.CurrentExercise(self.DataStorage['Set']))
            _information = copy.deepcopy(all_exercises[self.DataStorage['Current_exercise']]['information'])
            print(_information)
            self.DataStorage.update({'Information': _information, })
        pass

    def ChangeCheck(self):
        total_count = self.DataStorage['Information']['count'][0] + self.DataStorage['Information']['count'][1]
        total_reps = self.DataStorage['Reps'] * 2
        change_flag = total_count == total_reps
        return change_flag
    
    def LoopforExercises(self):
        _execute = copy.deepcopy(all_exercises[self.DataStorage['Current_exercise']]['execute'])
        self.OBJexercise.ExerciseCalculate(
            _execute, 
            self.DataStorage['Keypoint'], 
            self.DataStorage['Information'],
            self.DataStorage['Frame_size'])
        self.OBJexercise.CategorizInformation(self.DataStorage['Reps'])
        self.DataStorage.update(self.OBJexercise.Data())
        pass
        
    def LoopforDisplay(self):
        _noof_guidebar = copy.deepcopy(all_exercises[self.DataStorage['Current_exercise']])
        temp_list = [self.DataStorage['Reps'] -  self.DataStorage['Information']['count'][i] for i in range(len(self.DataStorage['Information']['count']))]
        Data = [
            _noof_guidebar['noof_guidebar'],
            self.DataStorage['Display information']['guide_progress'],
            self.DataStorage['Display information']['notification_text'],
            self.DataStorage['Current_exercise'],
            ':'.join(str(num) for num in temp_list),
            _noof_guidebar['card_info'],
            self.DataStorage['Display information']['card_progress']
        ]
        return Data
    


#from pygrabber.dshow_graph import FilterGraph


# from MediaPipe_System.Exercises import bicepcurl as p_bicepcurl
# from MoveNet_System.Exercises import bicepcurl as n_bicepcurl

# # model = hub.load('https://tfhub.dev/google/movenet/singlepose/thunder/4')
# # movenet = model.signatures['serving_default']

# mACTIVITIES = {
#     "bicepcurl": {
#         "execute": lambda a, b: n_bicepcurl.bicepcurl(a, b), 
#         "information": {'angles': [0, 0], 'count': [0, 0], 'internal_info': [[1, 100, 200, 300, 400, 500], [1, 100, 200, 300, 400, 500],[]], 'notification': "", },
#         "exercise_name": "BICEPCURLS",
#         "noof_guid_bar": 2},
# }

# def start_cam():
#     global cap
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print('error loading capture')
#         quit()

# def execute():
#     ret, frame = cap.read()
#     print(ret,'error loading capture')
#     if ret:
#         exercise = mACTIVITIES["bicepcurl"]["execute"](frame, movenet)
#         exercise.calculate()
#         image_data = make_points(frame, exercise.keypoints)
#     else:
#         cap.release()
#         print('error loading capture')
#         quit()
#     return image_data

# def make_points(frame, keypoints):
#     y, x, _ = frame.shape
#     for k in keypoints[0,0,:,:]:
#         k = k.numpy()
#         if k[2] > .3:
#             yc, xc = int(k[0] * y), int(k[1] * x)
#             output_frame = cv2.circle(frame, (xc, yc), 2, (0, 255, 0), 5)
#             _, buffer = cv2.imencode('.jpg', output_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
#     return buffer.tobytes()

