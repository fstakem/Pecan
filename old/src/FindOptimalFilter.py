#!/usr/bin/env python
# encoding: utf-8
"""
FindOptimalFilter.py

Created by Fredrick Stakem on 2010-03-29.
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
root = "/Users/fstakem/Research/PhD/2010_Research/OptimalFiltering/"
logDir = root + "code/log/"
outputDir = root + "code/output/"
movement = "Stacking"
simulations = range(1,2)
inputFiles = []
for i in simulations:
    inputFile = dataRoot + movement + "/Simulation" + str(i) + \
				"/positionLog.txt"
    inputFiles.append(inputFile)

# Transmission parameters
#------------------------------------------------------------------------------
predictionInterval = 100
samplingInterval = 10
heartbeat = 500
drThreshold = 0.02

# Network parameters
#------------------------------------------------------------------------------
delay = 100
jitter = 20
packetLoss = 0

# Filter parameters
#------------------------------------------------------------------------------
samplingFreq = int(1e3/samplingInterval)
numTaps = range(2,51,2)
bands = [0.0, 2, 3, 50.0]
#bands = [0.0, 1, 2, 50.0]
weights = [1, 0]
filterDelays = [(i/2) * samplingInterval for i in numTaps]

# Reconstruction parameters
#------------------------------------------------------------------------------
convergenceType = InterpolationType.Time
convergenceInterval = 100
snapLimit = 0.005

# Calculation parameters
#------------------------------------------------------------------------------
jumpThreshold = 0
jumpSpacing = 1

# Create the output data structures
#------------------------------------------------------------------------------
outputData = []
inputStats = None
outputStats = []
files = len(inputFiles)

for taps in numTaps:
	outputData.append([])
	outputStats.append([])
	
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
	transmittedData.append(data)

print "Total time spent simulating the transmission: " + str(time.time() - \
															 startTimeTotal)
print

# Simulate the reconstruction of the data
#------------------------------------------------------------------------------
# Simulate relative snap reconstruction
startTimeCon = time.time()
print "Simulating convergence reconstruction..."
for i, taps in enumerate(numTaps):
	print "\t\tSimulating filter with taps: " + str(taps)
	startTimeConverge = time.time()
	coefficients = scipy.signal.remez(taps, bands, weights, Hz=samplingFreq)
	gain = 1.0 / sum(coefficients)
	
	for j, data in enumerate(transmittedData):
		print "\t\t\tSimulating data set: " + str(j+1)
		rawInputData = data[0]
		filteredInputData = data[1]
		predictedData = data[2]
		drTxPackets = data[3]
		drRxPackets = data[4]
		drRxFilteredPackets = data[5]

		snapData = None
		
		if False:
			snapData = s.snapReconstructData(drRxFilteredPackets, logDir, 
										 	simNumber, samplingInterval)[0]
		else:
			snapData = s.snapLimitReconstructData(drRxFilteredPackets,
												  logDir,
												  simNumber,
												  samplingInterval,
											      convergenceType,
												  SnapLimitType.Absolute,
												  convergenceInterval,
											      snapLimit)[0]
		
		filteredData = 	s.filterData(snapData, logDir, simNumber, 
								     samplingInterval, coefficients)[0]
		filteredData = s.amplifyData(filteredData, gain)
		
		outputData[i].append(filteredData)

	print "\t\tSimulation time for all of the data sets: " + \
		  str(time.time() - startTimeConverge)
print "\t\tSimulation time for all of the filter values sets: " + \
      str(time.time() - startTimeCon)

# Calculate the results and statistics
#------------------------------------------------------------------------------
distanceJumps = []

for inputData in transmittedData:
	initialData = inputData[1]
	distanceJump = s.findDistanceBetweenSamples(initialData,
											    jumpThreshold,
											    jumpSpacing)
	distanceJumps.append( s.calculateStats(distanceJump) )

inputStats = [ s.aggregateStats(distanceJumps) ]

for i, taps in enumerate(outputData):
    distanceErrors = []
    distanceJumps = []
    stats = []
    for j, reconstructedData in enumerate(taps):
        inputData = transmittedData[j][1]
        distanceError = s.findDistanceError(inputData,
					reconstructedData)
        distanceErrors.append( s.calculateStats(distanceError) )

        distanceJump = s.findDistanceBetweenSamples(reconstructedData,
							jumpThreshold,
							jumpSpacing)
        distanceJumps.append( s.calculateStats(distanceJump) )

    outputStats[i].append( s.aggregateStats(distanceErrors) )
    outputStats[i].append( s.aggregateStats(distanceJumps) )

# Create the curves to be plotted
#------------------------------------------------------------------------------
errorMeans = []
errorStds = []
errorMedians = []
jumpMeans = []
jumpStds = []
jumpMedians = []

for i, taps in enumerate(numTaps):
	errorMeans.append(outputStats[i][0][0])
	errorStds.append(outputStats[i][0][1])
	errorMedians.append(outputStats[i][0][2])
	jumpMeans.append(outputStats[i][1][0])
	jumpStds.append(outputStats[i][1][1])
	jumpMedians.append(outputStats[i][1][2])
	
# Output the data
#------------------------------------------------------------------------------
curves = [errorMeans, errorStds, errorMedians, jumpMeans, jumpStds, jumpMedians]

print				
strOutput = ""
for i, taps in enumerate(numTaps):
	strOutput = str(taps)
	for data in curves:
		strOutput += "\t" + str(data[i])
	print strOutput
print

# Plot the statistics
#------------------------------------------------------------------------------
figure = 1
pylab.figure(figure)
figure += 1
pylab.plot(filterDelays, errorMeans)
pylab.plot(filterDelays, errorMedians)
pylab.figure(figure)
figure += 1
pylab.plot(filterDelays, jumpMeans)
pylab.plot(filterDelays, jumpMedians)

pylab.show()












