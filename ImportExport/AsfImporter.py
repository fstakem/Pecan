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
from AcclaimParseException import AcclaimParseException

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
    def parseData(cls, raw_lines):
        cls.logger.info('parseData(): Entering method.')
        
        asf_data = AsfData()
        asf_sections = cls.seperateSections(raw_lines)
        asf_data.version = asf_sections[cls.VERSION_KEYWORD]
        asf_data.name = asf_sections[cls.NAME_KEYWORD]
        asf_data.units = asf_sections[cls.UNITS_KEYWORD]
        asf_data.documentation = asf_sections[cls.DOCUMENTATION_KEYWORD]
        asf_data.acclaim_root = asf_sections[cls.ROOT_KEYWORD]
        asf_data.bones = asf_sections[cls.BONES_KEYWORD]
        asf_data.hierarchy = asf_sections[cls.HIERARCHY_KEYWORD]
        
        cls.logger.info('parseData(): Exiting method.')
        return asf_data
    
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
                if current_lines != None:
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
            
        for key in asf_sections.keys():
            cls.logger.info('Found the ASF section: %s' % (key))
        
        cls.logger.info('seperateSections(): Exiting method.')
        return asf_sections
    
    @classmethod
    def parseVersion(cls, asf_sections):
        cls.logger.info('parseVersion(): Entering method.')
        
        try:
            lines = asf_sections[cls.VERSION_KEYWORD]
            version = lines[0].split()[1]
        except KeyError:
            raise AcclaimParseException("Asf version section was not found.")
        except IndexError:
            raise AcclaimParseException("Error parsing the asf version data.")
        
        cls.logger.info('Found version: %s' % (version))
        cls.logger.info('parseVersion(): Exiting method.')
        return version
    
    @classmethod
    def parseName(cls, asf_sections):
        cls.logger.info('parseName(): Entering method.')
        
        try:
            lines = asf_sections[cls.NAME_KEYWORD]
            name = lines[0].split()[1]
        except KeyError:
            raise AcclaimParseException("Asf name section was not found.")
        except IndexError:
            raise AcclaimParseException("Error parsing the asf name data.")
        
        cls.logger.info('Found name: %s' % (name))
        cls.logger.info('parseName(): Exiting method.')
        return name
    
    @classmethod
    def parseUnits(cls, asf_sections):
        cls.logger.info('parseUnits(): Entering method.')
        
        try:
            lines = asf_sections[cls.UNITS_KEYWORD]
        except KeyError:
            raise AcclaimParseException("Asf units section was not found.")
        
        units = {}
        
        if len(lines) > 0:
            for line in lines:
                tokens = line.split()
                try:
                    units[tokens[0]] = tokens[1]
                except IndexError:
                    raise AcclaimParseException("Error parsing the asf unit data.")
        else:
            raise AcclaimParseException("No data found for the asf unit section.")
        
        for key in units.keys():
            cls.logger.info('Found unit: %s => %s' % (key, units[key]))  
        
        cls.logger.info('parseUnits(): Exiting method.')
        return units
    
    @classmethod
    def parseDocumentation(cls, asf_sections):
        cls.logger.info('parseDocumentation(): Entering method.')
        
        try:
            lines = asf_sections[cls.DOCUMENTATION_KEYWORD]
        except KeyError:
            cls.logger.info('Could not find the asf documentation section.')
        
        for line in lines:
            cls.logger.info('Found documentation line: %s' % (line))
            
        cls.logger.info('parseDocumentation(): Exiting method.')
        return lines
    
    @classmethod
    def parseRoot(cls, asf_sections):
        cls.logger.info('parseRoot(): Entering method.')
        
        try:
            lines = asf_sections[cls.ROOT_KEYWORD]
        except KeyError:
            raise AcclaimParseException("Asf root section was not found.")
        
        acclaim_root = AcclaimRoot()
        print '***ROOT***'
        print lines
        
        if len(lines) > 3:
            for line in lines:
                tokens = line.split()
                
                try:
                    if tokens[0] == cls.ROOT_ORDER_LABEL:
                        for token in tokens[1:]:
                            operation = OperationOnAxis.getOperationOnAxisFromString(token)
                            acclaim_root.amc_data_order.append(operation)
                    elif tokens[0] == cls.ROOT_AXIS_LABEL:
                        acclaim_root.orientation_order.append(Axis.getAxisFromString(tokens[0]))
                        acclaim_root.orientation_order.append(Axis.getAxisFromString(tokens[1]))
                        acclaim_root.orientation_order.append(Axis.getAxisFromString(tokens[2]))
                    elif tokens[0] == cls.ROOT_POSITION_LABEL:
                        acclaim_root.position = Vector(tokens[1], tokens[2], tokens[3])
                    elif tokens[0] == cls.ROOT_ORIENTATION_LABEL:
                        acclaim_root.orientation = Vector(tokens[1], tokens[2], tokens[3])
                    else:
                        raise AcclaimParseException("Label in asf root section is unknown.")
                except IndexError:
                    raise AcclaimParseException("Data missing from a label in the asf root section.")
        else:
            raise AcclaimParseException("Asf root section does not have all of the data.")
        
        cls.logger.info('Found root: %s' % (str(acclaim_root)))
        cls.logger.info('parseRoot(): Exiting method.')
        return acclaim_root
    
    @classmethod
    def parseBones(cls, asf_sections):
        cls.logger.info('parseBones(): Entering method.')
        
        try:
            lines = asf_sections[cls.BONES_KEYWORD]
        except KeyError:
            raise AcclaimParseException("Asf bones section was not found.")
        
        acclaim_bones = []
        bone_lines = None
        
        if len(lines) > 0:
            for line in lines:
                tokens = line.split()
                
                if tokens[0] == cls.START_LABEL:
                    bone_lines = []
                elif tokens[0] == cls.END_LABEL:
                    acclaim_bones.append( cls.parseBone(bone_lines) )
                else:
                    bone_lines.append(line)
        else:
            raise AcclaimParseException("No data found in the asf bones section.")
        
        cls.logger.info('parseBones(): Exiting method.')
        return acclaim_bones
    
    @classmethod
    def parseBone(cls, lines):
        cls.logger.info('parseBone(): Entering method.')
        
        acclaim_bone = AcclaimBone()
        last_label = ''
         
        for line in lines:
            tokens = line.split()
            
            try:
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
                    reformatted_line = line.replace(cls.BONE_LIMITS_LABEL, '')
                    reformatted_line = reformatted_line.replace('(', '')
                    reformatted_line = reformatted_line.replace(')', '')
                    tokens = line.split()
                    
                    limits = []
                    for token in tokens:
                        limits.append(float(token))
                    acclaim_bone.limits.append(limits)
                    
            except IndexError:
                raise AcclaimParseException("Data is missing from a label in one of the bones.")
            except ValueError:
                raise AcclaimParseException("Data from one of the bone labels is not the right type.")
        
        cls.logger.info('Found bone: %s' % (str(acclaim_bone)))    
        cls.logger.info('parseBone(): Exiting method.')
        return acclaim_bone
    
    @classmethod
    def parseHierarchy(cls, asf_sections):
        cls.logger.info('parseHierarchy(): Entering method.')
        
        try:
            lines = asf_sections[cls.HIERARCHY_KEYWORD]
        except KeyError:
            raise AcclaimParseException("Asf hierarchy section was not found.")
        
        hierarchy = {}
        
        if len(lines) > 0:
            for line in lines:
                tokens = line.split()
                
                if tokens[0] == cls.START_LABEL:
                    continue
                elif tokens[0] == cls.END_LABEL:
                    break
                
                children = []
                for token in tokens[1:]:
                    children.append(token)
                    
                hierarchy[tokens[0]] = children
        else:
            raise AcclaimParseException("No data found in the asf hierarchy section.")
        
        for key in hierarchy.keys():
            cls.logger.info('Found hierarchy node: %s %s' % ( str(key, ' '.join(str(hierarchy[key])[1:-1].split(', '))) ))
        
        cls.logger.info('parseHierarchy(): Exiting method.')
        return hierarchy
    
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    
    
# Simple class tests
if __name__=='__main__':
    asf_importer = AsfImporter()
    keys = AsfImporter.__dict__.keys()
    
    for key in keys:
        print key + '    ' + str(asf_importer.__getattribute__(key))
    
     
