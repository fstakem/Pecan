#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                         A M C  I M P O R T E R                          |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.13.12

# Libraries
import logging

# Classes

class AmcImporter(object):
    """This is a parsing class that imports data in the mocap AMC format."""
    
    # Setup logging
    logger = logging.getLogger('AmcImporter')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s Line: %(lineno)d |  %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Class constants
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    @classmethod
    def seperateFrames(cls):
        cls.logger.info('seperateFrames(): Entering method.')
        
        cls.logger.info('seperateFrames(): Exiting method.')
    
    @classmethod
    def parseFrames(cls):
        cls.logger.info('parseFrames(): Entering method.')
        
        cls.logger.info('parseFrames(): Exiting method.')
    
    @classmethod
    def parseFrame(cls):
        cls.logger.info('parseFrame(): Entering method.')
        
        cls.logger.info('parseFrame(): Exiting method.')
    
    @classmethod
    def initializeBones(cls):
        cls.logger.info('initializeBones(): Entering method.')
        
        cls.logger.info('initializeBones(): Exiting method.')
    
    @classmethod
    def checkForAllBonesInFrame(cls):
        cls.logger.info('checkForAllBonesInFrame(): Entering method.')
        
        cls.logger.info('checkForAllBonesInFrame(): Exiting method.')
    
    
    