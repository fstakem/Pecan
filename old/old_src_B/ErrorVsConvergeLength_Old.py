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
reconThresholds = range(20,510, 100)
jumpThreshold =0.001
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
deltaInput = sim.findDistanceBetweenSamples(inputData, jumpThreshold, spacing)
																			
for reconThreshold in reconThresholds:
	convergeTxData = sim.simulateLinearConvergence(simulationData[4], logDir, "_ex1", samplingInterval,
										   	   	   interpolationType, reconThreshold)
	snapRxData = sim.simulateSnapRecon(simulationData[4], logDir, "_ex1", samplingInterval)
	errors.append( sim.findDistanceError(inputData, convergeTxData[0]) )
	deltaSnap.append( sim.findDistanceBetweenSamples(snapRxData, jumpThreshold, spacing) )
	deltaConverge.append( sim.findDistanceBetweenSamples(convergeTxData, jumpThreshold, spacing) )

# Prepare the data for plotting
temp = []
for error in errors:
	temp.append( scipy.stats.mean(error) )
errors = temp

#pylab.figure(1)
#pylab.plot(reconThresholds, errors)
pylab.figure(2)
n, bins, patches = pylab.hist(deltaInput, 50)

pylab.show()



