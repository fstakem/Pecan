#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                           U T I L I T I E S                             |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 8.4.12

# Libraries
import logging
import inspect

# This doesn't work but look into it
def log_all_tests(logger, log_seperators, prefix='test'):
    def log_tests(cls):
        for name, m in inspect.getmembers(cls, inspect.ismethod):
            if name.startswith(prefix):
                print name
                print m
                setattr(cls, name, log_test(logger, log_seperators))
        return cls
    return log_tests

def log_test(logger, log_seperators):
    def log(func):
        def onCall(self):
            logger.debug(log_seperators[0])
            logger.debug('Starting: ' + func.func_name + '()')
            
            func(self)
            
            logger.debug('Finishing: ' + func.func_name + '()')
            logger.debug(log_seperators[1])
            logger.debug('')
        return onCall
    return log

def readLinesFromFile(filename):
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    
    return lines
 
# Test out complex decorator
logger = logging.getLogger('Utilities')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s Line: %(lineno)d |  %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

header_line = '******************************************************' 
footer_line = header_line
log_seperator = (header_line, footer_line)

@log_test(logger, log_seperator)   
def foo():
    logger.info('This is a test of the decorator generator.')
     
    
if __name__=='__main__':
   foo()
   
   