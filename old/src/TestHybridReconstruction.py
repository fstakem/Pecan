#!/usr/bin/env python
# encoding: utf-8
"""
TestHybridReconstruction.py

Created by Fredrick Stakem on 2010-04-09.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
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
root = "/Users/fstakem/Research/OptimalFiltering/"
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
drThreshold = .015

# Reconstruction parameters
snapLimitType = SnapLimitType.Relative
snapLimit = 0.4
reconstructionThreshold = 80

# Network parameters
delay = 100
jitter = 20
packetLoss = 0

# Plotting paramters
lowerTime = 18000
upperTime = 26500
yMax = 0.45
yMin = 0.05

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
hydridSnapData = s.hydridSnapReconstructData(drRxFilteredPackets, logDir, simNumber, samplingInterval,
										     interpolationType, snapLimitType, reconstructionThreshold, 
										     snapLimit)[0]															
convergedData = s.convergeData(drRxFilteredPackets, logDir, simNumber, samplingInterval,
					  		   interpolationType, reconstructionThreshold)[0]

iData = [ [] ] * 4
sData = [ [] ] * 4
hData = [ [] ] * 4
cData = [ [] ] * 4

iData[0], iData[1], iData[2], iData[3] = s.splitData(filteredInputData)
sData[0], sData[1], sData[2], sData[3] = s.splitData(snapReconData)
hData[0], hData[1], hData[2], hData[3] = s.splitData(hydridSnapData)
cData[0], cData[1], cData[2], cData[3] = s.splitData(convergedData)

pylab.figure(1)
pylab.plot(iData[0], iData[1], 'k-', sData[0], sData[1], 'b-')
pylab.axis([ 19000, 26000, 0.05, 0.45 ])
pylab.figure(2)
pylab.plot(iData[0], iData[1], 'k-', hData[0], hData[1], 'b-')
pylab.axis([ 19000, 26000, 0.05, 0.45 ])
pylab.figure(3)
pylab.plot(iData[0], iData[1], 'k-', cData[0], cData[1], 'b-')
pylab.axis([ 19000, 26000, 0.05, 0.45 ])

pylab.show()





