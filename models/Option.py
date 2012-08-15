import datetime
from models.BaseModel import BaseModel

class Option(BaseModel):    
    def __init__(self, DBCON, _id=None):
        self.fields = [
            ('text', None),
            ('added', datetime.datetime.now()),
        ]
        self.init(DBCON, _id)