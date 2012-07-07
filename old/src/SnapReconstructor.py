#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |                      S N A P   R E C O N S T R U C T O R                     |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

from copy import *
from Vector import Vector
from Sample import Sample
from PredictionSample import PredictionSample

class SnapReconstructor(object):
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self):
        # Data
        self.rawSignal = []
        self.reconstructedSignal = []
        # Algorithm parameters
        self.samplingInterval = 10
    
    def getReconstructedSignal(self, rawSignal=[], samplingInterval=10):
        if isinstance( rawSignal, list ):
            self.rawSignal = rawSignal
        if isinstance( samplingInterval, int ) and samplingInterval > 0:
            self.samplingInterval = samplingInterval
        
        self.pullDataFromPackets()
        self.executeAlgorithm()
        self.resampleData()
        
        return self.reconstructedSignal
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P R I V A T E   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def pullDataFromPackets(self):
		temp = []
		for packet in self.rawSignal:
			temp.append(packet.predictionSample)
		
		self.rawSignal = temp
    
    def executeAlgorithm(self):
		self.reconstructedSignal = []
		self.reconstructedSignal.append( deepcopy(self.rawSignal[0].sample) )
		nextTimeToRecord = self.reconstructedSignal[0].time + 1
		
		tempRawSignal = self.rawSignal[1:]
		for index, predictionSample in enumerate(tempRawSignal):
			lastReceivedSample = tempRawSignal[index-1]
			while predictionSample.sample.time > nextTimeToRecord:
				estimatedSample = self.estSample(lastReceivedSample, nextTimeToRecord)
				self.reconstructedSignal.append( estimatedSample )
				nextTimeToRecord += 1
				
			self.reconstructedSignal.append( deepcopy(predictionSample.sample) )
			nextTimeToRecord += 1
	
    def estSample(self, predictionSample, time):
        deltaTime = time - predictionSample.sample.time
        if time < 0:
            print "Error: must estimate a position in the future"
            return deepcopy( predictionSample.sample )
        
        deltaTimeVector = Vector(deltaTime, deltaTime, deltaTime)
        deltaPosition = predictionSample.velocity * deltaTimeVector
        estimatedPosition = predictionSample.sample.position + deltaPosition
        estimatedSample = Sample(time, estimatedPosition)

        return estimatedSample

    def resampleData(self):
		temp = []
		for sample in self.reconstructedSignal:
			if (sample.time % self.samplingInterval) == 0:
				temp.append(sample)
		
		self.reconstructedSignal = temp
		
                       
    
    