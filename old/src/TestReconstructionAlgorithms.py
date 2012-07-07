#!/usr/bin/env python
# encoding: utf-8
"""
TestReconstructionAlgorithms.py

Created by Fredrick Stakem on 2010-03-21.
Copyright (c) 2010 __Research__. All rights reserved.
"""

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
dataRoot = "/Users/fstakem/Data/Movements_5_1_08/"
root = "/Users/fstakem/Research/PhD/OptimalFiltering/"
logDir = root + "code/log/"
outputDir = root + "code/output/"
movement = "Stacking"
inputFile = inputFile = dataRoot + movement + "/Simulation" + str(1) + "/positionLog.txt"

# Parameters for all algorithms
samplingInterval = 10
predictionInterval = 100
heartbeat = 500
processingDelay = -100
interpolationType = InterpolationType.Time

# Dead reckoing parameters
#drThreshold = .02
#drThreshold = .015
drThreshold = .02

# Close snap limit parameters
closeRelSnapLimit = 0.4
closeAbSnapLimit = 0.002

# Far snap limit parameters
farRelSnapLimit = 0.4
farAbSnapLimit = 0.002

# Close convergence parameters
closeReconThreshold = 100
snapLimitType = SnapLimitType.Relative

# Far convergence parameters
farReconThreshold = 120

# Network parameters
delay = 100
jitter = 40
packetLoss = 0

# Filter parameters
samplingFreq = int(1e3/samplingInterval)
longTaps = 16
shortTaps = 12
bands = [0.0, 1, 2, 50.0]
weights = [1, 0]
longCoefficients = scipy.signal.remez(longTaps, bands, weights, Hz=samplingFreq)
longGain = 1.0 / sum(longCoefficients)
shortCoefficients = scipy.signal.remez(shortTaps, bands, weights, Hz=samplingFreq)
shortGain = 1.0 / sum(shortCoefficients)

# Plotting paramters
lowerTime = 18000
upperTime = 26500
yMax = 0.45
yMin = 0.05
useDb = False
errorBins = 50
jumpBins = 100
plotTimeDomain = True
plotFreqDomain = False
plotError = False
plotJump = False

# Simulate the algorithms
simNumber = inputFile.split('/')[-2][-1]
 
data = s.transmitData(inputFile, logDir, predictionInterval, 
					  samplingInterval, heartbeat, drThreshold, 
					  delay, jitter, packetLoss)
										
rawInputData = data[0]
filteredInputData = data[1]
predictedData = data[2]
drTxPackets = data[3]
drRxPackets = data[4]
drRxFilteredPackets = data[5]
										
snapReconData = s.snapReconstructData(drRxFilteredPackets, logDir, simNumber, samplingInterval)[0]

closeRelSnapLimitData = s.snapLimitReconstructData(drRxFilteredPackets, logDir, simNumber, samplingInterval,
												    interpolationType, SnapLimitType.Relative, closeReconThreshold, 
												    closeRelSnapLimit)[0]
closeAbSnapLimitData = s.snapLimitReconstructData(drRxFilteredPackets, logDir, simNumber, samplingInterval,
												  interpolationType, SnapLimitType.Absolute, closeReconThreshold, 
												  closeAbSnapLimit)[0]
farRelSnapLimitData = s.snapLimitReconstructData(drRxFilteredPackets, logDir, simNumber, samplingInterval,
								                 interpolationType, SnapLimitType.Relative, closeReconThreshold, 
								                 farRelSnapLimit)[0]
farAbSnapLimitData = s.snapLimitReconstructData(drRxFilteredPackets, logDir, simNumber, samplingInterval,
								                interpolationType, SnapLimitType.Absolute, closeReconThreshold, 
								                farAbSnapLimit)[0]
																
closeConvergedData = s.convergeData(drRxFilteredPackets, logDir, simNumber, samplingInterval,
					  			    interpolationType, closeReconThreshold)[0]
farConvergedData = s.convergeData(drRxFilteredPackets, logDir, simNumber, samplingInterval,
								 interpolationType, farReconThreshold)[0]

snapFilteredData = s.filterData(closeRelSnapLimitData, logDir, simNumber, samplingInterval, 
							    longCoefficients)[0]
snapFilteredData = s.amplifyData(snapFilteredData, longGain)				
relSnapFilteredData = s.filterData(closeRelSnapLimitData, logDir, simNumber, samplingInterval, 
							       shortCoefficients)[0]
relSnapFilteredData = s.amplifyData(relSnapFilteredData, shortGain)
abSnapFilteredData = s.filterData(closeAbSnapLimitData, logDir, simNumber, samplingInterval, 
							      shortCoefficients)[0]
abSnapFilteredData = s.amplifyData(abSnapFilteredData, shortGain)


convergedFilteredData = s.filterData(closeConvergedData, logDir, simNumber, samplingInterval, 
									 shortCoefficients)[0]	
convergedFilteredData = s.amplifyData(convergedFilteredData, shortGain)

farConvergedShiftData = s.timeshift(farConvergedData, processingDelay)
snapFilteredShiftData = s.timeshift(snapFilteredData, processingDelay)
relSnapFilteredShiftData = s.timeshift(relSnapFilteredData, processingDelay)
abSnapFilteredShiftData = s.timeshift(abSnapFilteredData, processingDelay)
convergedFilteredShiftData = s.timeshift(convergedFilteredData, processingDelay)
				
# Calculate the data metrics
# A) Distance error
distanceError = []
distanceError.append( s.findDistanceError(filteredInputData, snapReconData) )
distanceError.append( s.findDistanceError(filteredInputData, farRelSnapLimitData) )
distanceError.append( s.findDistanceError(filteredInputData, farAbSnapLimitData) )
distanceError.append( s.findDistanceError(filteredInputData, farConvergedData) )

distanceError.append( s.findDistanceError(filteredInputData, snapFilteredData) )
distanceError.append( s.findDistanceError(filteredInputData, relSnapFilteredData) )
distanceError.append( s.findDistanceError(filteredInputData, abSnapFilteredData) )
distanceError.append( s.findDistanceError(filteredInputData, convergedFilteredData) )

distanceError.append( s.findDistanceError(filteredInputData, farConvergedShiftData) )
distanceError.append( s.findDistanceError(filteredInputData, snapFilteredShiftData) )
distanceError.append( s.findDistanceError(filteredInputData, relSnapFilteredShiftData) )
distanceError.append( s.findDistanceError(filteredInputData, abSnapFilteredShiftData) )
distanceError.append( s.findDistanceError(filteredInputData, convergedFilteredShiftData) )

errorTitles = [ 'Input/Snap Error                          ', 'Input/Snap Relative Limit Error           ', 
				'Input/Snap Absolute Limit Error           ', 'Input/Convergence Error                   ', 
				'Input/Snap Filtered Error                 ', 'Input/Snap Relative Filtered Error        ', 
                'Input/Snap Absolute Filtered Error        ', 'Input/Converence Filtered Error           ',
				'Input/Convergence Shifted Error           ', 'Input/Snap Filtered Shifted Error         ',
				'Input/Snap Relative Filtered Shifted Error', 'Input/Snap Absolute Filtered Shifted Error',
                'Input/Convergence Filtered Shifted Error  ' ]

# B) Inter-sample jump
threshold = 0
spacing = 1
distanceJump = []
distanceJump.append( s.findDistanceBetweenSamples(rawInputData, threshold, spacing) )
distanceJump.append( s.findDistanceBetweenSamples(filteredInputData, threshold, spacing) )
distanceJump.append( s.findDistanceBetweenSamples(snapReconData, threshold, spacing) )
distanceJump.append( s.findDistanceBetweenSamples(farRelSnapLimitData, threshold, spacing) )
distanceJump.append( s.findDistanceBetweenSamples(farAbSnapLimitData, threshold, spacing) )
distanceJump.append( s.findDistanceBetweenSamples(farConvergedData, threshold, spacing) )

distanceJump.append( s.findDistanceBetweenSamples(snapFilteredData, threshold, spacing) )
distanceJump.append( s.findDistanceBetweenSamples(relSnapFilteredData, threshold, spacing) )
distanceJump.append( s.findDistanceBetweenSamples(abSnapFilteredData, threshold, spacing) )
distanceJump.append( s.findDistanceBetweenSamples(convergedFilteredData, threshold, spacing) )

jumpTitles = [ 'Raw Input Jump             ', 'Filtered Input Jump        ', 
               'Snap Jump                  ', 'Snap Relative Jump         ',
			   'Snap Absolute Jump         ', 'Convergence Jump           ',
               'Snap Filtered Jump         ', 'Snap Relative Filtered Jump',
               'Snap Absolute Filtered Jump', 'Convergence Filtered Jump  ' ]

# C Transmitted and received signal correlation
signalCorrelation = []
signalCorrelation.append( s.findCorrelation(filteredInputData, snapReconData) )
signalCorrelation.append( s.findCorrelation(filteredInputData, farRelSnapLimitData) )
signalCorrelation.append( s.findCorrelation(filteredInputData, farAbSnapLimitData) )
signalCorrelation.append( s.findCorrelation(filteredInputData, farConvergedData) )
signalCorrelation.append( s.findCorrelation(filteredInputData, snapFilteredData) )
signalCorrelation.append( s.findCorrelation(filteredInputData, relSnapFilteredData) )
signalCorrelation.append( s.findCorrelation(filteredInputData, abSnapFilteredData) )
signalCorrelation.append( s.findCorrelation(filteredInputData, convergedFilteredData) )
signalCorrelation.append( s.findCorrelation(filteredInputData, farConvergedShiftData) )
signalCorrelation.append( s.findCorrelation(filteredInputData, snapFilteredShiftData) )
signalCorrelation.append( s.findCorrelation(filteredInputData, relSnapFilteredShiftData) )
signalCorrelation.append( s.findCorrelation(filteredInputData, abSnapFilteredShiftData) )
signalCorrelation.append( s.findCorrelation(filteredInputData, convergedFilteredShiftData) )
	                                      
# Calculate the statistics
errorStatistics = [ [ [], [], [] ],
					[ [], [], [] ],
					[ [], [], [] ],
					[ [], [], [] ],
					[ [], [], [] ],
					[ [], [], [] ],
					[ [], [], [] ],
					[ [], [], [] ],
					[ [], [], [] ],
					[ [], [], [] ],
					[ [], [], [] ],
					[ [], [], [] ],
					[ [], [], [] ]
 				  ]

jumpStatistics = [ [ [], [], [] ],
				   [ [], [], [] ],
				   [ [], [], [] ],
				   [ [], [], [] ],
				   [ [], [], [] ],
				   [ [], [], [] ],
				   [ [], [], [] ],
				   [ [], [], [] ],
				   [ [], [], [] ], 
				   [ [], [], [] ]
 				  ]

for index, error in enumerate(distanceError):
	mean, std, median = s.calculateStats(error)
	errorStatistics[index][0].append(mean)
	errorStatistics[index][1].append(std)
	errorStatistics[index][2].append(median)
	
for index, jump in enumerate(distanceJump):
	mean, std, median = s.calculateStats(jump)
	jumpStatistics[index][0].append(mean)
	jumpStatistics[index][1].append(std)
	jumpStatistics[index][2].append(median)
	
# Print out the resulting statistics
for i, error in enumerate(errorStatistics):
	outputStr = errorTitles[i] + ":\t"
	for j in range(0,3):
		outputStr += "%.5f   " % errorStatistics[i][j][0]
	print outputStr
	
for i, error in enumerate(jumpStatistics):
	outputStr = jumpTitles[i] + ":\t"
	for j in range(0,3):
		outputStr += "%.5f   " % jumpStatistics[i][j][0]
	print outputStr

# Plotting
figure = 1
tdData = [ [ [], [], [], [] ],
		   [ [], [], [], [] ],
		   [ [], [], [], [] ],
		   [ [], [], [], [] ],
		   [ [], [], [], [] ],
		   [ [], [], [], [] ],
		   [ [], [], [], [] ],
		   [ [], [], [], [] ],
		   [ [], [], [], [] ]
 		 ]

tdData[0][0], tdData[0][1], tdData[0][2], tdData[0][3] = s.splitData(filteredInputData)
tdData[1][0], tdData[1][1], tdData[1][2], tdData[1][3] = s.splitData(snapReconData)
tdData[2][0], tdData[2][1], tdData[2][2], tdData[2][3] = s.splitData(farRelSnapLimitData)
tdData[3][0], tdData[3][1], tdData[3][2], tdData[3][3] = s.splitData(farAbSnapLimitData)
tdData[4][0], tdData[4][1], tdData[4][2], tdData[4][3] = s.splitData(farConvergedData)
tdData[5][0], tdData[5][1], tdData[5][2], tdData[5][3] = s.splitData(snapFilteredData)
tdData[6][0], tdData[6][1], tdData[6][2], tdData[6][3] = s.splitData(relSnapFilteredData)
tdData[7][0], tdData[7][1], tdData[7][2], tdData[7][3] = s.splitData(abSnapFilteredData)
tdData[8][0], tdData[8][1], tdData[8][2], tdData[8][3] = s.splitData(convergedFilteredData)

fdData = [ [ [], [], [], [], [], [], [] ],
		   [ [], [], [], [], [], [], [] ],
		   [ [], [], [], [], [], [], [] ],
		   [ [], [], [], [], [], [], [] ],
		   [ [], [], [], [], [], [], [] ],
		   [ [], [], [], [], [], [], [] ],
		   [ [], [], [], [], [], [], [] ],
		   [ [], [], [], [], [], [], [] ],
		   [ [], [], [], [], [], [], [] ]
 		 ]

fdData[0][0], fdData[0][1], fdData[0][2], fdData[0][3], \
fdData[0][4], fdData[0][5], fdData[0][6] = s.fft(filteredInputData, useDb)

fdData[1][0], fdData[1][1], fdData[1][2], fdData[1][3], \
fdData[1][4], fdData[1][5], fdData[1][6] = s.fft(snapReconData, useDb)

fdData[2][0], fdData[2][1], fdData[2][2], fdData[2][3], \
fdData[2][4], fdData[2][5], fdData[2][6] = s.fft(farRelSnapLimitData, useDb)

fdData[3][0], fdData[3][1], fdData[3][2], fdData[3][3], \
fdData[3][4], fdData[3][5], fdData[3][6] = s.fft(farAbSnapLimitData, useDb)

fdData[4][0], fdData[4][1], fdData[4][2], fdData[4][3], \
fdData[4][4], fdData[4][5], fdData[4][6] = s.fft(farConvergedData, useDb)

fdData[5][0], fdData[5][1], fdData[5][2], fdData[5][3], \
fdData[5][4], fdData[5][5], fdData[5][6] = s.fft(snapFilteredData, useDb)

fdData[6][0], fdData[6][1], fdData[6][2], fdData[6][3], \
fdData[6][4], fdData[6][5], fdData[6][6] = s.fft(relSnapFilteredData, useDb)

fdData[7][0], fdData[7][1], fdData[7][2], fdData[7][3], \
fdData[7][4], fdData[7][5], fdData[7][6] = s.fft(abSnapFilteredData, useDb)

fdData[8][0], fdData[8][1], fdData[8][2], fdData[8][3], \
fdData[8][4], fdData[8][5], fdData[8][6] = s.fft(convergedFilteredData, useDb)

titles = [ 'Input/Snap Error', 'Input/Snap Relative Limit Error', 
		   'Input/Snap Absolute Limit Error', 'Input/Convergence Error', 
		   'Input/Snap Filtered Error', 'Input/Snap Relative Filtered Error', 
           'Input/Snap Absolute Filtered Error', 'Input/Converence Filtered Error'
		 ]
		
# Output data to file for graphing
lowerTimeLimit = 19000
upperTimeLimit = 25000

inputDataFile = logDir + "InputData_Graph.txt"
iData = []
for sample in filteredInputData:
	if sample.time >= lowerTimeLimit and sample.time <= upperTimeLimit and sample.time % 50 == 0:
		iData.append(sample)
s.exportData(inputDataFile, iData)

snapDataFile = logDir + "SnapData_Graph.txt"
sData = []
for sample in snapReconData:
	if sample.time >= lowerTimeLimit and sample.time <= upperTimeLimit and sample.time % 50 == 0:
		sData.append(sample)
s.exportData(snapDataFile, sData)

convergenceFile = logDir + "ConvergenceData_Graph.txt"
cData = []
for sample in farConvergedData:
	if sample.time >= lowerTimeLimit and sample.time <= upperTimeLimit and sample.time % 50 == 0:
		cData.append(sample)
s.exportData(convergenceFile, cData)

filterFile = logDir + "FilterData_Graph.txt"
fData = []
for sample in snapFilteredData:
	if sample.time >= lowerTimeLimit and sample.time <= upperTimeLimit and sample.time % 50 == 0:
		fData.append(sample)
s.exportData(filterFile, fData)

# A) Plot the data time domain
if plotTimeDomain:
	for index, data in enumerate(tdData[1:]):
		pylab.figure(figure)
		figure += 1
		pylab.plot(tdData[0][0], tdData[0][1], 'k-', tdData[index+1][0], tdData[index+1][1], 'g-')
		pylab.axis([18000, 26500, 0.05, 0.45])
		pylab.title(titles[index])
	
# B) Plot the frequency domain
if plotFreqDomain:
	for index, data in enumerate(tdData[1:]):
		pylab.figure(figure)
		figure += 1
		pylab.plot(fdData[0][0], fdData[0][1], 'k-', fdData[index+1][0], fdData[index+1][1], 'g-')
		#pylab.axis([0, 80, 0, 0.3])
		pylab.axis([-40, 40, 0, 0.3])
		pylab.title(titles[index])
	
# C) Plot the metrics
if plotError:
	for index, data in enumerate(distanceError):
		pylab.figure(figure)
		figure += 1
		n, bins, patches = pylab.hist(data, errorBins, (.01, .1))
		pylab.title(errorTitles[index])
	
if plotJump:
	for index, data in enumerate(distanceJump):
		pylab.figure(figure)
		figure += 1
		n, bins, patches = pylab.hist(data, jumpBins, (.005, .05))
		pylab.title(jumpTitles[index])	
	
pylab.show()	
	
	
			
				
				