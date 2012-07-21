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

# Classes
from ImportExport import AsfImporter

class AsfImporterTest(unittest.TestCase):
       
    # Setup logging
    logger = logging.getLogger('AsfImporterTest')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s Line: %(lineno)d |  %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Class variables
    asf_filename = ''
    asf_keyword = 'KEYWORD'
    
    def setUp(self):
        AsfImporterTest.logger.info('Setting up for the test.')
        
        AsfImporterTest.logger.info('Importing data from the file: ' + AsfImporterTest.asf_filename)
        self.asf_importer = AsfImporter()
        
        AsfImporterTest.logger.info('Separating the ASF data into separate sections.')
        self.asf_sections = {}
        self.testSeperateSections()
        
    def tearDown(self):
        pass
    
    def testSeperateSections(self):
        AsfImporterTest.logger.info('Starting test: testSeperateSections()')
        asf_class_members = AsfImporter.__dict__.keys()
        for asf_class_member in asf_class_members:
            if asf_class_member.split('_')[-1] == AsfImporterTest.asf_keyword:
                keyword = self.asf_importer.__getattribute__(asf_class_member)
                try:
                    self.asf_sections[keyword]
                except KeyError:
                    assert False, 'The section %s was not properly separated.' % (keyword)
        
        AsfImporterTest.logger.info('Finishing: testSeperateSections()')
        
    def testParseVersion(self):
        AsfImporterTest.logger.info('Starting: testParseVersion()')
        # TODO
        AsfImporterTest.logger.info('Finishing: testParseVersion()')
    
    def testParseName(self):
        AsfImporterTest.logger.info('Starting: testParseName()')
        # TODO
        AsfImporterTest.logger.info('Finishing: testParseName()')
    
    def testParseUnits(self):
        AsfImporterTest.logger.info('Starting: testParseUnits()')
        # TODO
        AsfImporterTest.logger.info('Finishing: testParseUnits()')
    
    def testParseDocumentation(self):
        AsfImporterTest.logger.info('Starting: testParseDocumentation()')
        # TODO
        AsfImporterTest.logger.info('Finishing: testParseDocumentation()')
    
    def testParseRoot(self):
        AsfImporterTest.logger.info('Starting: testParseRoot()')
        # TODO
        AsfImporterTest.logger.info('Finishing: testParseRoot()')
    
    def testParseBones(self):
        AsfImporterTest.logger.info('Starting: testParseBones()')
        # TODO
        AsfImporterTest.logger.info('Finishing: testParseBones()')
    
    def testParseBone(self):
        AsfImporterTest.logger.info('Starting: testParseBone()')
        # TODO
        AsfImporterTest.logger.info('Finishing: testParseBone()')
    
    def testParseHierarchy(self):
        AsfImporterTest.logger.info('Starting: testParseHierarchy()')
        # TODO
        AsfImporterTest.logger.info('Finishing: testParseHierarchy()')
    
if __name__=='__main__':
   unittest.main()
   
   