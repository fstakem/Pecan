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
from MocapMath import Vector
from MocapDataFormats import AcclaimBone
from MocapDataFormats import AcclaimRoot
from MocapDataFormats import AsfData
from MocapDataFormats import Axis
from MocapDataFormats import OperationOnAxis

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
                    operation = OperationOnAxis.getOperationOnAxisFromString(token)
                    acclaim_root.amc_data_order.append(operation)
            elif tokens[0] == cls.ROOT_AXIS_LABEL:
                for token in tokens[:]:
                    axis = Axis.getAxisFromString(token)
                    acclaim_root.orientation_order.append(axis)
            elif tokens[0] == cls.ROOT_POSITION_LABEL:
                acclaim_root.position = Vector(tokens[1], tokens[2], tokens[3])
            elif tokens[0] == cls.ROOT_ORIENTATION_LABEL:
                acclaim_root.orientation = Vector(tokens[1], tokens[2], tokens[3])
        
        cls.logger.info('parseRoot(): Exiting method.')
        return acclaim_root
    
    @classmethod
    def parseBones(cls, asf_sections):
        cls.logger.info('parseBones(): Entering method.')
        
        lines = asf_sections[cls.BONES_KEYWORD]
        acclaim_bones = []
        bone_lines = None
        
        for line in lines:
            tokens = line.split()
            
            if tokens[0] == cls.START_LABEL:
                bone_lines = []
            elif tokens[0] == cls.END_LABEL:
                acclaim_bones.append( cls.parseBone(bone_lines) )
            else:
                bone_lines.append(line)
        
        cls.logger.info('parseBones(): Exiting method.')
        return acclaim_bones
    
    @classmethod
    def parseBone(cls, lines):
        cls.logger.info('parseBone(): Entering method.')
        
        acclaim_bone = AcclaimBone()
        last_label = ''
        
        #self.id = 0
        #self.name = ''
        #self.direction = Vector()
        #self.length = 0
        #self.orientation = Vector()
        #self.orientation_order = []
        #self.dof = []
        #self.limits = []
        
        for line in lines:
            tokens = line.split()
            
            if tokens[0] == cls.BONE_ID_LABEL:
                acclaim_bone.id = int(tokens[1])
            elif tokens[0] == cls.BONE_NAME_LABEL:
                acclaim_bone.name = tokens[1]
            elif tokens[0] == cls.BONE_DIRECTION_LABEL:
                acclaim_bone.direction = Vector(tokens[1], tokens[2], tokens[3])
            elif tokens[0] == cls.BONE_LENGTH_LABEL:
                acclaim_bone.length = float(tokens[1])
            elif tokens[0] == cls.BONE_AXIS_LABEL:
                acclaim_bone.orientation = Vector(tokens[1], tokens[2], tokens[3])
                for i in range(len(tokens[4])):
                    axis = Axis.getAxisFromString(tokens[4][i])
                    acclaim_bone.orientation_order.append(axis)
            elif tokens[0] == cls.BONE_DOF_LABEL:
                for token in tokens[1:]:
                    operation_on_axis = OperationOnAxis.getOperationOnAxisFromString(token)
                    acclaim_bone.dof.append(operation_on_axis)
            elif tokens[0] == cls.BONE_LIMITS_LABEL or last_label == cls.BONE_LIMITS_LABEL:
                pass
                # TODO
            
        cls.logger.info('parseBone(): Exiting method.')
        return acclaim_bone
    
    @classmethod
    def parseHierarchy(cls):
        cls.logger.info('parseHierarchy(): Entering method.')
        
        cls.logger.info('parseHierarchy(): Exiting method.')
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    
    
    
