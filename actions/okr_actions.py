import json
import random 
import os

with open(os.getcwd() + '/actions/okr-action-mapper.json') as f:
  okr_data = json.load(f)


class ShowOKRAction():
    def __init__(self):
        self.okr_data = okr_data

    def get_random_utterance(self,key):
            
        utter_lst = okr_data['utterance'][key]
        n = random.randint(0,len(utter_lst)-1)
        utter_sent = utter_lst[n]
        
        return utter_sent


class UpdateOKRAction():
    def __init__(self):
        self.okr_data = okr_data

    def get_random_utterance(self,key):
        
        utter_lst = okr_data['utterance'][key]
        n = random.randint(0,len(utter_lst)-1)
        utter_sent = utter_lst[n]
        
        return utter_sent

    def get_okr_update_status(self,usr):
        #here call the external API
        
        if usr :
          return self.get_random_utterance('msg_update_true')
        else:
          return self.get_random_utterance('msg_update_false')

    

      


        
                
    
    

    
    
    
    
    



       
       
      
         
        