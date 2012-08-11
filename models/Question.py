import datetime
from models.BaseModel import BaseModel

class Question(BaseModel):    
    def __init__(self, DBCON, _id=None):
        self.fields = [
            ('text', None),
            ('complete', False),
            ('added', datetime.datetime.now()),
            ('userId', None),
        ]
        self.init(DBCON, _id)