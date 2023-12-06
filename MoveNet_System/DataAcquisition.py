import cv2
import numpy as np
import tensorflow as tf
class DataAcquisition():
    def __init__(self, capture, movenet) -> None:
        self.capture = capture
        self.movenet = movenet

        pass

    def StoreFrame(self):
        ret, frame = self.capture.read()

        if not ret:
            quit()

        self.Frame = frame
        pass

    def FrameAnalyze(self):
        tf_image = cv2.resize(self.Frame, (256, 256))
        tf_image = cv2.cvtColor(tf_image, cv2.COLOR_BGR2RGB)
        tf_image = np.asarray(tf_image)
        tf_image = np.expand_dims(tf_image, axis=0)

        input_movenet = tf.cast(tf_image, dtype=tf.int32)

        output = self.movenet(input_movenet)
        keypoint = output['output_0']
        self.Keypoint = keypoint
        pass
    
    def CurrentExercise(self, _set):
        current_exercise = _set['name of exercise'].pop(0)
        reps = _set['reps'].pop(0)
        #_set.update({'name of exercise': _set['name of exercise'], 'reps': _set['reps']})
        return {
            'Set': _set,
            'Current_exercise': current_exercise,
            'Reps': reps,
        }

    def Data(self):
        Data = {
            'Frame' : self.Frame,
            'Keypoint': self.Keypoint,
        }
        return Data
