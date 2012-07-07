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

# Globals
InterpolationType = Enum( 'Time', 'Distance' )

# Filesystem paramters
dataRoot = "/Users/fstakem/Data/Movements_5_1_08/"
root = "/Users/fstakem/Research/OptimalFiltering/"
logDir = root + "code/log/"
outputDir = root + "code/output/"
movement = "Stacking"
inputFile = inputFile = dataRoot + movement + "/Simulation" + str(1) + "/positionLog.txt"

# Test parameters
samplingInterval = 10
predictionInterval = 100
drThreshold = .02
farReconThreshold = 100
closeReconThreshold = 40
snapLimit = 0.5
interpolationType = InterpolationType.Time
heartbeat = 500
delay = 100
jitter = 20
packetLoss = 0

# Filter parameters
samplingFreq = int(1e3/samplingInterval)
taps = 20
snapTaps = 12
bands = [0.0, 1, 2, 50.0]
weights = [1, 0]
coefficients = scipy.signal.remez(taps, bands, weights, Hz=samplingFreq)
gain = 1.0 / sum(coefficients)
snapCoefficients = scipy.signal.remez(snapTaps, bands, weights, Hz=samplingFreq)
snapGain = 1.0 / sum(snapCoefficients)

# Plotting paramters
plotTimeDomain = True
plotFreqDomain = True
plotStatistics = True

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
snapLimitReconData = s.snapLimitReconstructData(drRxFilteredPackets, logDir, simNumber, samplingInterval,
												interpolationType, closeReconThreshold, snapLimit)[0]
closeConvergedData = s.convergeData(drRxFilteredPackets, logDir, simNumber, samplingInterval,
					  			    interpolationType, closeReconThreshold)[0]
farConveredData = s.convergeData(drRxFilteredPackets, logDir, simNumber, samplingInterval,
								 interpolationType, farReconThreshold)[0]
				
snapFilteredData = s.filterData(snapReconData, logDir, simNumber, samplingInterval, 
							    snapCoefficients)[0]
convergedFilteredData = s.filterData(closeConvergedData, logDir, simNumber, samplingInterval, 
									 coefficients)[0]	
				
# Calculate the data statistics


# Plotting
figure = 1
inputTime, inputX, inputY, inputZ = s.splitData(filteredInputData)
snapTime, snapX, snapY, snapZ = s.splitData(snapReconData)
snapLimitTime, snapLimitX, snapLimitY, snapLimitZ = s.splitData(snapLimitReconData)
convergedTime, convergedX, convergedY, convergedZ = s.splitData(farConveredData)
filteredTime, filteredX, filteredY, filteredZ = s.splitData(snapFilteredData)
conFilteredTime, conFilteredX, conFilteredY, conFilteredZ = s.splitData(convergedFilteredData)

# Plot the data time domain
if plotTimeDomain:
	pylab.figure(figure)
	figure += 1
	pylab.plot(inputTime, inputX, 'k-', snapTime, snapX, 'g-')
	
	pylab.figure(figure)
	figure += 1
	pylab.plot(inputTime, inputX, 'k-', snapLimitTime, snapLimitX, 'g-')
	
	pylab.figure(figure)
	figure += 1
	pylab.plot(inputTime, inputX, 'k-', convergedTime, convergedX, 'g-')
	
	pylab.figure(figure)
	figure += 1
	pylab.plot(inputTime, inputX, 'k-', filteredTime, filteredX, 'g-')
	
	pylab.figure(figure)
	figure += 1
	pylab.plot(inputTime, inputX, 'k-', conFilteredTime, conFilteredX, 'g-')
	
# Plot the frequency domain
if plotFreqDomain:
	pass
	
# Plot the statistics	
if plotStatistics:
	pass
	
pylab.show()	
	
	
			
				
				