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
from MocapDataFormats import AcclaimBone
from MocapDataFormats import AcclaimRoot
from MocapDataFormats import AsfData

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
    
    ROOT_ORDER_LABEL = 'order'
    ROOT_AXIS_LABEL = 'axis'
    ROOT_POSITION_LABEL = 'position'
    ROOT_ORIENTATION_LABEL = 'orientation'
    
    BONE_ID_LABEL = 'id'
    BONE_NAME_LABEL = 'name'
    BONE_DIRECTION_LABEL = 'direction'
    BONE_POSITION_LABEL = 'position'
    BONE_ORIENTATION_LABEL = 'orientation'
    BONE_LENGTH_LABEL = 'length'
    BONE_ORDER_LABEL = 'order'
    BONE_AXIS_LABEL = 'axis'
    BONE_DOF_LABEL = 'dof'
    BONE_LIMITS_LABEL = 'limits'
    
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
        version = lines[0].split()[0]
        
        cls.logger.info('parseVersion(): Exiting method.')
        return version
    
    @classmethod
    def parseName(cls, asf_sections):
        cls.logger.info('parseName(): Entering method.')
        
        lines = asf_sections[cls.NAME_KEYWORD]
        name = lines[0].split()[0]
        
        cls.logger.info('parseName(): Exiting method.')
        return name
    
    @classmethod
    def parseUnits(cls, asf_sections):
        cls.logger.info('parseUnits(): Entering method.')
        
        lines = asf_sections[cls.UNITS_KEYWORD]
        units = {}
        
        for line in lines:
            tokens = line.split()
            units[tokens[0]] = tokens[1]
        
        cls.logger.info('parseUnits(): Exiting method.')
        return units
    
    @classmethod
    def parseDocumentation(cls, asf_sections):
        cls.logger.info('parseDocumentation(): Entering method.')
        
        lines = asf_sections[cls.DOCUMENTATION_KEYWORD]
        
        cls.logger.info('parseDocumentation(): Exiting method.')
        return lines
    
    @classmethod
    def parseRoot(cls, asf_sections):
        cls.logger.info('parseRoot(): Entering method.')
        
        lines = asf_sections[cls.ROOT_KEYWORD]
        acclaim_root = AcclaimRoot()
        
        for line in lines:
            tokens = line.split()
            
            if tokens[0] == cls.ROOT_ORDER_LABEL:
                for token in tokens[1:]:
                    acclaim_root.amc_data_order.append(token)
            elif tokens[0] == cls.ROOT_AXIS_LABEL:
                pass
            elif tokens[0] == cls.ROOT_POSITION_LABEL:
                pass
            elif tokens[0] == cls.ROOT_ORIENTATION_LABEL:
                pass
        
        cls.logger.info('parseRoot(): Exiting method.')
        return acclaim_root
    
    @classmethod
    def parseBones(cls, asf_sections):
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
    
    
    
