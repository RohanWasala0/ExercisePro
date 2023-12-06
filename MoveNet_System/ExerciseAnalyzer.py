class ExerciseAnalyzer():
    def __init__(self) -> None:
        pass

    def ExerciseCalculate(self, execute, keypoint, information, frame_size):
        obj_exercise = execute(keypoint, information)
        obj_exercise.calculate(frame_size)
        self.temp_info = obj_exercise.give_data()
        #print(self.info['notification'])
        pass
    def CategorizInformation(self, reps):
        #angles for the guidebar/ count for exercise_card/ 
        self.angles = [100 - round((angle / 170) * 100) for angle in self.temp_info['angles']]
        self.card_count = [100 - round((count / reps)* 100) for count in self.temp_info['count']]
        pass
    def Data(self):
        Data = {
            'Information': self.temp_info,
            'Display information': {
                'guide_progress': self.angles, 
                'card_progress': self.card_count,
                'notification_text': self.temp_info['notification']},

        }
        return Data