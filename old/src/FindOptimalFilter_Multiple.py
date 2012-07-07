#!/usr/bin/env python
# encoding: utf-8
"""
FindOptimalFilter.py

Created by Fredrick Stakem on 2010-04-11.
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
samplingInterval = 10
heartbeat = 500
interpolationType = InterpolationType.Time

# Transmission parameters
#------------------------------------------------------------------------------
predictionInterval = 100
drThreshold = 0.015

# Network parameters
#------------------------------------------------------------------------------
delay = 100
jitter = 20
packetLoss = 0

# Reconstruction parameters
#------------------------------------------------------------------------------
convergenceInterval = 100
snapLimitType = SnapLimitType.Absolute
#snapLimit = 0.002
snapLimit = 0.004

# Filter parameters
#------------------------------------------------------------------------------
samplingFreq = int(1e3/samplingInterval)
numTaps = range(2,41,6)
bands = [0.0, 1, 2, 50.0]
weights = [1, 0]
filterDelays = [(i/2) * samplingInterval for i in numTaps]

# Calculation parameters
#------------------------------------------------------------------------------
jumpThreshold = 0
jumpSpacing = 1

# Create the output data structures
#------------------------------------------------------------------------------
inputStats = None
outputSnapData = []
outputSnapStats = []
outputAbSnapData = []
outputAbSnapStats = []
outputConvData = []
outputConvStats = []
files = len(inputFiles)

for taps in numTaps:
	outputSnapData.append([])
	outputSnapStats.append([])
	outputAbSnapData.append([])
	outputAbSnapStats.append([])
	outputConvData.append([])
	outputConvStats.append([])
	
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
		simNumber = str(i) + "_" + str(j+1)
		rawInputData = data[0]
		filteredInputData = data[1]
		predictedData = data[2]
		drTxPackets = data[3]
		drRxPackets = data[4]
		drRxFilteredPackets = data[5]
		
		# Snap data
		snapData = s.snapReconstructData(drRxFilteredPackets, logDir, 
										 simNumber, samplingInterval)[0]
										
		filteredSnapData = 	s.filterData(snapData, logDir, simNumber, 
								         samplingInterval, coefficients)[0]
		filteredSnapData = s.amplifyData(filteredSnapData, gain)
		outputSnapData[i].append(filteredSnapData)

		# Snap clipped data
		abSnapData = s.snapLimitReconstructData(drRxFilteredPackets, logDir, simNumber, 
											    samplingInterval, interpolationType, 
											    snapLimitType, convergenceInterval, 
											    snapLimit)[0]
		
		filteredAbSnapData = 	s.filterData(abSnapData, logDir, simNumber, 
								             samplingInterval, coefficients)[0]
		filteredAbSnapData = s.amplifyData(filteredAbSnapData, gain)
		outputAbSnapData[i].append(filteredAbSnapData)
		
		# Converged data
		convData = s.convergeData(drRxFilteredPackets, logDir, simNumber, 
								  samplingInterval, interpolationType, 
								  convergenceInterval)[0]
								
		filteredConvData = 	s.filterData(convData, logDir, simNumber, 
								         samplingInterval, coefficients)[0]
		filteredConvData = s.amplifyData(filteredConvData, gain)
		outputConvData[i].append(filteredConvData)
		
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

for i, taps in enumerate(outputSnapData):
    errors = []
    jumps = []
    for j, data in enumerate(taps):
        inputData = transmittedData[j][1]
		
        error = s.findDistanceError(inputData, data)
        errors.append( s.calculateStats(error) )

        jump = s.findDistanceBetweenSamples(data,
											jumpThreshold,
											jumpSpacing)
        jumps.append( s.calculateStats(jump) )

    outputSnapStats[i].append( s.aggregateStats(errors) )
    outputSnapStats[i].append( s.aggregateStats(jumps) )

for i, taps in enumerate(outputAbSnapData):
    errors = []
    jumps = []
    for j, data in enumerate(taps):
        inputData = transmittedData[j][1]

        error = s.findDistanceError(inputData, data)
        errors.append( s.calculateStats(error) )

        jump = s.findDistanceBetweenSamples(data,
											jumpThreshold,
											jumpSpacing)
        jumps.append( s.calculateStats(jump) )

    outputAbSnapStats[i].append( s.aggregateStats(errors) )
    outputAbSnapStats[i].append( s.aggregateStats(jumps) )

for i, taps in enumerate(outputConvData):
    errors = []
    jumps = []
    for j, data in enumerate(taps):
        inputData = transmittedData[j][1]

        error = s.findDistanceError(inputData, data)
        errors.append( s.calculateStats(error) )

        jump = s.findDistanceBetweenSamples(data,
											jumpThreshold,
											jumpSpacing)
        jumps.append( s.calculateStats(jump) )

    outputConvStats[i].append( s.aggregateStats(errors) )
    outputConvStats[i].append( s.aggregateStats(jumps) )

# Create the curves to be plotted
#------------------------------------------------------------------------------
snapErrorMeans = []
snapErrorStds = []
snapErrorMedians = []
snapJumpMeans = []
snapJumpStds = []
snapJumpMedians = []

abSnapErrorMeans = []
abSnapErrorStds = []
abSnapErrorMedians = []
abSnapJumpMeans = []
abSnapJumpStds = []
abSnapJumpMedians = []

convErrorMeans = []
convErrorStds = []
convErrorMedians = []
convJumpMeans = []
convJumpStds = []
convJumpMedians = []

for i, taps in enumerate(numTaps):
	snapErrorMeans.append( outputSnapStats[i][0][0] )
	snapErrorStds.append( outputSnapStats[i][0][1] )
	snapErrorMedians.append( outputSnapStats[i][0][2] )
	
	snapJumpMeans.append( outputSnapStats[i][1][0] )
	snapJumpStds.append( outputSnapStats[i][1][1] )
	snapJumpMedians.append( outputSnapStats[i][1][2] )
	
	abSnapErrorMeans.append( outputAbSnapStats[i][0][0] )
	abSnapErrorStds.append( outputAbSnapStats[i][0][1] )
	abSnapErrorMedians.append( outputAbSnapStats[i][0][2] )
	
	abSnapJumpMeans.append( outputAbSnapStats[i][1][0] )
	abSnapJumpStds.append( outputAbSnapStats[i][1][1] )
	abSnapJumpMedians.append( outputAbSnapStats[i][1][2] )
	
	convErrorMeans.append( outputConvStats[i][0][0] )
	convErrorStds.append( outputConvStats[i][0][1] )
	convErrorMedians.append( outputConvStats[i][0][2] )
	
	convJumpMeans.append( outputConvStats[i][1][0] )
	convJumpStds.append( outputConvStats[i][1][1] )
	convJumpMedians.append( outputConvStats[i][1][2] )
	

# Output the data
#------------------------------------------------------------------------------
snapCurves = [snapErrorMeans, snapErrorStds, snapErrorMedians, \
			  snapJumpMeans, snapErrorStds, snapJumpMedians]
abSnapCurves = [abSnapErrorMeans, abSnapErrorStds, abSnapErrorMedians, \
			    abSnapJumpMeans, abSnapErrorStds, abSnapJumpMedians]
convCurves = [convErrorMeans, convErrorStds, convErrorMedians, \
			  convJumpMeans, convJumpStds, convJumpMedians]

print				
strOutput = ""
for i, taps in enumerate(numTaps):
	strOutput = str(taps)
	for data in snapCurves:
		strOutput += "\t" + str(data[i])
	print strOutput
print

print				
strOutput = ""
for i, taps in enumerate(numTaps):
	strOutput = str(taps)
	for data in abSnapCurves:
		strOutput += "\t" + str(data[i])
	print strOutput
print

print				
strOutput = ""
for i, taps in enumerate(numTaps):
	strOutput = str(taps)
	for data in convCurves:
		strOutput += "\t" + str(data[i])
	print strOutput
print

# Plot the statistics
#------------------------------------------------------------------------------
figure = 1
 
pylab.figure(figure)
pylab.plot(filterDelays, snapErrorMeans, 'b-')
pylab.plot(filterDelays, snapErrorStds, 'g-')

pylab.plot(filterDelays, convErrorMeans, 'b--')
pylab.plot(filterDelays, convErrorStds, 'g--')
figure += 1

pylab.figure(figure)
pylab.plot(filterDelays, abSnapErrorMeans, 'b-')
pylab.plot(filterDelays, abSnapErrorStds, 'g-')

pylab.plot(filterDelays, convErrorMeans, 'b--')
pylab.plot(filterDelays, convErrorStds, 'g--')
figure += 1

pylab.figure(figure)
pylab.plot(filterDelays, snapJumpMeans, 'b-')
pylab.plot(filterDelays, snapJumpStds, 'g-')

pylab.plot(filterDelays, convJumpMeans, 'b--')
pylab.plot(filterDelays, convJumpStds, 'g--')
figure += 1

pylab.figure(figure)
pylab.plot(filterDelays, abSnapJumpMeans, 'b-')
pylab.plot(filterDelays, abSnapJumpStds, 'g-')

pylab.plot(filterDelays, convJumpMeans, 'b--')
pylab.plot(filterDelays, convJumpStds, 'g--')
figure += 1


pylab.show()












