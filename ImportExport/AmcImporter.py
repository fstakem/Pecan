#  .-------------------------------------------------------------------------.
#  |                                                                         |
#  |                         A M C  I M P O R T E R                          |
#  |                                                                         |
#  '-------------------------------------------------------------------------'

#  By: Fred Stakem 
#  Date: 7.13.12

# Libraries
import logging
from collections import OrderedDict

# Classes
from MocapDataFormats import AcclaimFrame
from AcclaimParseException import AcclaimParseException

class AmcImporter(object):
    """This is a parsing class that imports data in the mocap AMC format."""
    
    # Setup logging
    logger = logging.getLogger('AmcImporter')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(name)s Line: %(lineno)d |  %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Class constants
    COMMENT_CHAR = '#'
    KEYWORD_CHAR = ':'
    
    # -----------------------------------------------------------------------
    #       Class Functions
    # -----------------------------------------------------------------------
    @classmethod
    def parseData(cls, raw_lines):
        cls.logger.info('parseData(): Entering method.')
        
        frames = AmcImporter.seperateFrames(raw_lines)
        acclaim_frames = OrderedDict()
        bones = []
        for i, key in enumerate(frames.keys()):
            acclaim_frame = AmcImporter.parseFrame(frames[key])
            
            if i == 0:
                bones = acclaim_frame.bone_orientations.keys()
            else:
                if not AmcImporter.checkForAllBones(acclaim_frame, bones):
                    raise AcclaimParseException('Not all expected bones contained in the frame.')
            
            acclaim_frames[acclaim_frame.number] = acclaim_frame
            
        cls.logger.info('parseData(): Exiting method.')
        return acclaim_frames
    
    @classmethod
    def seperateFrames(cls, raw_lines):
        cls.logger.info('seperateFrames(): Entering method.')
        
        frames = OrderedDict()
        current_frame = None
        frame_lines = []
        
        for raw_line in raw_lines:
            line = raw_line.strip()
            
            if line.startswith(cls.COMMENT_CHAR) or line.startswith(cls.KEYWORD_CHAR):
                continue
            
            tokens = line.split()
            
            if tokens[0].isdigit():
                try:
                    if current_frame == None:
                        current_frame = int(tokens[0])
                        frame_lines = [current_frame]
                    else:
                        frames[current_frame] = frame_lines
                        current_frame = int(tokens[0])
                        frame_lines = [current_frame]
                except ValueError:
                    raise AcclaimParseException("The frame is improperly formed.")
            else:
                frame_lines.append(line)
        
        cls.logger.info('Found the %s frames.' % (str(len(frames.keys()))))
        cls.logger.info('seperateFrames(): Exiting method.')
        return frames
       
    @classmethod
    def parseFrame(cls, lines):
        cls.logger.info('parseFrame(): Entering method.')
        
        acclaim_frame = AcclaimFrame()
        
        try:
            acclaim_frame.number = lines[0]
            
            for line in lines[1:]:
                tokens = line.split()
                
                bone_orientations = []
                for token in tokens[1:]:
                    bone_orientations.append(float(token))
                    
                acclaim_frame.bone_orientations[tokens[0]] = bone_orientations
        except IndexError:
            raise AcclaimParseException("The frame is improperly formed.")
        
        cls.logger.info('Found the frame: %s' % (str(acclaim_frame)))
        cls.logger.info('parseFrame(): Exiting method.')
        return acclaim_frame
       
    @classmethod
    def checkForAllBones(cls, frame, all_bones):
        cls.logger.info('checkForAllBonesInFrame(): Entering method.')
        
        for bone in all_bones:
            try:
                frame.bone_orientations[bone]
            except KeyError:
                return False
            
        return True
         
        cls.logger.info('checkForAllBonesInFrame(): Exiting method.')
        
    # -----------------------------------------------------------------------
    #       Instance Functions
    # -----------------------------------------------------------------------
    # None
    
    
    