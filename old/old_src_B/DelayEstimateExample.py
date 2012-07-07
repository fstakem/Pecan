#!/usr/bin/env python
# encoding: utf-8
"""
DelayEstimateExample.py

Created by Fredrick Stakem on 2010-03-15.
Copyright (c) 2010 __Research__. All rights reserved.
"""

import Simulator as sim
import pdb
import numpy
import scipy
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
reconThreshold = 100
interpolationType = InterpolationType.Time
heartbeat = 500
delay = 100
jitter = 20
packetLoss = 0

# Filter parameters
numberOfTaps = 8
bands = [0, 1, 2, 50]
weight = [1, 0]
coefficients = scipy.signal.remez(numberOfTaps, bands, weight, Hz=100)

# Viewing parameters
lowerCorrelation = -600
upperCorrelation = 600


# Simulate the transmission
simulationData = sim.simulateTransmission(inputFile, logDir, predictionInterval, 
										  samplingInterval, heartbeat, drThreshold, 
										  delay, jitter, packetLoss)
inputData = simulationData[0]
snapRxData = sim.simulateSnapRecon(simulationData[4], logDir, "_ex1", samplingInterval)[0]
cor = sim.findCorrelation(inputData, snapRxData)
corX = scipy.linspace(0, (len(cor[0])) * samplingInterval, len(cor[0]))
corX -= numpy.array([ (len(cor[0])/2) * samplingInterval])
inputDataSplit = sim.splitData(inputData)
snapRxDataSplit = sim.splitData(snapRxData)

lowerIndex = 0
upperIndex = len(corX)
for i, v in enumerate(corX):
	if abs(lowerCorrelation - v) < 10:
		lowerIndex = i
	elif abs(upperCorrelation - v) < 10:
		upperIndex = i
print lowerIndex, upperIndex
corX = corX[lowerIndex:upperIndex]
cor[0] = cor[0][lowerIndex:upperIndex]
cor[1] = cor[1][lowerIndex:upperIndex]
cor[2] = cor[2][lowerIndex:upperIndex]
cor[0] = cor[0].tolist()
cor[1] = cor[1].tolist()
cor[2] = cor[2].tolist()

print "Delay where the correlation is max"
print str(corX[cor[0].index(max(cor[0]))])
print str(corX[cor[1].index(max(cor[1]))])
print str(corX[cor[2].index(max(cor[2]))])

pylab.figure(1)
pylab.subplot(311)
pylab.plot(corX, cor[0])
pylab.subplot(312)
pylab.plot(corX, cor[1])
pylab.subplot(313)
pylab.plot(corX, cor[2])

if False:
	pylab.figure(2)
	pylab.subplot(311)
	pylab.plot(inputDataSplit[0], inputDataSplit[1])
	pylab.subplot(312)
	pylab.plot(inputDataSplit[0], inputDataSplit[2])
	pylab.subplot(313)
	pylab.plot(inputDataSplit[0], inputDataSplit[3])

	pylab.figure(3)
	pylab.subplot(311)
	pylab.plot(snapRxDataSplit[0], snapRxDataSplit[1])
	pylab.subplot(312)
	pylab.plot(snapRxDataSplit[0], snapRxDataSplit[2])
	pylab.subplot(313)
	pylab.plot(snapRxDataSplit[0], snapRxDataSplit[3])

pylab.show()









