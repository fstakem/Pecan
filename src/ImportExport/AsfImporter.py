#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                         A S F  I M P O R T E R                          |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.13.12

# Libraries
import logging

# Classes

class AsfImporter(object):
    """This is a parsing class that imports data in the mocap ASF format."""
    
    # Setup logging
    logger = logging.getLogger('AsfImporter')
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
    def seperateSections(cls, raw_lines):
        cls.logger.info('seperateSections(): Entering method.')
        
        cls.logger.info('seperateSections(): Exiting method.')
    
    @classmethod
    def parseVersion(cls):
        cls.logger.info('parseVersion(): Entering method.')
        
        cls.logger.info('parseVersion(): Exiting method.')
    
    @classmethod
    def parseName(cls):
        cls.logger.info('parseName(): Entering method.')
        
        cls.logger.info('parseName(): Exiting method.')
    
    @classmethod
    def parseUnits(cls):
        cls.logger.info('parseUnits(): Entering method.')
        
        cls.logger.info('parseUnits(): Exiting method.')
    
    @classmethod
    def parseDocumentation(cls):
        cls.logger.info('parseDocumentation(): Entering method.')
        
        cls.logger.info('parseDocumentation(): Exiting method.')
    
    @classmethod
    def parseRoot(cls):
        cls.logger.info('parseRoot(): Entering method.')
        
        cls.logger.info('parseRoot(): Exiting method.')
    
    @classmethod
    def parseBones(cls):
        cls.logger.info('parseBones(): Entering method.')
        
        cls.logger.info('parseBones(): Exiting method.')
    
    @classmethod
    def parseBone(cls):
        cls.logger.info('parseBone(): Entering method.')
        
        cls.logger.info('parseBone(): Exiting method.')
    
    @classmethod
    def parseHierarchy(cls):
        cls.logger.info('parseHierarchy(): Entering method.')
        
        cls.logger.info('parseHierarchy(): Exiting method.')
    
    