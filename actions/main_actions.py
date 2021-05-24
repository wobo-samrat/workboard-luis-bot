import json
import random 
import os


with open(os.getcwd() + '/actions/main-action-mapper.json') as f:
  main_data = json.load(f)

class MainAction():
    def __init__(self):
        self.main_data = main_data

    def get_random_utterance(self,key):        
        utter_lst = main_data['utterance'][key]
        n = random.randint(0,len(utter_lst)-1)
        utter_sent = utter_lst[n]
        
        return utter_sent


 