
#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                   A M C  I M P O R T E R  T E S T                       |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.17.12

# Libraries
import logging
import unittest
import traceback
from collections import OrderedDict

# Classes
from Globals import *
from Utilities import *
from ImportExport import *
from MocapMath import *
from MocapDataFormats import *

class AmcImporterTest(unittest.TestCase):
       
    # Setup logging
    logger = logging.getLogger('AmcImporterTest')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s Line: %(lineno)d |  %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Class variables
    amc_filename = '../data/amc.amc'
    NUMBER_OF_FRAMES = 149
    FRAME_NUMBER = 3
    BONE_ORIENTATIONS = OrderedDict( [ ( 'root', [ 9.36924, 17.8658, -17.3215, -2.08624, -7.53541, -3.20952 ] ), 
                                       ( 'lowerback', [ 2.40927, -0.341368, 1.15325 ] ),
                                       ( 'upperback', [ 0.0914609, -0.391867, 2.6267 ] ),
                                       ( 'thorax', [ -1.24644, -0.196673, 2.06109 ] ),
                                       ( 'lowerneck', [ -9.29056, -3.91364, -6.80735 ] ),
                                       ( 'upperneck', [ 27.3923, -3.57141, -2.52178 ] ),
                                       ( 'head', [ 10.3988, -2.65388, -0.15793 ] ),
                                       ( 'rclavicle', [ 1.11071e-014, -7.15625e-015] ),
                                       ( 'rhumerus', [ -29.4949, -11.4934, -80.8962 ] ),
                                       ( 'rradius', [ 21.0916 ] ),
                                       ( 'rwrist', [ -9.76415 ] ),
                                       ( 'rhand', [ -18.6086, -20.6482 ] ),
                                       ( 'rfingers', [ 7.12502 ] ),
                                       ( 'rthumb', [ 7.68291, -50.4886 ] ),
                                       ( 'lclavicle', [ 1.11071e-014, -7.15625e-015 ] ),
                                       ( 'lhumerus', [ 18.0329, -14.7893, 62.8649 ] ),
                                       ( 'lradius', [ 136.077 ] ),
                                       ( 'lwrist', [ 10.2479 ] ),
                                       ( 'lhand', [ -37.5642, -18.6327 ] ),
                                       ( 'lfingers', [ 7.12502 ] ),
                                       ( 'lthumb', [ -10.6189, 11.079 ] ),
                                       ( 'rfemur', [ -0.584382, 4.63926, 22.5698 ] ),
                                       ( 'rtibia', [ 26.6186 ] ),
                                       ( 'rfoot', [ -15.2777, -10.1364 ] ),
                                       ( 'rtoes', [ 3.73231 ] ),
                                       ( 'lfemur', [ 4.15146, 1.15468, -13.8566 ] ),
                                       ( 'ltibia', [ 19.9336 ] ),
                                       ( 'lfoot', [ -16.299, 6.62697 ] ),
                                       ( 'ltoes', [ -5.03798 ] ) ])
    
    def setUp(self):
        AmcImporterTest.logger.info('Starting: setUp()')
        
        AmcImporterTest.logger.info('Importing data from the file: ' + AmcImporterTest.amc_filename)
        self.amc_lines = Utilities.readLinesFromFile(AmcImporterTest.amc_filename)
        AmcImporterTest.logger.info('Read %i lines from the file.', len(self.amc_lines))
        
        AmcImporterTest.logger.info('Separating the AMC data into separate frames.')
        self.amc_frames = AmcImporter.seperateFrames(self.amc_lines)
        self.testSeperateFrames()
        
        AmcImporterTest.logger.info('Finishing: setUp()')
    
    def tearDown(self):
        pass
    
    @log_test(logger, globals.log_seperator)
    def testParseData(self):
        try:
            AmcImporter.parseData(self.amc_lines)
        except AcclaimParseException:
            traceback.print_exc()
            assert False, 'The file was not properly parsed.'
     
    @log_test(logger, globals.log_seperator)   
    def testSeperateFrames(self):
        number_of_frames = len(self.amc_frames)
        assert number_of_frames == AmcImporterTest.NUMBER_OF_FRAMES, 'Incorrect number of frames parsed: %s' % (str(number_of_frames))
      
    @log_test(logger, globals.log_seperator) 
    def testParseFrame(self):
        try:
            acclaim_frame = AmcImporter.parseFrame(self.amc_frames[AmcImporterTest.FRAME_NUMBER])
            assert acclaim_frame.number == AmcImporterTest.FRAME_NUMBER, 'Incorrect frame: %s' % (str(acclaim_frame.number))
            
            for key in AmcImporterTest.BONE_ORIENTATIONS.keys():
                for i, value in enumerate(AmcImporterTest.BONE_ORIENTATIONS[key]):
                    assert value == acclaim_frame.bone_orientations[key][i], 'Incorrect orientation value: %s' % (str(acclaim_frame[key][i]))
        except AcclaimParseException:
            traceback.print_exc()
            assert False, 'The frame was not properly parsed.'
        except KeyError:
            traceback.print_exc()
            AmcImporterTest.logger.info('Frame: %s' % (str(acclaim_frame)))
            assert False, 'The frame was not properly parsed.' 
    
    @log_test(logger, globals.log_seperator)   
    def testCheckForAllBones(self):
        try:
            acclaim_frame = AmcImporter.parseFrame(self.amc_frames[AmcImporterTest.FRAME_NUMBER])
            assert acclaim_frame.number == AmcImporterTest.FRAME_NUMBER, 'Incorrect frame: %s' % (str(acclaim_frame.number))
            
            contains_all_bones = AmcImporter.checkForAllBones(acclaim_frame, AmcImporterTest.BONE_ORIENTATIONS.keys())
            assert contains_all_bones, 'Not all the expected bones are contained in the frame.'
            
        except AcclaimParseException:
            traceback.print_exc()
            assert False, 'The frame was not properly parsed.'
        except KeyError:
            traceback.print_exc()
            AmcImporterTest.logger.info('Frame: %s' % (str(acclaim_frame)))
            assert False, 'The frame was not properly parsed.' 
            
    
if __name__=='__main__':
   unittest.main()
   
   
   