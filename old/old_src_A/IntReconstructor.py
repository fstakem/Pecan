#  .---------------------------------------------------------------------------.
#  |                                                                           |
#  |           I N T E R P O L A T I O N   R E C O N S T R U C T O R           |
#  |                                                                           |
#  '---------------------------------------------------------------------------'

import pdb
import inspect
from copy import *
from enum import Enum
from Globals import *
from Vector import Vector
from Sample import Sample
from PredictionSample import PredictionSample

class IntReconstructor(object):
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self):
        # Data
        self.rawSignal = []
        self.reconstructedSignal = []
        # Algorithm parameters
        self.samplingInterval = 10
        self.convergenceTime = 100
        self.heartbeatRate = 500
    
    def getReconstructedSignal(self, rawSignal=[], samplingInterval=10,
                               interpolationType=InterpolationType.Time,
							   convergenceTime=100, heartbeatRate=500):
        if isinstance( rawSignal, list ):
            self.rawSignal = rawSignal
        if isinstance( samplingInterval, int ) and samplingInterval > 0:
            self.samplingInterval = samplingInterval
        if (isinstance( convergenceTime, float ) and convergenceTime > 0) or \
           (isinstance(convergenceTime, int ) and convergenceTime > 0):
            self.convergenceTime = convergenceTime
        if isinstance( heartbeatRate, int ) and heartbeatRate > 0:
            self.heartbeatRate = heartbeatRate
        
        self.pullDataFromPackets()
        self.executeAlgorithm()
        self.resampleData()
        
        return self.reconstructedSignal
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P R I V A T E   F U N C T I O N S
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def pullDataFromPackets(self):
		temp = []
		for packet in self.rawSignal:
			temp.append(packet.predictionSample)
		
		self.rawSignal = temp
    
    def executeAlgorithm(self):
		self.reconstructedSignal = []
		self.reconstructedSignal.append( deepcopy(self.rawSignal[0].sample) )
		extrapolationSample = self.rawSignal[0]
		futureExtrapolationSample = None
		nextTimeToRecord = self.reconstructedSignal[0].time + 1
		
		tempRawSignal = self.rawSignal[1:]
		for index, predictionSample in enumerate(tempRawSignal):
			while predictionSample.sample.time > nextTimeToRecord:
				if futureExtrapolationSample != None and \
				   futureExtrapolationSample.sample.time == nextTimeToRecord:
					extrapolationSample = futureExtrapolationSample
					futureExtrapolationSample = None
					self.reconstructedSignal.append( deepcopy(extrapolationSample.sample) )
				else:
					estimatedSample = self.estSample(extrapolationSample, nextTimeToRecord)
					self.reconstructedSignal.append( deepcopy(estimatedSample) )
				
				nextTimeToRecord += 1
			
			lastEstimatedSample = self.reconstructedSignal[-1]
			targetSample = self.calcTargetSample(predictionSample)
			extrapolationSample = self.calcExtrapolationSample(lastEstimatedSample, targetSample)
			futureExtrapolationSample = PredictionSample(targetSample, predictionSample.velocity)
			estimatedSample = self.estSample(extrapolationSample, nextTimeToRecord)
			self.reconstructedSignal.append( deepcopy(estimatedSample) )
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
    
    def calcTargetSample(self, predictionSample):
		time = min(self.convergenceTime, self.heartbeatRate)
		targetSample = self.estSample(predictionSample, predictionSample.sample.time + time)
		return targetSample
    
    def calcExtrapolationSample(self, currentSample, targetSample):
		deltaPosition = targetSample.position - currentSample.position
		deltaTime = targetSample.time - currentSample.time
		invDeltaTimeVector = Vector( 1 / float(deltaTime), \
		                             1 / float(deltaTime), \
		                             1 / float(deltaTime))
		velocity = deltaPosition * invDeltaTimeVector
		
		extrapolationSample = PredictionSample()
		extrapolationSample.sample = deepcopy(currentSample)
		extrapolationSample.velocity = velocity
		return extrapolationSample
    
    def resampleData(self):
        temp = []
        for sample in self.reconstructedSignal:
            if (sample.time % self.samplingInterval) == 0:
                temp.append(sample)
        
        self.reconstructedSignal = temp
		
		
		