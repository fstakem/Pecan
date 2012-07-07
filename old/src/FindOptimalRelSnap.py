#!/usr/bin/env python
# encoding: utf-8
"""
FindOptimalAbSnap.py

Created by Fredrick Stakem on 2010-04-08.
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
drThreshold = 0.015

# Network parameters
#------------------------------------------------------------------------------
delay = 100	
jitter = 20
packetLoss = 0

# Reconstruction parameters
#------------------------------------------------------------------------------
convergenceTime = 100
snapLimits = scipy.linspace(.1, .9, 9)
convergenceType = InterpolationType.Time

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

for snapLimit in snapLimits:
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
for i, snapLimit in enumerate(snapLimits):
	print "\t\tSimulating convergence time: " + str(convergenceTime)
	startTimeConverge = time.time()
	
	for j, data in enumerate(transmittedData):
		print "\t\t\tSimulating data set: " + str(j+1)
		rawInputData = data[0]
		filteredInputData = data[1]
		predictedData = data[2]
		drTxPackets = data[3]
		drRxPackets = data[4]
		drRxFilteredPackets = data[5]

		relativeSnapData = s.snapLimitReconstructData(drRxFilteredPackets,
													  logDir,
													  simNumber,
													  samplingInterval,
										              convergenceType,
													  SnapLimitType.Relative,
													  convergenceTime,
										              snapLimit)[0]
		
		outputData[i].append(relativeSnapData)

	print "\t\tSimulation time for all of the data sets: " + \
		  str(time.time() - startTimeConverge)
print "\t\tSimulation time for all of the convergence values sets: " + \
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

for i, snapLimit in enumerate(outputData):
    distanceErrors = []
    distanceJumps = []
    stats = []
    for j, reconstructedData in enumerate(snapLimit):
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

for i, snapLimit in enumerate(snapLimits):
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
for i, snapLimit in enumerate(snapLimits):
	strOutput = str(snapLimit)
	for data in curves:
		strOutput += "\t" + str(data[i])
	print strOutput
print
