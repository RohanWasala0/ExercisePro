import cv2
import numpy as np
import tensorflow as tf

class Master():
    def __init__(self, frame, movenet):
        self.Frame = frame
        self.model = movenet
        pass
    
    def load_keypoints(self):
        tf_img = cv2.resize(self.Frame, (256,256))
        tf_img = cv2.cvtColor(tf_img, cv2.COLOR_BGR2RGB)
        tf_img = np.asarray(tf_img)
        tf_img = np.expand_dims(tf_img, axis=0)

        input_movenet = tf.cast(tf_img, dtype=tf.int32)

        output = self.model(input_movenet)
        self.keypoints = output['output_0']