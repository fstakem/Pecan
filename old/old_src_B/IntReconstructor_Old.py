#  .------------------------------------------------------------------------------.
#  |                                                                              |
#  |            I N T E R P O L A T I O N   R E C O N S T R U C T O R             |
#  |                                                                              |
#  '------------------------------------------------------------------------------'

from copy import *
from Vector import Vector
from Sample import Sample
from PredictionSample import PredictionSample

class IntReconstructor(object):
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self):
        # Data
        self.rawSignal = []
        self.reconstructedSignal = []
        # Algorithm parameters
        self.samplingInterval = 10
        self.distanceThreshold = 0.01
        self.heartbeatRate = 500
            
    def getReconstructedSignal(self, rawSignal=[], samplingInterval=10, \
                               distanceThreshold=0.01, heartbeatRate=500):
        if isinstance( rawSignal, list ):
            self.rawSignal = rawSignal
        if isinstance( samplingInterval, int ) and samplingInterval > 0:
            self.samplingInterval = samplingInterval
        if isinstance( distanceThreshold, float ) and distanceThreshold > 0:
            self.distanceThreshold = distanceThreshold
        if isinstance( heartbeatRate, int ) and heartbeatRate > 0:
            self.heartbeatRate = heartbeatRate
        
        self.pullDataFromPackets()
        self.executeAlgorithm()
        
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
        nextTimeToRecord = 0
        timeDiff = self.rawSignal[0].sample.time % self.samplingInterval
        if timeDiff == 0:
            self.reconstructedSignal.append( deepcopy(self.rawSignal[0].sample) )
            nextTimeToRecord = self.rawSignal[0].sample.time + \
                               self.samplingInterval
        else:
            change = self.samplingInterval - timeDiff
            newSample = Sample()
            newSample.time = self.rawSignal[0].sample.time + change
            newSample.position = deepcopy(self.rawSignal[0].sample.position)
            self.reconstructedSignal.append(newSample)
            nextTimeToRecord = newSample.time + self.samplingInterval
            
        interpolationSample = PredictionSample()
        interpolationSample.sample = self.reconstructedSignal[0]
        interpolationSample.velocity = self.rawSignal[0].velocity
        for index, predictionSample in enumerate(self.rawSignal):
            if predictionSample.sample.time == nextTimeToRecord:
                estimatedSample = self.calculateEstSample(interpolationSample, \
                                                          nextTimeToRecord)
                self.reconstructedSignal.append(estimatedSample)
                targetSample = self.findTarget(predictionSample)
                interpolationSample = self.findInterpolationSample(estimatedSample, \
                                                                   targetSample)
                nextTimeToRecord = nextTimeToRecord + self.samplingInterval
            elif predictionSample.sample.time > nextTimeToRecord:
                while predictionSample.sample.time > nextTimeToRecord:
                    estimatedSample = self.calculateEstSample(interpolationSample, \
                                                              nextTimeToRecord)
                    self.reconstructedSignal.append(estimatedSample)
                    nextTimeToRecord = nextTimeToRecord + self.samplingInterval
                    
                if predictionSample.sample.time == nextTimeToRecord:
                    estimatedSample = self.calculateEstSample(interpolationSample, \
                                                          nextTimeToRecord)
                    self.reconstructedSignal.append(estimatedSample)
                    targetSample = self.findTarget(predictionSample)
                    interpolationSample = self.findInterpolationSample(estimatedSample, \
                                                                       targetSample)
                    nextTimeToRecord = nextTimeToRecord + self.samplingInterval
                else:
                    targetSample = self.findTarget(predictionSample)
                    interpolationSample = self.findInterpolationSample(self.reconstructedSignal[-1], \
                                                                       targetSample)
            
    def findTarget(self, predictionSample):
        distance = 0
        estimatedSample = 0
        futureTime = predictionSample.sample.time
        timeDifference = 0
        
        while distance < self.distanceThreshold and timeDifference < self.heartbeatRate:
            futureTime += self.samplingInterval
            timeDifference = futureTime - predictionSample.sample.time
            estimatedSample = self.calculateEstSample(predictionSample, \
                                                      futureTime)
            
            distance = predictionSample.sample.position.distance(estimatedSample.position)
            
        return estimatedSample
                     
    def findInterpolationSample(self, currentSample, targetSample):
        deltaPosition = targetSample.position - \
                        currentSample.position
        deltaTime = targetSample.time - \
                    currentSample.time
        invDeltaTimeVector = Vector( 1 / float(deltaTime), \
                                     1 / float(deltaTime), \
                                     1 / float(deltaTime))
        velocity = deltaPosition * invDeltaTimeVector
        
        interpolationSample = PredictionSample()
        interpolationSample.sample = deepcopy(currentSample)
        interpolationSample.velocity = velocity
        return interpolationSample
    
    def calculateEstPosition(self, lastPredictionSample, currentTime):
        deltaTime = currentTime - lastPredictionSample.sample.time
        deltaTimeVector = Vector(deltaTime, deltaTime, deltaTime)
        deltaPosition = lastPredictionSample.velocity * deltaTimeVector
        estimatedPosition = lastPredictionSample.sample.position + deltaPosition
        return estimatedPosition
    
    def calculateEstSample(self, interpolationSample, currentTime):
        estimatedSample = Sample()
        estimatedSample.time = currentTime
        estimatedSample.position = self.calculateEstPosition(interpolationSample, currentTime)
        return estimatedSample

        
        
        