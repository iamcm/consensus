import sys, traceback
from datetime import datetime
import settings

class Logger:    
    @staticmethod
    def log_to_file(content, logfile=None):
        _file = logfile or settings.LOGFILEPATH
        
        with open(_file, 'a') as f:
            output = Logger.format(content)
            f.write(output)
            
    @staticmethod
    def format(content):
        dt = datetime.now()
        timestamp = dt.strftime("%A, %d. %B %Y %I:%M%p")
        
        return """
###########
%s
-----------
%s
###########
""" % (timestamp, str(content))

    @staticmethod
    def log_exception(logfile=None):
        _file = logfile or settings.LOGFILEPATH
        
        exceptiontype, value, exceptiontraceback = sys.exc_info()
        
        with open(_file, 'a') as f:
            output = Logger.format('')
            f.write(output)
            traceback.print_exception(exceptiontype, value, exceptiontraceback, file=f)