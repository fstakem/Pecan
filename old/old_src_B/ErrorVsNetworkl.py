#!/usr/bin/env python
# encoding: utf-8
"""
ErrorVsNetworkl.py

Created by Fredrick Stakem on 2010-03-19.
Copyright (c) 2010 __Research__. All rights reserved.
"""

import Simulator as sim
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
simulations = range(1,81)
inputFiles = []
for i in simulations:
	inputFile = dataRoot + movement + "/Simulation" + str(i) + "/positionLog.txt"
	inputFiles.append(inputFile)
	
# Test parameters
samplingInterval = 10
predictionInterval = 100
drThreshold = .02
reconThreshold = 100
interpolationType = InterpolationType.Time
heartbeat = 500

# Filter parameters
samplingFreq = 100
numberOfTaps = 22
weights = [1, 0]
minFreq = 0
maxFreq = 50
cutoffFreq = 1
bands = [minFreq, cutoffFreq, cutoffFreq+1, maxFreq]
coefficients = scipy.signal.remez(numberOfTaps, bands, weights, Hz=samplingFreq)

# Simulate the transmission and reconstruction
#------------------------------------------------------------------------------
startTimeTotal = time.time()

# First -> fixed delay, variable jitter, fixed packet loss
delay = 100
jitters = range(5, 101, 5)
jitters.insert(0, 1)
packetLoss = 0
varJitterResults = []

for jitter in jitters:
	for i, inputFile in enumerate(inputFiles):
		# Simulate the transmission
		simulationData = sim.simulateTransmission(inputFile, logDir, predictionInterval, 
												  samplingInterval, heartbeat, drThreshold, 
												  delay, jitter, packetLoss)
												
		# Simulate the reconstruction
		simNumber = inputFile.split('/')[-2][-1]
		reconstructionSnap = sim.simulateSnapRecon(simulationData[4], logDir, simNumber, samplingInterval)[0]
		reconstructionInt = sim.simulateLinearConvergence(simulationData[4], logDir, simNumber, samplingInterval,
		  							  				      interpolationType, reconThreshold)[0]
		reconstructionFilter = sim.simulateFilterRecon(reconstructionSnap, logDir, simNumber, samplingInterval, coefficients)[0]
		 sim.amplifyData(reconstructionFilter)
		s  =napError = 1
		intError = 1
		filterError = 1
		varJitterResults.append([snapError, intError, filterError])


# Second -> variable delay, fixed jitter, fixed packet loss
delays = range(10,401,10)
delays.insert(0,1)
jitter = 20
packetLoss = 0
varDelayResults = []

for delay in delays:
	for i, inputFile in enumerate(inputFiles):
		# Simulate the transmission
		simulationData = sim.simulateTransmission(inputFile, logDir, predictionInterval, 
												  samplingInterval, heartbeat, drThreshold, 
												  delay, jitter, packetLoss)

		# Simulate the reconstruction
		simNumber = inputFile.split('/')[-2][-1]
		reconstructionSnap = sim.simulateSnapRecon(simulationData[4], logDir, simNumber, samplingInterval)[0]
		reconstructionInt = sim.simulateLinearConvergence(simulationData[4], logDir, simNumber, samplingInterval,
		  							  				      interpolationType, reconThreshold)[0]
		reconstructionFilter = sim.simulateFilterRecon(reconstructionSnap, logDir, simNumber, samplingInterval, coefficients)[0]
		snapError = 1
		intError = 1
		filterError = 1
		varDelayResults.append([snapError, intError, filterError])








