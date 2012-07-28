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
from ImportExport import Utilities

# Classes
from ImportExport import AsfImporter
from ImportExport import AcclaimParseException
from MocapMath import Vector

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
    UNITS_KEY = 'length'
    UNITS_VALUE = '0.45' 
    ROOT_POSITION = Vector(0, 0, 0)
    BONE_ID = '1'
    BONE_NAME = 'lhipjoint'
    BONE_DIRECTION = Vector(0.566809, -0.746272, 0.349008)
    BONE_LENGTH = 2.40479
    
    def setUp(self):
        AsfImporterTest.logger.info('Setting up for the test.')
        
        AsfImporterTest.logger.info('Importing data from the file: ' + AsfImporterTest.asf_filename)
        asf_lines = Utilities.readLinesFromFile(AsfImporterTest.asf_filename)
        AsfImporterTest.logger.info('Read %i lines from the file.', len(asf_lines))
        
        AsfImporterTest.logger.info('Separating the ASF data into separate sections.')
        self.asf_sections = AsfImporter.seperateSections(asf_lines)
        self.testSeperateSections()
        
    def tearDown(self):
        pass
    
    def testParseData(self):
        AsfImporterTest.logger.info('Starting: testParseData()')
        
        # The other tests need the data in asf sections but this test needs the raw lines
        AsfImporterTest.logger.info('Importing data from the file: ' + AsfImporterTest.asf_filename)
        asf_lines = Utilities.readLinesFromFile(AsfImporterTest.asf_filename)
        AsfImporterTest.logger.info('Read %i lines from the file.', len(asf_lines))
        #AsfImporter.parseBone(asf_lines)
        
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
                    assert False, 'The %s section was not properly separated.' % (keyword)
        
        AsfImporterTest.logger.info('Finishing: testSeperateSections()')
        
    def testParseVersion(self):
        AsfImporterTest.logger.info('Starting: testParseVersion()')
        
        try:
            version = AsfImporter.parseVersion(self.asf_sections)
            assert version == AsfImporterTest.VERSION, 'Incorrect value for the version number: %s' % (version)
        except AcclaimParseException:
            assert False, 'The version section was not properly parsed.'
        
        AsfImporterTest.logger.info('Finishing: testParseVersion()')
    
    def testParseName(self):
        AsfImporterTest.logger.info('Starting: testParseName()')
        
        try:
            name = AsfImporter.parseName(self.asf_sections)
            assert name == AsfImporterTest.NAME, 'Incorrect value for the name: %s' % (name)
        except AcclaimParseException:
            assert False, 'The name section was not properly parsed.'
            
        AsfImporterTest.logger.info('Finishing: testParseName()')
    
    def testParseUnits(self):
        AsfImporterTest.logger.info('Starting: testParseUnits()')
        
        try:
            units = AsfImporter.parseUnits(self.asf_sections)
            assert units[AsfImporterTest.UNITS_KEY] == AsfImporterTest.UNITS_VALUE, 'Incorrect value for the units: %s' % (units[AsfImporterTest.UNITS_KEY])
        except AcclaimParseException:
            assert False, 'The units section was not properly parsed.'
        except KeyError:
            assert False, 'The units section was not properly parsed.'
            
        AsfImporterTest.logger.info('Finishing: testParseUnits()')
    
    def testParseDocumentation(self):
        AsfImporterTest.logger.info('Starting: testParseDocumentation()')
        
        try:
            documentation = AsfImporter.parseUnits(self.asf_sections)
        except AcclaimParseException:
            assert False, 'The documentation section was not properly parsed.'
            
        AsfImporterTest.logger.info('Finishing: testParseDocumentation()')
    
    def testParseRoot(self):
        AsfImporterTest.logger.info('Starting: testParseRoot()')
        
        try:
            root = AsfImporter.parseRoot(self.asf_sections)
            assert root.position == AsfImporterTest.ROOT_POSITION, 'Incorrect value for the root position: %s' % (str(root.position))
        except AcclaimParseException:
            traceback.print_exc()
            assert False, 'The root section was not properly parsed.'
            
        AsfImporterTest.logger.info('Finishing: testParseRoot()')
    
    def testParseBones(self):
        AsfImporterTest.logger.info('Starting: testParseBones()')
          
        try:
            bones = AsfImporter.parseBones(self.asf_sections)
            bone = bones[0]
            assert bone.id == AsfImporterTest.BONE_ID, 'Incorrect value for the bone id: %d' % (bone.id)
            assert bone.name == AsfImporterTest.BONE_NAME, 'Incorrect value for the bone name: %s' % (bone.name)
            assert bone.direction == AsfImporterTest.BONE_DIRECTION, 'Incorrect value for the bone direction: %s' % (str(bone.direction))
            assert bone.length == AsfImporterTest.BONE_LENGTH, 'Incorrect value for the bone length: %d' % (bone.lngth)
        except AcclaimParseException:
            assert False, 'The root section was not properly parsed.'
        except IndexError:
            assert False, 'The root section was not properly parsed.'
            
        AsfImporterTest.logger.info('Finishing: testParseBones()')
       
    def testParseHierarchy(self):
        AsfImporterTest.logger.info('Starting: testParseHierarchy()')
        # TODO
        AsfImporterTest.logger.info('Finishing: testParseHierarchy()')
    
if __name__=='__main__':
   unittest.main()
   
   