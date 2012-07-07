#!/usr/bin/env python
# encoding: utf-8
"""
ShowEffectsOfConv_Filter.py

Created by Fredrick Stakem on 2010-04-12.
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
root = "/Users/fstakem/Research/PhD/2010_Research/OptimalFiltering/"
logDir = root + "code/log/"
outputDir = root + "code/output/"
movement = "Stacking"
inputFile = inputFile = dataRoot + movement + "/Simulation" + str(1) + "/positionLog.txt"

# Parameters for all algorithms
samplingInterval = 10
predictionInterval = 100
heartbeat = 500
interpolationType = InterpolationType.Time

# Dead reckoing parameters
drThreshold = .025

# Close convergence parameters
shortConvergenceInterval = 100
longConvergenceInterval = 300

# Network parameters
delay = 100
jitter = 60
packetLoss = 0

# Filter parameters
samplingFreq = int(1e3/samplingInterval)
longTaps = 60
shortTaps = 20
bands = [0.0, 1, 2, 50.0]
weights = [1, 0]
longCoefficients = scipy.signal.remez(longTaps, bands, weights, Hz=samplingFreq)
longGain = 1.0 / sum(longCoefficients)
shortCoefficients = scipy.signal.remez(shortTaps, bands, weights, Hz=samplingFreq)
shortGain = 1.0 / sum(shortCoefficients)

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

snapShortFilteredData = s.filterData(snapReconData, logDir, simNumber, samplingInterval, 
							         shortCoefficients)[0]
snapShortFilteredData = s.amplifyData(snapShortFilteredData, shortGain)	

snapLongFilteredData = s.filterData(snapReconData, logDir, simNumber, samplingInterval, 
							        longCoefficients)[0]
snapLongFilteredData = s.amplifyData(snapLongFilteredData, longGain)

shortConvData = s.convergeData(drRxFilteredPackets, logDir, simNumber, samplingInterval,
  			     		       interpolationType, shortConvergenceInterval)[0]	

longConvData = s.convergeData(drRxFilteredPackets, logDir, simNumber, samplingInterval,
  			     		      interpolationType, longConvergenceInterval)[0]		

# Output data to file for graphing
lowerTimeLimit = 19000
upperTimeLimit = 25000

inputDataFile = outputDir + "InputData_Graph.txt"
iData = []
for sample in filteredInputData:
	if sample.time >= lowerTimeLimit and sample.time <= upperTimeLimit and sample.time % 50 == 0:
		iData.append(sample)
s.exportData(inputDataFile, iData)

snapDataFile = outputDir + "SnapData_Graph.txt"
sData = []
for sample in snapReconData:
	if sample.time >= lowerTimeLimit and sample.time <= upperTimeLimit and sample.time % 50 == 0:
		sData.append(sample)
s.exportData(snapDataFile, sData)

shortConvergenceFile = outputDir + "ShortConvergenceData_Graph.txt"
scData = []
for sample in shortConvData:
	if sample.time >= lowerTimeLimit and sample.time <= upperTimeLimit and sample.time % 50 == 0:
		scData.append(sample)
s.exportData(shortConvergenceFile, scData)

longConvergenceFile = outputDir + "LongConvergenceData_Graph.txt"
lcData = []
for sample in longConvData:
	if sample.time >= lowerTimeLimit and sample.time <= upperTimeLimit and sample.time % 50 == 0:
		lcData.append(sample)
s.exportData(longConvergenceFile, lcData)

shortFilterFile = outputDir + "ShortFilterData_Graph.txt"
sfData = []
for sample in snapShortFilteredData:
	if sample.time >= lowerTimeLimit and sample.time <= upperTimeLimit and sample.time % 50 == 0:
		sfData.append(sample)
s.exportData(shortFilterFile, sfData)

longFilterFile = outputDir + "LongFilterData_Graph.txt"
lfData = []
for sample in snapShortFilteredData:
	if sample.time >= lowerTimeLimit and sample.time <= upperTimeLimit and sample.time % 50 == 0:
		lfData.append(sample)
s.exportData(longFilterFile, lfData)


# Plot the data
iData = [ [], [], [], [] ]
sData = [ [], [], [], [] ]
sfData = [ [], [], [], [] ]
lfData = [ [], [], [], [] ]
scData = [ [], [], [], [] ]
lcData = [ [], [], [], [] ]

iData[0], iData[1], iData[2], iData[3] = s.splitData(filteredInputData)
sData[0], sData[1], sData[2], sData[3] = s.splitData(snapReconData)
sfData[0], sfData[1], sfData[2], sfData[3] = s.splitData(snapShortFilteredData)
lfData[0], lfData[1], lfData[2], lfData[3] = s.splitData(snapLongFilteredData)
scData[0], scData[1], scData[2], scData[3] = s.splitData(shortConvData)
lcData[0], lcData[1], lcData[2], lcData[3] = s.splitData(longConvData)

figure = 1
pylab.figure(figure)
pylab.plot(iData[0], iData[1], 'k--', sData[0], sData[1], 'g-')
pylab.axis([18000, 26500, 0.05, 0.45])
figure += 1

pylab.figure(figure)
pylab.plot(iData[0], iData[1], 'k--', sfData[0], sfData[1], 'g-')
pylab.plot(iData[0], iData[1], 'k--', lfData[0], lfData[1], 'b-')
pylab.axis([18000, 26500, 0.05, 0.45])
figure += 1

pylab.figure(figure)
pylab.plot(iData[0], iData[1], 'k--', scData[0], scData[1], 'g-')
pylab.plot(iData[0], iData[1], 'k--', lcData[0], lcData[1], 'b-')
pylab.axis([18000, 26500, 0.05, 0.45])
figure += 1

pylab.show()


