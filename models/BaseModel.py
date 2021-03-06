from bson.objectid import ObjectId
import models 
from models.Logger import Logger

import datetime

class BaseModel(object):
    """
    This should be extended by any models wishing to persist data to mongo. It expects a
    distionary named 'fields' of 'mongo-field':'default-value' pairs.
    
    When extending this class, sub classes should call self.init(<args>) in their constructors, this
    is just a shorthand for to save having to remember the syntax of super(self.__class__, self).__init__(*args, **kwargs)
    
    Fields can hold a list of Classes eg:
    
    c1 = Competitor(_DBCON)
    c1.name = 'one'
    c2 = Competitor(_DBCON)
    c2.name = 'two'
    
    f = Fixture(_DBCON)
    f.competitors = [c1,c2]
    f.save()
    
    then can use as:
    
    for c in f.competitors:
        c.name
    
    e.g.
    - create a class
    
    class Todo(BaseModel):    
        def __init__(self, DBCON, _id=None):
            self.fields = [
                ('text', None),
                ('complete', False),
                ('added', datetime.datetime.now()),
                ('userId', None),
            ]
            self.init(DBCON, _id)
    
    - save an item
    
    t = Todo(_DBCON)
    t.text = todo
    t.userId = bottle.request.session.userid
    t.save()
    
    - get an item
    
    t = Todo(_DBCON, todoId)
    """
    def __init__(self, db, _id=None):
        self._mongocollection = 'self.db.%s' % self.__class__.__name__
        self._id = None
        self._fields = self.fields or []
        self.db = db

        for attribute, value in self._fields:
            setattr(self, attribute, value)
        
        if _id:
            self._get(_id)
    
    def _unicode_to_class(self, string):
        return str(string[string.find('model'):string.rfind("'")])
    
    def _get(self, _id):
        #Logger.log_to_file('%s.find_one({"_id":ObjectId("%s")})' % (self._mongocollection, str(_id)))
        entity = eval('%s.find_one({"_id":ObjectId("%s")})' % (self._mongocollection, str(_id)))
        
        if entity:
            setattr(self, '_id', entity.get('_id'))
            for f, val in self._fields:
                fieldtype = type(getattr(self, f))
                fieldvalue = entity.get(f)
                
                if fieldtype == list:
                    Logger().log_to_file("1")
                    fieldlist = []
                    for el in fieldvalue:
                        Logger().log_to_file("2")
                        if type(el)==dict and el.has_key('__instanceOf__'):
                            el = eval('%s(self.db, ObjectId("%s"))' %
                                      (self._unicode_to_class(el['__instanceOf__']), el['_id']))
                        
                        fieldlist.append(el)
                    fieldvalue = fieldlist
                elif type(fieldvalue)==dict and fieldvalue.has_key('__instanceOf__'):     
                    Logger().log_to_file("3")    
                    fieldvalue = eval('%s(self.db, ObjectId("%s"))' %
                                      (self._unicode_to_class(fieldvalue['__instanceOf__'])
                                      , fieldvalue['_id']))
                    
                setattr(self, f, fieldvalue)
    
    def _get_hash(self, saveClasses=True):
        obj = {}
        for f, val in self._fields:
            fieldtype = type(getattr(self, f))
            fieldvalue = getattr(self, f)
            
            if fieldtype == list:
                fieldlist = []
                for el in fieldvalue:
                    if hasattr(el, '_get_hash'):
                        if(saveClasses): el.save()
                        el = el._get_hash()
                    
                    fieldlist.append(el)
                fieldvalue = fieldlist
            elif hasattr(fieldvalue, '_get_hash'):
                if(saveClasses): fieldvalue.save()
                fieldvalue = fieldvalue._get_hash()            
                  
            obj[f] = fieldvalue
            
        if self._id: obj['_id'] = self._id
        
        # add __class__ as metadata with the name of __instanceOf__ so we can grab it when
        # hydrating a model
        obj['__instanceOf__'] = str(self.__class__)
        
        return obj
            
    def save(self):
        if self._id:
            eval('%s.save(%s)' % (self._mongocollection, str(self._get_hash())))
        else:
            self._id = eval('%s.insert(%s)' % (self._mongocollection, str(self._get_hash())))
    
    def init(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
    

        
    