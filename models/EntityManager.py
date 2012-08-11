from bson.objectid import ObjectId
import datetime
from models.Logger import Logger

class EntityManager:
    """
    This class handles getting a list of entities, or removing one/many entities
    from a mongo collection
    """
    def __init__(self, db):
        self.db = db
        
    def getAll(self, entity, filterCriteria='', sortBy=[]):
        """
        Get all or a selection of entities from the datastore. This returns
        a list of entities.
        
        Entity should be class object
        
        filterCriteria can be used to filter the results and should be
        a dictionary that adheres to the pymongo documentation
        http://api.mongodb.org/python/current/genindex.html
        {'name':'jim'}
        
        sortBy should be a list of tuples (attribute, direction)
        [
            ('name',1),
            ('age',1),
        ]
        
        e.g.
        todos = EntityManager(_DBCON).getAll(Todo, filterCriteria={'userId':bottle.request.session.userid}, sortBy=[('added', 1)])
        """
        if len(sortBy)>0:
            strSortBy = '.sort(%s)' % str(sortBy)
        else:
            strSortBy = ''
            
        entities = []
        for result in eval('self.db.%s.find(%s)%s' % (entity.__name__, str(filterCriteria), strSortBy)):
            e = entity(self.db)
            setattr(e, '_id', result.get('_id'))
            for f, val in e.fields:
                setattr(e, f, result.get(f))
            entities.append(e)
        
        return entities
        
    def deleteOne(self, entity, _id):
        """
        Deletes a single entity from the datastore based on the id given
        
        entity should be a string
        _id should be the entity id
        
        e.g.
        EntityManager(_DBCON).deleteOne('Todo', todoId)
        """
        return eval('self.db.%s.remove({"_id":ObjectId("%s")})' % (entity, str(_id)))
        