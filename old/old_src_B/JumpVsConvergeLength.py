#!/usr/bin/env python
# encoding: utf-8
"""
ErrorVsConvergeLength.py

Created by Fredrick Stakem on 2010-03-15.
Copyright (c) 2010 __Research__. All rights reserved.
"""

import Simulator as sim
import pdb
import numpy
import scipy
import scipy.stats
import pylab
from enum import Enum

# Globals
InterpolationType = Enum( 'Time', 'Distance' )

# Filesystem paramters
dataRoot = "/Users/fstakem/Data/Movements_5_1_08/"
root = "/Users/fstakem/Research/OptimalFiltering/"
logDir = root + "code/log/"
movement = "Stacking"
simulationNumber = 1
inputFile = dataRoot + movement + "/Simulation" + str(simulationNumber) + "/positionLog.txt"

# Test parameters
samplingInterval = 10
predictionInterval = 100
drThreshold = .02
interpolationType = InterpolationType.Time
heartbeat = 500
delay = 100
jitter = 40
packetLoss = 0
reconThresh = 140
reconThresholds = range(20,510, 20)
jumpThreshold = 0.01
spacing = 1

# Output results
errors = []
deltaInput = []
deltaSnap = []
deltaConverge = []

# Simulate the transmission
simulationData = sim.simulateTransmission(inputFile, logDir, predictionInterval, 
										  samplingInterval, heartbeat, drThreshold, 
										  delay, jitter, packetLoss)
inputData = simulationData[0]
snapRxData = sim.simulateSnapRecon(simulationData[4], logDir, "_ex1", samplingInterval)[0]
convergeRxData = sim.simulateLinearConvergence(simulationData[4], logDir, "_ex1", samplingInterval,
									   	   	   interpolationType, reconThresh)[0]

deltaInput = sim.findDistanceBetweenSamples(inputData, jumpThreshold, spacing)
deltaSnap = sim.findDistanceBetweenSamples(snapRxData, jumpThreshold, spacing)	
deltaConverge = sim.findDistanceBetweenSamples(convergeRxData, jumpThreshold, spacing)

inputData = sim.splitData(inputData)
snapRxData = sim.splitData(snapRxData)
convergeTxData = sim.splitData(convergeRxData)
																	
#for reconThreshold in reconThresholds:
	#convergeRxData = sim.simulateLinearConvergence(simulationData[4], logDir, "_ex1", samplingInterval,
	#									   	   	   interpolationType, reconThreshold)[0]
	#deltaConverge.append( sim.findDistanceBetweenSamples(convergeRxData, jumpThreshold, spacing) )


pylab.figure(1)
pylab.subplot(311)
n, bins, patches = pylab.hist(deltaInput, 50, (.01, .07))
pylab.subplot(312)
n, bins, patches = pylab.hist(deltaSnap, 50, (.01, .07))
pylab.subplot(313)
n, bins, patches = pylab.hist(deltaConverge, 50, (.01, .07))

pylab.figure(2)
pylab.subplot(311)
pylab.plot(inputData[0], inputData[1])
pylab.subplot(312)
pylab.plot(snapRxData[0], snapRxData[1])
pylab.subplot(313)
pylab.plot(convergeTxData[0], convergeTxData[1])

pylab.show()



