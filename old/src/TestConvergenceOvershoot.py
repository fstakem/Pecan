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
from Sample import Sample
from PredictionSample import PredictionSample
from DRPredictor import DRPredictor
from Packet import Packet
from DRTransmitter import DRTransmitter
from Network import Network
from Receiver import Receiver

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
drThreshold = .015

# Reconstruction parameters
snapLimitType = SnapLimitType.Relative
snapLimit = 0.4
reconstructionThreshold = 100

# Network parameters
delay = 1
jitter = 0
packetLoss = 0

# Plotting paramters
lowerTime = 18000
upperTime = 26500
yMax = 0.45
yMin = 0.05

# Simulate the algorithm
stepFunc = []
for i in range(0,5001, 10):
	if i < 200:
		stepFunc.append( Sample(i, 0, 0, 0) )
	else:
		stepFunc.append( Sample(i, 1, 1, 1) )
	
predictor = DRPredictor()
predictedData = predictor.getPredictedData(stepFunc, predictionInterval, samplingInterval)	
s.exportData(logDir + "PredictionData.txt", predictedData)
transmitter = DRTransmitter(heartbeat)
drTxPackets = transmitter.getTransmittedPackets(.9, predictedData)
s.exportData(logDir + "TransmittedData.txt", drTxPackets)
network = Network()
drRxPackets = network.getReceivedPackets(drTxPackets, delay, jitter, packetLoss)
s.exportData(logDir + "ReceivedData.txt", drRxPackets)
receiver = Receiver()
drRxFilteredPackets = receiver.getFilteredData(drRxPackets)	
s.exportData(logDir + "FilteredData.txt", drRxFilteredPackets)							
convergedData = s.convergeData(drRxFilteredPackets, logDir, "-", samplingInterval,
					  		   interpolationType, reconstructionThreshold)[0]

iData = [ [] ] * 4
cData = [ [] ] * 4

iData[0], iData[1], iData[2], iData[3] = s.splitData(stepFunc)
cData[0], cData[1], cData[2], cData[3] = s.splitData(convergedData)

pylab.figure(1)
pylab.plot(iData[0], iData[1], 'k-', cData[0], cData[1], 'b-')
pylab.axis([ 0, 2000, -.1, 1.8 ])

pylab.show()





