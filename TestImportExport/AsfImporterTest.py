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
from ImportExport import Utilities

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
    asf_filename = '../data/asf.asf'
    asf_keyword = 'KEYWORD'
    
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
        AsfImporter.parseBone(asf_lines)
        
        AsfImporterTest.logger.info('Finishing: testParseData()')
    
    def testSeperateSections(self):
        AsfImporterTest.logger.info('Starting: testSeperateSections()')
        asf_class_members = AsfImporter.__dict__.keys()
        for asf_class_member in asf_class_members:
            if asf_class_member.split('_')[-1] == AsfImporterTest.asf_keyword:
                asf_importer = AsfImporter()
                keyword = asf_importer.__getattribute__(asf_class_member)
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
   
   