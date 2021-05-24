from typing import List


class ShowOKRDetails:
    def __init__(
        self,
        okr_type: str = None ,
        okr_usr_rply: str = None     
    ):
        self.okr_type = okr_type
        self.okr_usr_rply = okr_usr_rply


    def get_okr_type(self):

        key = self.okr_type        
        okr_key = 'personal'
        if key is not None:
            if key in ['my','I','mine','me','personal','own']:
                okr_key = 'personal'
            elif key in ['team','teams','associates']:
                okr_key = 'team'        
        else :
            okr_key = 'personal'

        print('okr_key => ', okr_key)

        return okr_key

class UpdateOKRDetails:
    def __init__(
        self,
        okr_type: str = None ,
        is_okr_updated : str = 'No',
        okr_update_reply: str = None     
    ):
        self.okr_type = okr_type
        self.okr_update_reply = okr_update_reply
        self.is_okr_updated = is_okr_updated

    def get_okr_type(self):

        key = self.okr_type        
        okr_key = 'personal'
        if key is not None:
            if key in ['my','I','mine','me','personal','own']:
                okr_key = 'personal'
            elif key in ['team','teams','associates']:
                okr_key = 'team'        
        else :
            okr_key = 'personal'

        print('okr_key => ', okr_key)

        return okr_key
        