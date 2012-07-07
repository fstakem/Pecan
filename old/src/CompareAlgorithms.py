#!/usr/bin/env python
# encoding: utf-8
"""
CompareAlgorithms.py

Created by Fredrick Stakem on 2010-03-31.
Copyright (c) 2010 __Research__. All rights reserved.
"""

# Import libraries
#------------------------------------------------------------------------------
import Simulator as s
import pdb
import numpy
import scipy
import scipy.signal
import pylab
import time
import math
from enum import Enum
from Globals import *

# Filesystem paramters
#------------------------------------------------------------------------------
dataRoot = "/Users/fstakem/Data/Movements_5_1_08/"
root = "/Users/fstakem/Research/OptimalFiltering/"
logDir = root + "code/log/"
outputDir = root + "code/output/"
movement = "Stacking"
# TODO -> increase the number of simulations
simulations = range(1,2)
inputFiles = []
for i in simulations:
    inputFile = dataRoot + movement + "/Simulation" + str(i) + \
				"/positionLog.txt"
    inputFiles.append(inputFile)

# Simulation parameters
#------------------------------------------------------------------------------
simulateFiltering = False

# Transmission parameters
#------------------------------------------------------------------------------
predictionInterval = 100
samplingInterval = 10
heartbeat = 500
drThreshold = 0.02
convergenceType = InterpolationType.Time

# Network parameters
#------------------------------------------------------------------------------
delay = 100
jitter = 20
packetLoss = 0

# Reconstruction parameters
#------------------------------------------------------------------------------
convergenceTimes = range(10,30,10)
relativeSnapLimit = 0.5
absoluteSnapLimit = 0.002

# Filter parameters
#------------------------------------------------------------------------------
samplingFreq = int(1e3/samplingInterval)
taps = 10
bands = [0.0, 1, 2, 50.0]
weights = [1, 0]
coefficients = scipy.signal.remez(taps, bands, weights, Hz=samplingFreq)
gain = 1.0 / sum(coefficients)

# Calculation parameters
#------------------------------------------------------------------------------
jumpThreshold = 0
jumpSpacing = 1

# Plotting parameters
#------------------------------------------------------------------------------
plotDistance = True
plotJump = True
plotMean = True
plotMedian = True

# Create the output data structures
#------------------------------------------------------------------------------
outputData = []
inputStats = None
outputStats = []
algorithms = 3
files = len(inputFiles)
for i in range(0,algorithms):
	outputData.append([])
	outputStats.append([])
	
	for convergenceTime in convergenceTimes:
		outputData[-1].append([])
		outputStats[-1].append([])

# Simulate the transmission of the data
#------------------------------------------------------------------------------
startTimeTotal = time.time()
transmittedData = []
for inputFile in inputFiles:
	simNumber = inputFile.split('/')[-2][-1]
	print "Simulating the transmission for simulation: " + str(simNumber)

	data = s.transmitData(inputFile, logDir, predictionInterval,
						  samplingInterval, heartbeat, drThreshold,
						  delay, jitter, packetLoss)
	snapData = s.snapReconstructData(data[5], 
									 logDir, 
									 simNumber, 
									 samplingInterval)[0]
	filteredData = 	s.filterData(snapData, 
								 logDir, 
								 simNumber, 
							     samplingInterval, 
								 coefficients)[0]
	filteredData = s.amplifyData(filteredData, gain)
	
	data.append(snapData)
	data.append(filteredData)
	transmittedData.append(data)

print "Total time spent simulating the transmission: " + str(time.time() - \
															 startTimeTotal)
print
	
# Simulate the reconstruction of the data
#------------------------------------------------------------------------------
startTimeRecon = time.time()
for i, convergenceTime in enumerate(convergenceTimes):
	print "Simulating convergence time: " + str(convergenceTime)
	startTimeConverge = time.time()
	
	for j, data in enumerate(transmittedData):
		print "\tSimulating data set: " + str(j+1)
		simNumber = str(j+1)
		rawInputData = data[0]
		filteredInputData = data[1]
		predictedData = data[2]
		drTxPackets = data[3]
		drRxPackets = data[4]
		drRxFilteredPackets = data[5]
		snapData = data[6]
		inputFilteredData = data[7]
		
		convergenceData = s.convergeData(drRxFilteredPackets, 
										 logDir, 
										 simNumber, 
										 samplingInterval,
		  			     				 convergenceType, 
										 convergenceTime)[0]
		if not simulateFiltering:						
			outputData[0][i].append(convergenceData)
		else:
			filteredData = 	s.filterData(convergenceData, 
										 logDir, 
										 simNumber, 
									     samplingInterval, 
										 coefficients)[0]
			filteredData = s.amplifyData(filteredData, gain)
			outputData[0][i].append(filteredData)
		
		relativeSnapData = s.snapLimitReconstructData(drRxFilteredPackets,
													  logDir,
													  simNumber,
													  samplingInterval,
										              convergenceType,
													  SnapLimitType.Relative,
													  convergenceTime,
										              relativeSnapLimit)[0]
		if not simulateFiltering:
			outputData[1][i].append(relativeSnapData)
		else:
			filteredData = 	s.filterData(relativeSnapData, 
										 logDir, 
										 simNumber, 
									     samplingInterval, 
										 coefficients)[0]
			filteredData = s.amplifyData(filteredData, gain)
			outputData[1][i].append(filteredData)
		
		absoluteSnapData = s.snapLimitReconstructData(drRxFilteredPackets,
													  logDir,
													  simNumber,
													  samplingInterval,
										              convergenceType,
													  SnapLimitType.Absolute,
													  convergenceTime,
										              absoluteSnapLimit)[0]
		if not simulateFiltering:
			outputData[2][i].append(absoluteSnapData)
		else:
			filteredData = 	s.filterData(absoluteSnapData, 
										 logDir, 
										 simNumber, 
									     samplingInterval, 
										 coefficients)[0]
			filteredData = s.amplifyData(filteredData, gain)
			outputData[2][i].append(filteredData)
	
	print "\tSimulation time for all of the data sets: " + \
		  str(time.time() - startTimeConverge)
print "Simulation time for all of the convergence values sets: " + \
      str(time.time() - startTimeRecon)		
		
# Calculate the results and statistics
#------------------------------------------------------------------------------
inputJumps = []
snapErrors = []
snapJumps = []
filteredErrors = []
filteredJumps = []

for inputData in transmittedData:
	initialData = inputData[1]
	snapData = inputData[6]
	filteredData = inputData[7]

	inputJump = s.findDistanceBetweenSamples(initialData,
											 jumpThreshold,
											 jumpSpacing)
	inputJumps.append( s.calculateStats(inputJump) )
	
	snapJump = s.findDistanceBetweenSamples(snapData,
											jumpThreshold,
											jumpSpacing)
	snapJumps.append( s.calculateStats(snapJump) )
	
	filteredJump = s.findDistanceBetweenSamples(filteredData,
											    jumpThreshold,
											    jumpSpacing)
	filteredJumps.append( s.calculateStats(filteredJump) )
	
	snapError = s.findDistanceError(initialData, snapData)
	snapErrors.append( s.calculateStats(snapError) )
	
	filteredError = s.findDistanceError(initialData, filteredData)
	filteredErrors.append( s.calculateStats(filteredError) )

inputStats = [ s.aggregateStats(inputJumps), s.aggregateStats(snapErrors), 
			   s.aggregateStats(snapJumps), s.aggregateStats(filteredErrors),
			   s.aggregateStats(filteredJumps)]

for i, algorithm in enumerate(range(0,3)):
	for j, convergenceTime in enumerate(convergenceTimes):
	    distanceErrors = []
	    distanceJumps = []
	    stats = []
	    for k, reconstructedData in enumerate(outputData[i][j]):
	        inputData = transmittedData[k][1]
	        distanceError = s.findDistanceError(inputData,
												reconstructedData)
	        distanceErrors.append( s.calculateStats(distanceError) )

	        distanceJump = s.findDistanceBetweenSamples(reconstructedData,
														jumpThreshold,
														jumpSpacing)
	        distanceJumps.append( s.calculateStats(distanceJump) )

	    outputStats[i][j].append( s.aggregateStats(distanceErrors) )
	    outputStats[i][j].append( s.aggregateStats(distanceJumps) )

# Create the curves to be plotted
#------------------------------------------------------------------------------
convergenceErrorMean = []
convergenceErrorMedian = []
convergenceJumpMean = []
convergenceJumpMedian = []
relativeErrorMean = []
relativeErrorMedian = []
relativeJumpMean = []
relativeJumpMedian = []
absoluteErrorMean = []
absoluteErrorMedian = []
absoluteJumpMean = []
absoluteJumpMedian = []

for j, convergenceTime in enumerate(convergenceTimes):
	convergenceErrorMean.append( outputStats[0][j][0][0] )
	convergenceErrorMedian.append( outputStats[0][j][0][2] )
	convergenceJumpMean.append( outputStats[0][j][1][0] )
	convergenceJumpMedian.append( outputStats[0][j][1][2] )
	
	relativeErrorMean.append( outputStats[1][j][0][0] )
	relativeErrorMedian.append( outputStats[1][j][0][2] )
	relativeJumpMean.append( outputStats[1][j][1][0] )
	relativeJumpMedian.append( outputStats[1][j][1][2] )
	
	absoluteErrorMean.append( outputStats[2][j][0][0] )
	absoluteErrorMedian.append( outputStats[2][j][0][2])
	absoluteJumpMean.append( outputStats[2][j][1][0] )
	absoluteJumpMedian.append( outputStats[2][j][1][2] )
	
# Output the data
#------------------------------------------------------------------------------
curves = [convergenceErrorMean, convergenceErrorMedian, 
		  convergenceJumpMean, convergenceJumpMedian, 
		  relativeErrorMean, relativeErrorMedian, 
		  relativeJumpMean, relativeJumpMedian,
		  absoluteErrorMean, absoluteErrorMedian, 
		  absoluteJumpMean, absoluteJumpMedian]

print				
strOutput = ""
for i, convergenceTime in enumerate(convergenceTimes):
	strOutput = str(convergenceTime)
	for data in curves:
		strOutput += "\t" + str(data[i])
	print strOutput
print
	
# Plot the statistics
#------------------------------------------------------------------------------
figure = 1

if plotDistance == True:
	if plotMean == True:
		pylab.figure(figure)
		figure += 1
		pylab.plot(convergenceTimes, convergenceErrorMean, 'k-')
		pylab.plot(convergenceTimes, relativeErrorMean, 'r-')
		pylab.plot(convergenceTimes, absoluteErrorMean, 'g-')

	if plotMedian == True:
		pylab.figure(figure)
		figure += 1
		pylab.plot(convergenceTimes, convergenceErrorMedian, 'k-')
		pylab.plot(convergenceTimes, relativeErrorMedian, 'r-')
		pylab.plot(convergenceTimes, absoluteErrorMedian, 'g-')

if plotJump == True:
	if plotMean == True:
		pylab.figure(figure)
		figure += 1
		pylab.plot(convergenceTimes, convergenceJumpMean, 'k-')
		pylab.plot(convergenceTimes, relativeJumpMean, 'r-')
		pylab.plot(convergenceTimes, absoluteJumpMean, 'g-')

	if plotMedian == True:
		pylab.figure(figure)
		figure += 1
		pylab.plot(convergenceTimes, convergenceJumpMedian, 'k-')
		pylab.plot(convergenceTimes, relativeJumpMedian, 'r-')
		pylab.plot(convergenceTimes, absoluteJumpMedian, 'g-')

pylab.show()



