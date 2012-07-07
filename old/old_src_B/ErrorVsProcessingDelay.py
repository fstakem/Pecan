#!/usr/bin/env python
# encoding: utf-8
"""
ErrorVsProcessingDelay.py

Created by Fredrick Stakem on 2010-03-19.
Copyright (c) 2010 __Research__. All rights reserved.
"""

import Simulator as sim
import pdb
import numpy
import scipy
import scipy.signal
import pylab
import time
import math
from enum import Enum

# Globals
InterpolationType = Enum( 'Time', 'Distance' )

# Filesystem paramters
dataRoot = "/Users/fstakem/Data/Movements_5_1_08/"
root = "/Users/fstakem/Research/OptimalFiltering/"
logDir = root + "code/log/"
outputDir = root + "code/output/"
movement = "Stacking"
simulations = range(1,6)
inputFiles = []
for i in simulations:
	inputFile = dataRoot + movement + "/Simulation" + str(i) + "/positionLog.txt"
	inputFiles.append(inputFile)
	
# Test parameters
samplingInterval = 10
predictionInterval = 100
drThreshold = .02
#farThresholds = range(60,210,10)
#closeThreshold = 60
farThresholds = range(20,210,10)
closeThreshold = 20
snapLimit = 0.9
interpolationType = InterpolationType.Time
heartbeat = 500
delay = 100
jitter = 20
packetLoss = 0

# Filter parameters
samplingFreq = 100
snapNumTaps = range(4,42,2)
convergeNumTaps = range(0,38,2)
#snapNumTaps = range(12,42,2)
#convergeNumTaps = range(0,30,2)
bands = [0.0, 1, 2, 50.0]
weights = [1, 0]

# Simulate the transmission and part of the reconstruction
startTimeTotal = time.time()
testData = []
staticJumps = [ [ [], [], [] ], 
			    [ [], [], [] ],
				[ [], [], [] ],
			    [ [], [], [] ] ]
for inputFile in inputFiles:
	simulationData = sim.simulateTransmission(inputFile, logDir, predictionInterval, 
											  samplingInterval, heartbeat, drThreshold, 
											  delay, jitter, packetLoss)
	simNumber = inputFile.split('/')[-2][-1]
	snapReconstruction = sim.simulateSnapRecon(simulationData[4], logDir, simNumber, samplingInterval)[0]
	snapLimitReconstruction = sim.simulateSnapLimitRecon(simulationData[4], logDir, simNumber, samplingInterval,
														 interpolationType, closeThreshold, snapLimit)[0]
	convergedReconstruction = sim.simulateLinearConvergence(simulationData[4], logDir, simNumber, samplingInterval,
						  			                 		interpolationType, closeThreshold)[0]
	testData.append([simulationData[0], simulationData[4], snapReconstruction, 
					 snapLimitReconstruction, convergedReconstruction])
	
	# Find intra-sample jump
	threshold = 0
	spacing = 1
	jumpDataSets = []
	jumpDataSets.append( sim.findDistanceBetweenSamples(simulationData[0], threshold, spacing) )
	jumpDataSets.append( sim.findDistanceBetweenSamples(snapReconstruction, threshold, spacing) )
	jumpDataSets.append( sim.findDistanceBetweenSamples(snapLimitReconstruction, threshold, spacing) )
	jumpDataSets.append( sim.findDistanceBetweenSamples(convergedReconstruction, threshold, spacing) )
	for i, data in enumerate(jumpDataSets):
		mean, std, median = sim.calculateStats(data)
		staticJumps[i][0].append(mean)
		staticJumps[i][1].append(std)
		staticJumps[i][2].append(median)
	
# Simulate the rest of the reconstruction and calculate stats
distanceCurves = [ [ [], [], [] ], 
			       [ [], [], [] ],
				   [ [], [], [] ],
			       [ [], [], [] ] ]
jumpCurves = [ [ [], [], [] ], 
			   [ [], [], [] ],
			   [ [], [], [] ],
			   [ [], [], [] ] ]
for i in range(0, len(farThresholds)):
	farThreshold = farThresholds[i]
	snapTaps = snapNumTaps[i]
	convergeTaps = convergeNumTaps[i]
	
	# Parks-McClellan method
	snapCoefficients = scipy.signal.remez(snapTaps, bands, weights, Hz=samplingFreq)
	snapGain = 1.0 / sum(snapCoefficients)
	if convergeTaps != 0:
		convergeCoefficients = scipy.signal.remez(convergeTaps, bands, weights, Hz=samplingFreq)
		convergeGain = 1.0 / sum(convergeCoefficients)
	
	# Iterate all of the sample data
	distanceError = [ [ [], [], [] ], 
				      [ [], [], [] ],
					  [ [], [], [] ],
				      [ [], [], [] ] ]
	jump = 	[ [ [], [], [] ], 
			  [ [], [], [] ],
			  [ [], [], [] ],
			  [ [], [], [] ] ]
	for i, data in enumerate(testData):
		simulation = str(i+1)
		inputData = data[0]
		rxPackets = data[1]
		snapReconstruction = data[2]
		snapLimitReconstruction = data[3]
		convergedCloseData = data[4]
		# Simulate convergence
		convergedFarData = sim.simulateLinearConvergence(rxPackets, logDir, simulation, samplingInterval,
		  							  			         interpolationType, farThreshold)[0]
		
		# Simulate filtering
		snapFilteredData = sim.simulateFilterRecon(snapReconstruction, logDir, simulation, samplingInterval, 
										           snapCoefficients)[0]
		sim.amplifyData(snapFilteredData, snapGain)
		
		if convergeTaps != 0:
			convergedFilteredData = sim.simulateFilterRecon(convergedCloseData, logDir, simulation, samplingInterval, 
										                	convergeCoefficients)[0]
			sim.amplifyData(convergedFilteredData, convergeGain)
		else:
			convergedFilteredData = convergedCloseData
			
		if convergeTaps != 0:
			snapLimitFilteredData = sim.simulateFilterRecon(snapLimitReconstruction, logDir, simulation, samplingInterval, 
										                	convergeCoefficients)[0]
			sim.amplifyData(snapLimitFilteredData, convergeGain)
		else:
			snapLimitFilteredData = snapLimitReconstruction
		
		# Find the distance error
		errorDataSets = []
		errorDataSets.append( sim.findDistanceError(convergedFarData, inputData) )
		errorDataSets.append( sim.findDistanceError(snapFilteredData, inputData) )
		errorDataSets.append( sim.findDistanceError(snapLimitFilteredData, inputData) )
		errorDataSets.append( sim.findDistanceError(convergedFilteredData, inputData) )
		
		# Find intra-sample jump
		threshold = 0
		spacing = 1
		jumpDataSets = []
		jumpDataSets.append( sim.findDistanceBetweenSamples(convergedFarData, threshold, spacing) )
		jumpDataSets.append( sim.findDistanceBetweenSamples(snapFilteredData, threshold, spacing) )
		jumpDataSets.append( sim.findDistanceBetweenSamples(snapLimitFilteredData, threshold, spacing) )
		jumpDataSets.append( sim.findDistanceBetweenSamples(convergedFilteredData, threshold, spacing) )
		
		for i, v in enumerate(errorDataSets):
			errorData = errorDataSets[i]
			mean, std, median = sim.calculateStats(errorData)
			distanceError[i][0].append(mean)
			distanceError[i][1].append(std)
			distanceError[i][2].append(median)
			
			jumpData = jumpDataSets[i]
			mean, std, median = sim.calculateStats(jumpData)
			jump[i][0].append(mean)
			jump[i][1].append(std)
			jump[i][2].append(median)
		
	for i in range(0, len(distanceError)):
		for j in range(0,3):
			errorTemp = numpy.array(distanceError[i][j])
			jumpTemp = numpy.array(jump[i][j])
			distanceCurves[i][j].append( errorTemp.mean() )
			jumpCurves[i][j].append( jumpTemp.mean() )

# Create output
initialTime, initialX, initialY, initialZ = sim.splitData(testData[0])
snapTime, snapX, snapY, snapZ = sim.splitData(testData[2])
	
# Plot the output
pDelay = farThresholds
typePlot = 0
pylab.figure(1)
pylab.plot(pDelay, distanceCurves[0][0], 'k-', pDelay, distanceCurves[1][0], 'g-', 
		   pDelay, distanceCurves[2][0], 'r-', pDelay, distanceCurves[3][0], 'b-')
pylab.figure(2)
pylab.plot(pDelay, jumpCurves[0][0], 'k-', pDelay, jumpCurves[1][0], 'g-', 
		   pDelay, jumpCurves[2][0], 'r-', pDelay, jumpCurves[3][0], 'b-')
pylab.figure(3)
pylab.plot(pDelay, distanceCurves[0][2], 'k-', pDelay, distanceCurves[1][2], 'g-', 
		   pDelay, distanceCurves[2][2], 'r-', pDelay, distanceCurves[3][2], 'b-')
pylab.figure(4)
pylab.plot(pDelay, jumpCurves[0][2], 'k-', pDelay, jumpCurves[1][2], 'g-', 
		   pDelay, jumpCurves[2][2], 'r-', pDelay, jumpCurves[3][2], 'b-')
pylab.figure(5)
pylab.plot(initialTime, initialX, 'k-', initialTime, initialX, 'g--')
pylab.figure(6)
pylab.plot(snapTime, snapX, 'k-', snapTime, snapX, 'g-')
pylab.show()
