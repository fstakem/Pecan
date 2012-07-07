#  .---------------------------------------------------------------------------.
#  |                                                                           |
#  |  V A R I A B L E   I N T E R P O L A T I O N   R E C O N S T R U C T O R  |
#  |                                                                           |
#  '---------------------------------------------------------------------------'

import pdb
import inspect
from copy import *
from math import *
from enum import Enum
from Globals import *
from Vector import Vector
from Sample import Sample
from PredictionSample import PredictionSample

AlgorithmType = Enum( 'Fixed', 'Adaptive' )

class VarIntReconstructor(object):
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       P U B L I C   F U N C T I O N S
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	def __init__(self):
        # Data
		self.rawSignal = []
		self.reconstructedSignal = []
        # Algorithm parameters
		self.samplingInterval = 10
		self.shortConvergenceTime = 100
		self.longConvergenceTime = 100
		self.convergenceLimit = 500
		self.logFile = ""
		
	def getReconstructedSignal(self, rawSignal=[], samplingInterval=10,
                               shortConvergenceTime=100,
							   longConvergenceTime=100,
							   convergenceLimit=500):
		if isinstance( rawSignal, list ):
			self.rawSignal = rawSignal
		if isinstance( samplingInterval, int ) and samplingInterval > 0:
			self.samplingInterval = samplingInterval
		if isinstance( shortConvergenceTime, int ) and shortConvergenceTime > 0:
			self.shortConvergenceTime = shortConvergenceTime
		if isinstance( longConvergenceTime, int ) and longConvergenceTime > 0:
			self.longConvergenceTime = longConvergenceTime
		if isinstance( convergenceLimit, int ) and convergenceLimit > 0:
			self.convergenceLimit = convergenceLimit
        
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
		extrapolationSamples = [ self.rawSignal[0] ]
		nextTimeToRecord = self.reconstructedSignal[0].time + 1
		
		tempRawSignal = self.rawSignal[1:]
		for index, predictionSample in enumerate(tempRawSignal):
			while predictionSample.sample.time > nextTimeToRecord:
				if len(extrapolationSamples) > 1 and \
				   nextTimeToRecord == extrapolationSamples[0].sample.time:
					self.reconstructedSignal.append( deepcopy(extrapolationSamples[0].sample) )
					extrapolationSamples.pop(0)
				else:
					estimatedSample = self.estSample(extrapolationSamples[0], nextTimeToRecord)
					self.reconstructedSignal.append( estimatedSample )
				
				nextTimeToRecord += 1
			
			# New DR sample so must calculate the new extrapolation vectors
			lastEstimatedSample = self.reconstructedSignal[-1]
			estimatedSample = self.estSample(extrapolationSamples[0], nextTimeToRecord)
			jumpVector = predictionSample.sample.position - estimatedSample.position
			newAngles = self.measureAngles(predictionSample)
			algorithms = self.findAlgorithms(jumpVector, newAngles)
			timeToEqualitys = self.findTimeToEquality(algorithms, jumpVector, newAngles)
			timeToTargets = self.findTimeToTargets(timeToEqualitys)
			targets = self.findTargets(predictionSample, timeToTargets)
			tempExtrapolationSamples = self.findExtrapolationSamples(lastEstimatedSample, targets)
			
			extrapolationSamples = self.mergeExtrapolationSamples(predictionSample, timeToTargets,
																  tempExtrapolationSamples)
															
			estimatedSample = self.estSample(extrapolationSamples[0], nextTimeToRecord)
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
			
	def measureAngles(self, predictionSample):
		angleThreshold = 1.0
		const = 180 / pi
		x = atan(abs(predictionSample.velocity.x)) * const
		y = atan(abs(predictionSample.velocity.y)) * const
		z = atan(abs(predictionSample.velocity.z)) * const
		
		return [x, y, z]
		
	def findAlgorithms(self, jumpVector, newAngles):
		algorithms = []
		jumps = [jumpVector.x, jumpVector.y, jumpVector.z]
		for i, jump in enumerate(jumps):
			newAngle = newAngles[i]
			
			if jump > 0.0:
				if newAngle < 0.0:
					algorithms.append(AlgorithmType.Adaptive)
				else:
					algorithms.append(AlgorithmType.Fixed)
			elif jump < 0.0:
				if newAngle > 0.0:
					algorithms.append(AlgorithmType.Adaptive)
				else:
					algorithms.append(AlgorithmType.Fixed)
			else:
				algorithms.append(AlgorithmType.Fixed)
							
		return algorithms
	
	def findTimeToEquality(self, algorithms, jumpVector, angles):
		timeToEquality = []
		jumps = [jumpVector.x, jumpVector.y, jumpVector.z]
		for i, algorithm in enumerate(algorithms):
			if algorithm == AlgorithmType.Fixed:
				timeToEquality.append(0)
			elif algorithm == AlgorithmType.Adaptive:
				if angles[i] != 0:
					distance = abs(jumps[i]) / tan(abs(angles[i]) * pi / 180)
					timeToEquality.append( int(distance) )
				else:
					timeToEquality.append(0)
				
		return timeToEquality
		
	def findTimeToTargets(self, timeToEquality):
		timeToTargets = []
		for time in timeToEquality:
			if time == 0:
				timeToTargets.append(self.shortConvergenceTime)
			else:
				timeMin = min(self.convergenceLimit, time + self.longConvergenceTime)
				timeToTargets.append(timeMin)
				
		return timeToTargets
		
	def findTargets(self, predictionSample, timeToTargets):
		targets = []
		for i, timeToTarget in enumerate(timeToTargets):
			targetTime = predictionSample.sample.time + timeToTarget
			targets.append( self.estSample(predictionSample, targetTime) )
			
		return targets
		
	def findExtrapolationSamples(self, currentSample, targets):
		extrapolationSamples = []
		for i, target in enumerate(targets):
			extrapolationSamples.append( self.calcExtrapolationSample(currentSample, 
																	  target) )
		
		return extrapolationSamples
		
	def mergeExtrapolationSamples(self, predictionSample, timeToTargets, extrapolationSamples):
		newExtrapolationSamples = []
		newExtrapolationSample = PredictionSample(extrapolationSamples[0])
		newExtrapolationSample.velocity.y = extrapolationSamples[1].velocity.y
		newExtrapolationSample.velocity.z = extrapolationSamples[2].velocity.z
		newExtrapolationSamples.append(newExtrapolationSample)
		
		# Find the order of the samples
		times = [ (timeToTargets[0], '0'), 
				  (timeToTargets[1], '1'), 
				  (timeToTargets[2], '2') ]
		times.sort()
		
		for time in times:
			targetTime = time[0]
			index = time[1]
			newSample = self.estSample(newExtrapolationSamples[-1], 
						   			   newExtrapolationSamples[0].sample.time + targetTime)
			newVelocity = deepcopy( newExtrapolationSamples[-1].velocity )
			
			if index == '0':
				newVelocity.x = predictionSample.velocity.x
			elif index == '1':
				newVelocity.y = predictionSample.velocity.y
			elif index == '2':
				newVelocity.z = predictionSample.velocity.z
				
			newExtrapolationSample = PredictionSample(newSample, newVelocity)
			newExtrapolationSamples.append(newExtrapolationSample)
	
		return newExtrapolationSamples
		
				
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
		
		