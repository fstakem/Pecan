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
    COMMENT_CHAR = '#'
    KEYWORD_CHAR = ':'
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    # None
    
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    @classmethod
    def seperateFrames(cls, raw_lines):
        cls.logger.info('seperateFrames(): Entering method.')
        
        frames = {}
        frame_lines = []
        
        for raw_line in raw_lines:
            line = raw_line.strip()
            
            if line.startswith(cls.COMMENT_CHAR) or line.startswith(cls.KEYWORD_CHAR):
                continue
            
            tokens = line.split()
            
            if tokens[0].isdigit():
                pass
            else:
                pass
        
        cls.logger.info('seperateFrames(): Exiting method.')
        return frames
    
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
    
    
    