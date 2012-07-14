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
    COMMENT_CHAR = '#'
    KEYWORD_CHAR = ':'
    VERSION_KEYWORD = 'version'
    NAME_KEYWORD = 'name'
    UNITS_KEYWORD = 'units'
    ROOT_KEYWORD = 'root'
    DOCUMENTATION_KEYWORD = 'documentation'
    BONES_KEYWORD = 'bonedata'
    HIERARCHY_KEYWORD = 'hierarchy'
    START_LABEL = 'begin'
    END_LABEL = 'end'
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    @classmethod
    def seperateSections(cls, raw_lines):
        cls.logger.info('seperateSections(): Entering method.')
        
        asf_sections = {}
        current_keyword = ''
        current_lines = None
        
        for raw_line in raw_lines:
            line = raw_line.strip()
            
            if line.startswith(cls.COMMENT_CHAR):
                continue
            elif line.startswith(cls.KEYWORD_CHAR):
                if len(current_lines) != 0:
                    asf_sections[current_keyword] = current_lines
                    
                tokens = line.split()
                current_keyword = tokens[0][1:]
                current_lines = []
                
                if len(tokens) > 1:
                    keyword_line = ''
                    
                    for token in tokens:
                        keyword_line += token + ' '
                        
                    current_lines.append(keyword_line.strip())
            elif current_lines != None:
                current_lines.append(line)
                
        if current_lines != None:
            asf_sections[current_keyword] = current_lines
        
        cls.logger.info('seperateSections(): Exiting method.')
        return asf_sections
    
    @classmethod
    def parseVersion(cls, asf_sections):
        cls.logger.info('parseVersion(): Entering method.')
        
        lines = asf_sections[cls.VERSION_KEYWORD]
        
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
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    
    
    
