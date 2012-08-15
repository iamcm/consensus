import datetime
from models.BaseModel import BaseModel

class Response(BaseModel):    
    def __init__(self, DBCON, _id=None):
        self.fields = [
            ('option', None),
            ('added', datetime.datetime.now()),
            ('userId', None),
        ]
        self.init(DBCON, _id)