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
    
    def setUp(self):
        AsfImporterTest.logger.info('Setting up for the test.')
        
        AsfImporterTest.logger.info('Importing data from the file: ' + AsfImporterTest.asf_filename)
        
        AsfImporterTest.logger.info('Separating the ASF data into separate sections.')
        self.asf_sections = {}
        
        AsfImporterTest.logger.info('Testing that all of the different ASF sections have been properly found.')
    
    def tearDown(self):
        pass
        
    def testParseVersion(self):
        pass
    
    def testParseName(self):
        pass
    
    def testParseUnits(self):
        pass
    
    def testParseDocumentation(self):
        pass
    
    def testParseRoot(self):
        pass
    
    def testParseBones(self):
        pass
    
    def testParseBone(self):
        pass
    
    def testParseHierarchy(self):
        pass
    
if __name__=='__main__':
   unittest.main()
   
   