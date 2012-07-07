#  .---------------------------------------------------------------------------.
#  |                                                                           |
#  |               S N A P   L I M I T   R E C O N S T R U C T O R             |
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

class SnapLimitReconstructor(object):
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self):
        # Data
        self.rawSignal = []
        self.reconstructedSignal = []
        # Algorithm parameters
        self.samplingInterval = 10
        self.interpolationType = InterpolationType.Time
        self.threshold = 60
        self.heartbeatRate = 500
        self.snapLimit = 0.5
    
    def getReconstructedSignal(self, rawSignal=[], samplingInterval=10,
                               interpolationType=InterpolationType.Time,
							   threshold=60, heartbeatRate=500, snapLimit=0.5):
        if isinstance( rawSignal, list ):
            self.rawSignal = rawSignal
        if isinstance( samplingInterval, int ) and samplingInterval > 0:
            self.samplingInterval = samplingInterval
        if isinstance( interpolationType, Enum ):
            self.interpolationType = interpolationType
        if (isinstance( threshold, float ) and threshold > 0) or \
           (isinstance(threshold, int ) and threshold > 0):
            self.threshold = threshold
        if isinstance( heartbeatRate, int ) and heartbeatRate > 0:
            self.heartbeatRate = heartbeatRate
        if isinstance( snapLimit, float ) and snapLimit > 0:
            self.snapLimit = snapLimit
        
        self.pullDataFromPackets()
        self.executeAlgorithm()
        
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
		self.reconstructedSignal.append( self.findFirstSample() )
		reconstructionTime = self.reconstructedSignal[0].time + self.samplingInterval
		interpolationSample = PredictionSample(self.reconstructedSignal[0], 
		     								   self.rawSignal[0].velocity)
		targetSample = None
		
		for index, predictionSample in enumerate(self.rawSignal[1:]):
			currentTime = predictionSample.sample.time
			if currentTime < reconstructionTime:
				targetSample = None
				interpolationSample = predictionSample
			elif currentTime == reconstructionTime:
				estimatedSample = self.estimateSample(interpolationSample, 
				     								  reconstructionTime)
				targetSample = self.findTarget(predictionSample)
				interpolationSample = self.findSnapSample(predictionSample, estimatedSample, targetSample)
				self.reconstructedSignal.append(deepcopy(interpolationSample.sample))
				reconstructionTime += self.samplingInterval
			elif currentTime > reconstructionTime:
				while currentTime > reconstructionTime:
					if targetSample != None and reconstructionTime >= targetSample.sample.time:
						interpolationSample = targetSample
						targetSample = None
					
					estimatedSample = self.estimateSample(interpolationSample, 
					     								  reconstructionTime)
					self.reconstructedSignal.append(deepcopy(estimatedSample.sample))
					reconstructionTime += self.samplingInterval
					
				if currentTime < reconstructionTime:
					targetSample = None
					interpolationSample = predictionSample
				elif currentTime == reconstructionTime:
					estimatedSample = self.estimateSample(interpolationSample, 
					     								  reconstructionTime)
					targetSample = self.findTarget(predictionSample)
					interpolationSample = self.findSnapSample(predictionSample, estimatedSample, targetSample)
					self.reconstructedSignal.append(deepcopy(interpolationSample.sample))
					reconstructionTime += self.samplingInterval
				
    def findFirstSample(self):
        timeDiff = self.rawSignal[0].sample.time % self.samplingInterval
        
        if timeDiff == 0:
            return deepcopy(self.rawSignal[0].sample)
        else:
            change = self.samplingInterval - timeDiff
            newSample = Sample()
            newSample.time = self.rawSignal[0].sample.time + change
            newSample.position = deepcopy(self.rawSignal[0].sample.position)
            return newSample
    
    def findTarget(self, predictionSample):
        if self.interpolationType == InterpolationType.Time:
            return self.findTargetForTimeThreshold(predictionSample)
        elif self.interpolationType == Interpolation.Distance:
			return self.findTargetForDistanceThreshold(predictionSample)
	
    def findTargetForTimeThreshold(self, predictionSample):
		time = min(self.threshold, self.heartbeatRate)
		targetSample = self.estimateSample(predictionSample, predictionSample.sample.time + time)
		return targetSample
	
    def findTargetForDistanceThreshold(self, predictionSample):
        distance = 0
        targetSample = None
        time = predictionSample.sample.time
        timeDiff = 0

        while distance < self.threshold and timeDiff < self.heartbeatRate:
            time += self.samplingInterval
            timeDiff = time - predictionSample.sample.time
            targetSample = self.estimateSample(predictionSample, time)
            distance = predictionSample.sample.position.distance(target.sample.position)

        return targetSample
	
    def findInterpolationSample(self, currentSample, targetSample):
		deltaPosition = targetSample.sample.position - \
		                currentSample.sample.position
		deltaTime = targetSample.sample.time - \
		            currentSample.sample.time
		invDeltaTimeVector = Vector( 1 / float(deltaTime), \
		                             1 / float(deltaTime), \
		                             1 / float(deltaTime))
		velocity = deltaPosition * invDeltaTimeVector

		interpolationSample = PredictionSample()
		interpolationSample.sample = deepcopy(currentSample.sample)
		interpolationSample.velocity = velocity
		return interpolationSample
		
    def findSnapSample(self, currentSample, estimatedSample, targetSample):
		deltaPosition = targetSample.sample.position - \
		                currentSample.sample.position
		deltaPosition.x *= self.snapLimit
		deltaPosition.y *= self.snapLimit
		deltaPosition.z *= self.snapLimit
		snapPosition = currentSample.sample.position + deltaPosition
		
		deltaPosition = targetSample.sample.position - snapPosition
		deltaTime = targetSample.sample.time - \
		            currentSample.sample.time
		invDeltaTimeVector = Vector( 1 / float(deltaTime), \
		                             1 / float(deltaTime), \
		                             1 / float(deltaTime))
		velocity = deltaPosition * invDeltaTimeVector
		
		snapSample = PredictionSample()
		snapSample.sample = Sample(currentSample.sample.time, snapPosition)
		snapSample.velocity = velocity
		return snapSample
		
    def estimateSample(self, interpolationSample, time):
		estimatedSample = PredictionSample()
		estimatedSample.sample.time = time
		estimatedSample.sample.position = self.calculatePosition(interpolationSample, time)
		estimatedSample.velocity = deepcopy(interpolationSample.velocity)
		return estimatedSample
	
    def calculatePosition(self, interpolationSample, time):
		deltaTime = time - interpolationSample.sample.time
		if deltaTime < 0:
			print "Error at: " + str(interpolationSample.sample.time) + "  " + str(time)
			return deepcopy(interpolationSample.sample.position)
		elif deltaTime == 0:
			return deepcopy(interpolationSample.sample.position)
		else:
			deltaTimeVector = Vector(deltaTime, deltaTime, deltaTime)
			deltaPosition = interpolationSample.velocity * deltaTimeVector
			estimatedPosition = interpolationSample.sample.position + deltaPosition
			return estimatedPosition
		
		
		
