from godot import exposed, Control, PoolByteArray, ResourceLoader

import Manager
import copy

exercises = ['bicepcurl', 'bicepcurl']
reps = [2, 6]

@exposed
class user_display(Control):
    guidebar_flag = True
    manage_obj = Manager.Manager(0)
    def _ready(self):
        self.display = self.get_node("landmarked_display")
        self.guidebar_container = self.get_node("guid_bar_container")
        self.notification_label = self.get_node("notification_label")
        self.exercise_container = self.get_node("exercise_container")

        self.selected_flag = True
        self.change_flag = True
        self.guidebar_flag = True
        self.display.shouldRun = True

        temp_card = ResourceLoader.load("res://UI_Elements/exercise_card.tscn").instance()
        temp_card.set_name("temp_card")
        self.exercise_container.add_child(temp_card)
        pass
    
    def _process(self, delta):
        #print("user",Manager.all_exercises)
        selected_exercises = copy.deepcopy(exercises)
        temp = len(selected_exercises)
        selected_reps = copy.deepcopy(reps)
        if self.selected_flag:
            self.manage_obj.SelectSet(selected_exercises, selected_reps)
            self.selected_flag = False
        
        self.manage_obj.LoopforData()
        if self.display.shouldRun:
            self.display.data = PoolByteArray(self.manage_obj.LoopforFrameDisplay())

        if self.change_flag:
            print("changed exercise")
            self.manage_obj.ChangeExercise()
            self.remove_card(self.exercise_container)
        self.change_flag = self.manage_obj.ChangeCheck() 

        self.manage_obj.LoopforExercises()
        display_info = self.manage_obj.LoopforDisplay()
        
        if self.guidebar_flag:
            self.add_guidebars(display_info[0])
            self.add_exercisecard(temp, reps, display_info[5])
            self.guidebar_flag = False
        self.update_guid_bars(self.guidebar_container.get_children(), display_info[1])
        self.notify(display_info[2])
        self.update_exercise_card(self.exercise_container.get_children(), display_info[3], display_info[4], display_info[6])
        pass

    def add_guidebars(self, noof_guidebars):
        for i in range(noof_guidebars):
            print("adding guid_bar")
            guid_bar = ResourceLoader.load("res://UI_Elements/guid_bar.tscn").instance()
            guid_bar.set_name("guid_bar"+str(i))
            self.guidebar_container.add_child(guid_bar)
        pass
    
    def update_guid_bars(self, guid_bars, guidebar_precentage):
        for x in range(len(guid_bars)):
            guid_bars[x].value = guidebar_precentage[x]
        pass

    def notify(self, notification_text):
        self.notification_label.text = notification_text
        pass

    def add_exercisecard(self, noof_exercises, rep_, time):
        for i in range(noof_exercises):
            print("adding cards")
            exercise_card = ResourceLoader.load("res://UI_Elements/exercise_card.tscn").instance()
            exercise_card.set_name("exercise_card"+str(i))
            time_rep = exercise_card.get_node("Time_VBoxContainer").get_node("Data_Label")
            print(rep_, i)
            time_rep.text = str(rep_[i] * time)+":00"
            self.exercise_container.add_child(exercise_card)
        pass
    
    def update_exercise_card(self, exercise_cards, current_exercise, count_array, card_progress):
        count = exercise_cards[0].get_node("Count_VBoxContainer").get_node("Data_Label")
        count.text = count_array
        progress = exercise_cards[0].get_node("TextureProgress")
        progress.value = 100 - ((sum(card_progress)/200) * 100) 
        for y in range(len(exercise_cards)):
            label = exercise_cards[y].get_node("exercise_label")
            label.text = current_exercise
            
        pass

    def remove_card(self, container):
        children = container.get_children()
        container.remove_child(children[0])
        pass