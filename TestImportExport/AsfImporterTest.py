#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                  A S F  I M P O R T E R  T E S T                        |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.17.12

# Libraries
import logging
import unittest
import traceback

# Classes
from ImportExport import Utilities
from ImportExport import AsfImporter
from ImportExport import AcclaimParseException
from MocapMath import Vector
from MocapDataFormats import Axis
from MocapDataFormats import OperationOnAxis

class AsfImporterTest(unittest.TestCase):
       
    # Setup logging
    logger = logging.getLogger('AsfImporterTest')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s Line: %(lineno)d |  %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Class variables
    asf_filename = '../data/asf.asf'
    ASF_KEYWORD = 'KEYWORD'
    VERSION = '1.10'
    NAME = 'VICON'
    UNITS_MASS_KEY = 'mass'
    UNITS_MASS_VALUE = '1.0' 
    UNITS_LENGTH_KEY = 'length'
    UNITS_LENGTH_VALUE = '0.45'
    UNITS_ANGLE_KEY = 'angle'
    UNITS_ANGLE_VALUE = 'deg'
    ROOT_ORDER = ( OperationOnAxis('TX'), OperationOnAxis('TY'), OperationOnAxis('TZ'),
                   OperationOnAxis('RX'), OperationOnAxis('RY'), OperationOnAxis('RZ') )
    ROOT_AXIS = ( Axis('X'), Axis('Y'), Axis('Z') )
    ROOT_POSITION = Vector(0, 0, 0)
    ROOT_ORIENTATION = Vector(0, 0, 0)
    BONE_INDEX = 1
    BONE_ID = 2
    BONE_NAME = 'lfemur'
    BONE_DIRECTION = Vector(0.34202, -0.939693, 0.0)
    BONE_LENGTH = 7.1578
    BONE_ORIENTATION = Vector(0.0, 0.0, 20.0)
    BONE_ORIENTATION_ORDER = ( Axis('X'), Axis('Y'), Axis('Z') )
    BONE_DOF = ( OperationOnAxis('RX'), OperationOnAxis('RY'), OperationOnAxis('RZ') )
    BONE_LIMITS = ( (-160.0, 20.0), (-70.0, 70.0), (-60.0, 70.0) )
    HIERARCHY = ( 'lfemur', 'ltibia' )
    
    def setUp(self):
        AsfImporterTest.logger.info('Setting up for the test.')
        
        AsfImporterTest.logger.info('Importing data from the file: ' + AsfImporterTest.asf_filename)
        self.asf_lines = Utilities.readLinesFromFile(AsfImporterTest.asf_filename)
        AsfImporterTest.logger.info('Read %i lines from the file.', len(self.asf_lines))
        
        AsfImporterTest.logger.info('Separating the ASF data into separate sections.')
        self.asf_sections = AsfImporter.seperateSections(self.asf_lines)
        self.testSeperateSections()
        
    def tearDown(self):
        pass
    
    def testParseData(self):
        AsfImporterTest.logger.info('Starting: testParseData()')
         
        try:
            AsfImporter.parseData(self.asf_lines)
        except AcclaimParseException:
            traceback.print_exc()
            assert False, 'The file was not properly parsed.'
        
        AsfImporterTest.logger.info('Finishing: testParseData()')
    
    def testSeperateSections(self):
        AsfImporterTest.logger.info('Starting: testSeperateSections()')
        asf_class_members = AsfImporter.__dict__.keys()
        for asf_class_member in asf_class_members:
            if asf_class_member.split('_')[-1] == AsfImporterTest.ASF_KEYWORD:
                asf_importer = AsfImporter()
                keyword = asf_importer.__getattribute__(asf_class_member)
                try:
                    self.asf_sections[keyword]
                except KeyError:
                    traceback.print_exc()
                    AsfImporterTest.logger.info('Keyword: %s' % (keyword))
                    assert False, 'The %s section was not properly separated.' % (keyword)
        
        AsfImporterTest.logger.info('Finishing: testSeperateSections()')
        
    def testParseVersion(self):
        AsfImporterTest.logger.info('Starting: testParseVersion()')
        
        try:
            version = AsfImporter.parseVersion(self.asf_sections)
            assert version == AsfImporterTest.VERSION, 'Incorrect value for the version number: %s' % (version)
        except AcclaimParseException:
            traceback.print_exc()
            assert False, 'The version section was not properly parsed.'
        
        AsfImporterTest.logger.info('Finishing: testParseVersion()')
    
    def testParseName(self):
        AsfImporterTest.logger.info('Starting: testParseName()')
        
        try:
            name = AsfImporter.parseName(self.asf_sections)
            assert name == AsfImporterTest.NAME, 'Incorrect value for the name: %s' % (name)
        except AcclaimParseException:
            traceback.print_exc()
            assert False, 'The name section was not properly parsed.'
            
        AsfImporterTest.logger.info('Finishing: testParseName()')
    
    def testParseUnits(self):
        AsfImporterTest.logger.info('Starting: testParseUnits()')
              
        try:
            units = AsfImporter.parseUnits(self.asf_sections)
            assert units[AsfImporterTest.UNITS_MASS_KEY] == AsfImporterTest.UNITS_MASS_VALUE, 'Incorrect value for the units: %s' % (units[AsfImporterTest.UNITS_MASS_KEY])
            assert units[AsfImporterTest.UNITS_LENGTH_KEY] == AsfImporterTest.UNITS_LENGTH_VALUE, 'Incorrect value for the units: %s' % (units[AsfImporterTest.UNITS_LENGTH_KEY])
            assert units[AsfImporterTest.UNITS_ANGLE_KEY] == AsfImporterTest.UNITS_ANGLE_VALUE, 'Incorrect value for the units: %s' % (units[AsfImporterTest.UNITS_ANGLE_KEY])
        except AcclaimParseException:
            traceback.print_exc()
            assert False, 'The units section was not properly parsed.'
        except KeyError:
            traceback.print_exc()
            AsfImporterTest.logger.info('Units: %s' % (str(units)))
            assert False, 'The units section was not properly parsed.'
            
        AsfImporterTest.logger.info('Finishing: testParseUnits()')
    
    def testParseDocumentation(self):
        AsfImporterTest.logger.info('Starting: testParseDocumentation()')
        
        try:
            documentation = AsfImporter.parseUnits(self.asf_sections)
        except AcclaimParseException:
            traceback.print_exc()
            AsfImporterTest.logger.info('Documentation:')
            assert False, 'The documentation section was not properly parsed.'
            
        AsfImporterTest.logger.info('Finishing: testParseDocumentation()')
    
    def testParseRoot(self):
        AsfImporterTest.logger.info('Starting: testParseRoot()')
        
        try:
            root = AsfImporter.parseRoot(self.asf_sections)
            for i, data_order in enumerate(AsfImporterTest.ROOT_ORDER):
                assert root.amc_data_order[i] == data_order, 'Incorrect value for the AMC data order: %s' % (str(root.amc_data_order[i]))
            
            for i, orientation_order in enumerate(AsfImporterTest.ROOT_AXIS):
                assert root.orientation_order[i] == orientation_order, 'Incorrect value for the root orientation order: %s' % (str(root.orientation_order))

            assert root.position == AsfImporterTest.ROOT_POSITION, 'Incorrect value for the root position: %s' % (str(root.position))
            assert root.orientation == AsfImporterTest.ROOT_ORIENTATION, 'Incorrect value for the root orientation: %s' % (str(root.orientation))
        except AcclaimParseException:
            traceback.print_exc()
            assert False, 'The root section was not properly parsed.'
            
        AsfImporterTest.logger.info('Finishing: testParseRoot()')
    
    def testParseBones(self):
        AsfImporterTest.logger.info('Starting: testParseBones()')
           
        try:
            bones = AsfImporter.parseBones(self.asf_sections)
            bone = bones[AsfImporterTest.BONE_INDEX]
            assert bone.id == AsfImporterTest.BONE_ID, 'Incorrect value for the bone id: %d' % (bone.id)
            assert bone.name == AsfImporterTest.BONE_NAME, 'Incorrect value for the bone name: %s' % (bone.name)
            assert bone.direction == AsfImporterTest.BONE_DIRECTION, 'Incorrect value for the bone direction: %s' % (str(bone.direction))
            assert bone.length == AsfImporterTest.BONE_LENGTH, 'Incorrect value for the bone length: %d' % (bone.lngth)
            assert bone.orientation == AsfImporterTest.BONE_ORIENTATION, 'Incorrect value for the bone orientation: %s' % (str(bone.orientation))
        
            for i, orientation_order in enumerate(AsfImporterTest.BONE_ORIENTATION_ORDER):
                assert bone.orientation_order[i] == orientation_order, 'Incorrect value for the bone orientation order: %s' % (str(bone.orientation_order[i]))
    
            for i, dof in enumerate(AsfImporterTest.BONE_DOF):
                assert bone.dof[i] == dof, 'Incorrect value for the bone dof order: %s' % (str(bone.dof[i]))

            for i, limits in enumerate(bone.limits):
                for j, limit in enumerate(limits):
                    assert limit == AsfImporterTest.BONE_LIMITS[i][j], 'Incorrect value for the limit: %s' % (str(dof))
                    
            for i, limits in enumerate(AsfImporterTest.BONE_LIMITS):
                for j, limit in enumerate(limits):
                    assert bone.limits[i][j] == limit, 'Incorrect value for the limit: %s' % (str(bone.limits[i][j]))

        except AcclaimParseException:
            traceback.print_exc()
            assert False, 'The bone section was not properly parsed.'
        except IndexError:
            traceback.print_exc()
            AsfImporterTest.logger.info('Bone:')
            AsfImporterTest.logger.info('%s' % (str(bone)))
            assert False, 'The bone section was not properly parsed.'
            
        AsfImporterTest.logger.info('Finishing: testParseBones()')
       
    def testParseHierarchy(self):
        AsfImporterTest.logger.info('Starting: testParseHierarchy()')
    
        try:
            hierarchy = AsfImporter.parseHierarchy(self.asf_sections)
            children = hierarchy[AsfImporterTest.HIERARCHY[0]]
            for bone in AsfImporterTest.HIERARCHY[1:]:
                children.index(bone)
        except AcclaimParseException:
            traceback.print_exc()
            assert False, 'The hierarchy section was not properly parsed.'
        except KeyError:
            traceback.print_exc()
            AsfImporterTest.logger.info('Hierarchy: %s' % (str(hierarchy)))
            assert False, 'The hierarchy section was not properly parsed.'
        except ValueError:
            assert False, 'The hierarchy section did not contain: %s' % (bone)
        
        AsfImporterTest.logger.info('Finishing: testParseHierarchy()')
    
if __name__=='__main__':
   unittest.main()
   
   