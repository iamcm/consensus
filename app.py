###
import os, sys
_ROOTPATH = os.path.abspath('.')
sys.path.append(_ROOTPATH)
###
import json
import random
import bottle
import datetime
from bottle import route
import db
from db import _DBCON
from models.User import User
from models.Session import Session
from models.Email import Email
from models.Logger import Logger
from models.EntityManager import EntityManager
from models.Util import Util
from models.Question import Question
from models.Option import Option
from models.Response import Response
import settings


#######################################################
if settings.PROVIDE_STATIC_FILES:
    @route('/static/<filepath:path>')
    def server_static(filepath):
        return bottle.static_file(filepath, root=_ROOTPATH +'/static/')
        
    @route('/userfiles/<filepath:path>')
    def server_static(filepath):
        return bottle.static_file(filepath, root=_ROOTPATH +'/userfiles/') 
#######################################################

def checklogin(callback):
    def wrapper(*args, **kwargs):
        if bottle.request.get_cookie('token'):
            s = Session(_DBCON, publicid=bottle.request.get_cookie('token'))
            if not s.valid or not s.check(bottle.request.get('REMOTE_ADDR'), bottle.request.get('HTTP_USER_AGENT')):
                return bottle.redirect('/login')
            else:
                bottle.request.session = s
                return callback(*args, **kwargs)
        else:
            return bottle.redirect('/login')
    return wrapper
    


@route('/login', method='GET')
def index():
    vd = {
        #'date':datetime.datetime.now().strftime('%Y'),
        'baseurl':settings.BASEURL,
    }
    return bottle.template('login', vd=vd)
    
    
@route('/login', method='POST')
def index():
    vd = {
        #'date':datetime.datetime.now().strftime('%Y'),
        'baseurl':settings.BASEURL,
    }

    e = bottle.request.POST.get('email')
    p = bottle.request.POST.get('password')
        
    if e and p:
        u = User(_DBCON, email=e, password=p)
        
        if u._id:
            s = Session(_DBCON)
            s.userid = u._id
            s.ip = bottle.request.get('REMOTE_ADDR')
            s.useragent = bottle.request.get('HTTP_USER_AGENT')
            s.save()
            
            s.set_cookie()
            
            bottle.redirect('/')
        else:
            return bottle.template('login', error='Incorrect email/password combination', email=e, password=p, vd=vd)
    else:
        return bottle.template('login', error='Please complete the form', email=e or '', password=p or '', vd=vd)


@route('/logout', method='GET')
@checklogin
def index():
    s = bottle.request.session
    s.destroy()
    
    return bottle.redirect('/login')
    
    
@route('/register', method='GET')
def index():
    vd = {
        #'date':datetime.datetime.now().strftime('%Y'),
        'baseurl':settings.BASEURL,
    }
    return bottle.template('register', vd=vd)
    
    
@route('/register', method='POST')
def index():
    e = bottle.request.POST.get('email')
    p1 = bottle.request.POST.get('password1')
    p2 = bottle.request.POST.get('password2')
        
    if e and p1 and p2:
        if p1 != p2:
            return bottle.template('register', error='The passwords do not match', email=e, password1=p1, password2=p2)
        else:
            u = User(_DBCON, email=e, password=p1)
            if u._id:
                return bottle.template('register', error='An account already exists for that email address', email=e, password1=p1, password2=p2)
            else:
                u.save()
                e = Email(recipient=e)
                e.send('Places accounts activation', '<a href="%s/activate/%s">Activate</a>' % (settings.BASEURL, u.token))
                return bottle.redirect('/success')
                
                
    else:
        vd = {
            #'date':datetime.datetime.now().strftime('%Y'),
            'baseurl':settings.BASEURL,
        }
        return bottle.template('register', error='Please complete the form', email=e or '', password1=p1 or '', password2=p2 or '', vd=vd)
    
    
@route('/success', method='GET')
def index():
    vd = {
        #'date':datetime.datetime.now().strftime('%Y'),
        'baseurl':settings.BASEURL,
    }
    return bottle.template('register-success', vd=vd)


@route('/activate/<token>')
def index(token):
    u = User(_DBCON)
    if u.activate(token):
        s = Session(_DBCON)
        s.userid = u._id
        s.save()
        
        bottle.response.set_cookie('token', str(s.publicid), path='/')
        bottle.redirect('/')
    else:
        vd = {
            #'date':datetime.datetime.now().strftime('%Y'),
            'baseurl':settings.BASEURL,
        }
        return bottle.template('error', error='The token does not match any account that is pending activation', vd=vd)
    
    
    
    
 
    
    
    
@route('/fb/login')
def index():
    return bottle.redirect(FacebookClient().get_authentication_url())
    
@route('/fb/process')
def index():
    user = FacebookClient().process(bottle.request.GET['code'])
    
    if user:
        users = EntityManager(_DBCON).getAll(User, filterCriteria={'facebookUserId':user['id']})
        if users:
            _id = users[0]._id
        else:
            _id = None

        
        u = User(_DBCON, _id=_id)
        u.username = user['name']
        u.password = user['id']
        u.valid = False
        u.facebookUserId = user['id']
        u.save()
        
        s = Session(_DBCON)
        s.userid = u._id
        s.ip = bottle.request.get('REMOTE_ADDR')
        s.useragent = bottle.request.get('HTTP_USER_AGENT')
        s.save()
        
        s.set_cookie()
    
        bottle.redirect('/')
        
    else:
        bottle.redirect('/login')   
    

    
########################################################################






class Controller:
    """
    Base Controller to allow for sharing common data and tasks among views
    """
    def __init__(self):
        self.viewdata = {
            'date':datetime.datetime.now().strftime('%Y'),
            'baseurl':settings.BASEURL,
        }

    def _template(self, template):
        return bottle.template(template, vd=self.viewdata)

    
    def index(self):
        self.viewdata.update({
            'questions': EntityManager(_DBCON).getAll(Question, sortBy=[('added',1)]),    
        })
        return self._template('index')
        
    def question(self):
        q = Question(_DBCON, _id=bottle.request.GET.get('_id'))
        
        self.viewdata.update({'q':q})
        
        return self._template('question')
        
    def question_save(self):
        _id = bottle.request.POST.get('_id')
        t = bottle.request.POST.get('text')
        options = []

        for option in bottle.request.POST.getall('option'):
            o = Option(_DBCON)
            o.text = option
            o.save()
            options.append(o)

        if t and len(t.strip())>0:
            q = Question(_DBCON, _id)
            q.text = t
            q.options = options
            q.save()
        
            return bottle.redirect(settings.BASEURL +'/')
        else:
            self.viewdata.update({'error':'Please complete the form'})
            return self.question()
        
    def question_delete(self):
        _id = bottle.request.GET.get('_id')
        
        if _id:
            EntityManager(_DBCON).deleteOne('Question', _id)
        
        return bottle.redirect(settings.BASEURL +'/')
        
    def question_view(self):
        q = Question(_DBCON, _id=bottle.request.GET.get('_id'))
        
        self.viewdata.update({'q':q})

        return self._template('question_view')
        
    def question_respond(self):
        _id = bottle.request.POST.get('_id')
        option_id = bottle.request.POST.get('option')

        if _id and option_id:
            q = Question(_DBCON, _id=_id)
            r = Response(_DBCON)
            r.option = option_id
            r.userId = bottle.request.session.userid
            
            q.responses.append(r)
            q.save()
        
        return bottle.redirect(settings.BASEURL +'/')


@route('/', method='GET')
@checklogin
def index():
    return Controller().index()
    
@route('/question', method='GET')
@checklogin
def index():
    return Controller().question()
    
@route('/question', method='POST')
@checklogin
def index():
    return Controller().question_save()
    
@route('/question/delete', method='GET')
@checklogin
def index():
    return Controller().question_delete() 
    
@route('/question/view', method='GET')
@checklogin
def index():
    return Controller().question_view()  
    
@route('/question/respond', method='POST')
@checklogin
def index():
    return Controller().question_respond() 
    
    
#######################################################

if __name__ == '__main__':
    with open(_ROOTPATH +'/app.pid','w') as f:
        f.write(str(os.getpid()))
        
    if settings.DEBUG: bottle.debug() 
    bottle.run(server=settings.SERVER, reloader=settings.DEBUG, host=settings.APPHOST, port=settings.APPPORT, quiet=(settings.DEBUG==False) )
    