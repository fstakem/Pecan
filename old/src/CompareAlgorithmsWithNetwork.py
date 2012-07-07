#!/usr/bin/env python
# encoding: utf-8
"""
CompareAlgorithmsWithNetwork.py

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
root = "/Users/fstakem/Research/PhD/OptimalFiltering/"
logDir = root + "code/log/"
outputDir = root + "code/output/"
movement = "Stacking"
simulations = range(1,21)
inputFiles = []
for i in simulations:
    inputFile = dataRoot + movement + "/Simulation" + str(i) + \
				"/positionLog.txt"
    inputFiles.append(inputFile)

# Simulation parameters
#------------------------------------------------------------------------------
varyDelay = True

# Transmission parameters
#------------------------------------------------------------------------------
predictionInterval = 100
samplingInterval = 10
heartbeat = 500
drThreshold = 0.02
convergenceType = InterpolationType.Time

# Network parameters
#------------------------------------------------------------------------------
delaySet = []
jitterSet = []
packetLossSet = 0
networkParams = []

if varyDelay:
	delaySet = range(10, 201, 10)
	jitterSet = 20
	networkParams = [(x, jitterSet, packetLossSet) for x in delaySet]
else:
	delaySet = 100
	jitterSet = range(5, 81, 5)
	networkParams = [(delaySet, x, packetLossSet) for x in jitterSet]

# Reconstruction parameters
#------------------------------------------------------------------------------
convergenceType = InterpolationType.Time
convergenceInterval = 100
snapLimit = 0.005

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
inputStats = []
outputStats = []
for i in range(0,3):
	outputData.append([])
	outputStats.append([])
	
	for networkParam in networkParams:
		outputData[-1].append([])
		outputStats[-1].append([])
		
# Simulate the transmission of the data
#------------------------------------------------------------------------------
startTimeTotal = time.time()
transmittedData = []
for i, networkParam in enumerate(networkParams):
	delay = networkParam[0]
	jitter = networkParam[1]
	packetLoss = networkParam[2]
	transmittedData.append([])
	print "Simulating the transmission for network params: " + \
	      str(delay) + " " + str(jitter) + " " + str(packetLoss)
	
	for inputFile in inputFiles:
		simNumber = inputFile.split('/')[-2][-1]
		print "Simulating the transmission for data set: " + str(simNumber)

		data = s.transmitData(inputFile, logDir, predictionInterval,
							  samplingInterval, heartbeat, drThreshold,
							  delay, jitter, packetLoss)
		transmittedData[-1].append(data)
	print

print "Total time spent simulating the transmission: " + str(time.time() - \
															 startTimeTotal)
print
	
# Simulate the reconstruction of the data
#------------------------------------------------------------------------------
startTimeRecon = time.time()
for i, txDataSets in enumerate(transmittedData):
	startTimeData = time.time()
	networkParam = networkParams[i]
	delay = networkParam[0]
	jitter = networkParam[1]
	packetLoss = networkParam[2]
	print "Simulating the reconstruction for network params: " + \
	      str(delay) + " " + str(jitter) + " " + str(packetLoss)
	
	for j, txData in enumerate(txDataSets):
		print "\tSimulating data set: " + str(j+1)
		simNumber = str(j+1)
		rawInputData = txData[0]
		filteredInputData = txData[1]
		predictedData = txData[2]
		drTxPackets = txData[3]
		drRxPackets = txData[4]
		drRxFilteredPackets = txData[5]
		
		snapData = s.snapReconstructData(drRxFilteredPackets, 
										 logDir, 
										 simNumber, 
										 samplingInterval)[0]
		
		filteredData = 	s.filterData(snapData, 
								 	 logDir, 
								 	 simNumber, 
							     	 samplingInterval, 
								 	 coefficients)[0]
		filteredData = s.amplifyData(filteredData, gain)
		outputData[0][i].append(filteredData)
		
		abSnapData = s.snapLimitReconstructData(drRxFilteredPackets,
											    logDir,
											    simNumber,
											    samplingInterval,
										        convergenceType,
											    SnapLimitType.Absolute,
											    convergenceInterval,
										        snapLimit)[0]
		abFilteredData = s.filterData(abSnapData, 
								 	  logDir, 
								 	  simNumber, 
							     	  samplingInterval, 
								 	  coefficients)[0]
		abFilteredData = s.amplifyData(abFilteredData, gain)
		outputData[1][i].append(abFilteredData)
		
		convergenceData = s.convergeData(drRxFilteredPackets, 
										 logDir, 
										 simNumber, 
										 samplingInterval,
		  			     				 convergenceType, 
										 convergenceInterval)[0]						
		outputData[2][i].append(convergenceData)
		
		

	print "\tSimulation time for all of the data sets: " + \
		  str(time.time() - startTimeData)
print "Simulation time for all of the network parameters: " + \
      str(time.time() - startTimeRecon)
print

# Calculate the results and statistics
#------------------------------------------------------------------------------
print "Calculating the statistics..."
i = 0
inputJumps = []
	
for j, inputFile in enumerate(inputFiles):
	data = transmittedData[i][j]
	initialData = data[1]

	inputJump = s.findDistanceBetweenSamples(initialData,
											 jumpThreshold,
											 jumpSpacing)
	inputJumps.append( s.calculateStats(inputJump) )

inputStats = s.aggregateStats(inputJumps)

for i, algorithm in enumerate(range(0,3)):
	for j, networkParam in enumerate(networkParams):
	    distanceErrors = []
	    distanceJumps = []
	    stats = []
	    for k, reconstructedData in enumerate(outputData[i][j]):
	        inputData = transmittedData[j][k][1]
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
print "Seperating the data..."
x = []
snapErrorMean = []
snapErrorStd = []
snapErrorMedian = []
snapJumpMean = []
snapJumpStd = []
snapJumpMedian = []

abSnapErrorMean = []
abSnapErrorStd = []
abSnapErrorMedian = []
abSnapJumpMean = []
abSnapJumpStd = []
abSnapJumpMedian = []

convergenceErrorMean = []
convergenceErrorStd = []
convergenceErrorMedian = []
convergenceJumpMean = []
convergenceJumpStd = []
convergenceJumpMedian = []

for j, networkParam in enumerate(networkParams):
	snapErrorMean.append( outputStats[0][j][0][0] )
	snapErrorStd.append( outputStats[0][j][0][1] )
	snapErrorMedian.append( outputStats[0][j][0][2] )
	snapJumpMean.append( outputStats[0][j][1][0] )
	snapJumpStd.append( outputStats[0][j][1][1] )
	snapJumpMedian.append( outputStats[0][j][1][2] )
	
	abSnapErrorMean.append( outputStats[1][j][0][0] )
	abSnapErrorStd.append( outputStats[1][j][0][1] )
	abSnapErrorMedian.append( outputStats[1][j][0][2] )
	abSnapJumpMean.append( outputStats[1][j][1][0] )
	abSnapJumpStd.append( outputStats[1][j][1][1] )
	abSnapJumpMedian.append( outputStats[1][j][1][2] )
	
	convergenceErrorMean.append( outputStats[2][j][0][0] )
	convergenceErrorStd.append( outputStats[2][j][0][1] )
	convergenceErrorMedian.append( outputStats[2][j][0][2] )
	convergenceJumpMean.append( outputStats[2][j][1][0] )
	convergenceJumpStd.append( outputStats[2][j][1][1] )
	convergenceJumpMedian.append( outputStats[2][j][1][2] )

for networkParam in networkParams:	
	if varyDelay:
		x.append(networkParam[0])
	else:
		x.append(networkParam[1])
	
# Output the data
#------------------------------------------------------------------------------
print "Outputing the statistics..."
curves = [snapErrorMean, snapErrorStd, snapErrorMedian,
	  	  snapJumpMean, snapErrorStd, snapJumpMedian,
		  abSnapErrorMean, abSnapErrorStd, abSnapErrorMedian,
		  abSnapJumpMean, abSnapErrorStd, abSnapJumpMedian,
		  convergenceErrorMean, convergenceErrorStd, convergenceErrorMedian, 
		  convergenceJumpMean, convergenceJumpStd, convergenceJumpMedian]

print				
strOutput = ""
for i, networkParam in enumerate(networkParams):
	if varyDelay:
		strOutput = str(networkParam[0])
	else:
		strOutput = str(networkParam[1])
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
		pylab.plot(x, snapErrorMean, 'k-')
		pylab.plot(x, abSnapErrorMean, 'g-')
		pylab.plot(x, convergenceErrorMean, 'b-')

	if plotMedian == True:
		pylab.figure(figure)
		figure += 1
		pylab.plot(x, snapErrorMedian, 'k-')
		pylab.plot(x, abSnapErrorMedian, 'g-')
		pylab.plot(x, convergenceErrorMedian, 'b-')

if plotJump == True:
	if plotMean == True:
		pylab.figure(figure)
		figure += 1
		pylab.plot(x, snapJumpMean, 'k-')
		pylab.plot(x, abSnapJumpMean, 'k-')
		pylab.plot(x, convergenceJumpMean, 'b-')

	if plotMedian == True:
		pylab.figure(figure)
		figure += 1
		pylab.plot(x, snapJumpMedian, 'k-')
		pylab.plot(x, abSnapJumpMedian, 'g-')
		pylab.plot(x, convergenceJumpMedian, 'b-')

pylab.show()


