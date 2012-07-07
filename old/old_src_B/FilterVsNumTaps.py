#!/usr/bin/env python
# encoding: utf-8
"""
ErrorVsNumTaps.py

Created by Fredrick Stakem on 2010-03-15.
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
delay = 100
jitter = 20
packetLoss = 0

# Filter parameters
samplingFreq = 100
numberOfTaps = range(2,52,2)
weights = [1, 0]
minFreq = 0
maxFreq = 50
cutoffFreqs = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]

# Simulate the transmission
startTimeTotal = time.time()
testData = []
for inputFile in inputFiles:
	simulationData = sim.simulateTransmission(inputFile, logDir, predictionInterval, 
											  samplingInterval, heartbeat, drThreshold, 
											  delay, jitter, packetLoss)
	simNumber = inputFile.split('/')[-2][-1]
	reconstruction = sim.simulateSnapRecon(simulationData[4], logDir, simNumber, samplingInterval)
	testData.append([simulationData[0], reconstruction[0]])
	
# Simulate the quality for different filters
print
print "Curves: " + str(len(cutoffFreqs))
print "Taps: " + str(len(numberOfTaps))
print "Data Sets: " + str(len(testData))

errorCurves = []
delayCurves = []
for cutoffFreq in cutoffFreqs:
	print "Working on filter with cutoff frequency: " + str(cutoffFreq)
	errorCurve = []
	delayCurve = []
	bands = [minFreq, cutoffFreq, cutoffFreq+1, maxFreq]
	startTimeTaps = time.time()
	# Collect the error versus the number of taps
	for taps in numberOfTaps:
		print "\tWorking on filter with taps: " + str(taps)
		# Parks-McClellan method
		coefficients = scipy.signal.remez(taps, bands, weights, Hz=samplingFreq)
		# Window method
		#cutoff = --need to fill this in--
		#coefficients = scipy.signal.firwin(taps, cutoff, window='hamming')
		freqResponse = scipy.signal.freqz(coefficients)
		freq = freqResponse[0] * (samplingFreq/(2 * math.pi))
		magnitude = abs(freqResponse[1])
		phase = numpy.arctan2(freqResponse[1].imag, freqResponse[1].real) * (samplingFreq/(2 * math.pi))
		delay = 0.5 * taps * samplingInterval
		errors = []
		startTimeData = time.time()
		# Use mulitple differenet data sets
		for index, data in enumerate(testData):
			inputData = data[0]
			reconData = data[1]
			filteredData = sim.simulateFilterRecon(reconData, logDir, str(index+1), samplingInterval, coefficients)[0]
			error = sim.findDistanceError(inputData, filteredData)
			mean = numpy.array(error).mean()
			errors.append(mean)
	
		avgError = numpy.array(errors).mean()
		errorCurve.append(avgError)
		delayCurve.append(delay)
		print "\tTime working on the data sets: " + str(time.time() - startTimeData)
	errorCurves.append(errorCurve)
	delayCurves.append(delayCurve)
	print "\tTime working on the different taps: " + str(time.time() - startTimeTaps)
print "\tTotal time working on simulation: " + str(time.time() - startTimeTotal)


# Collect the final data and export
outputFile = outputDir + "FilterVsTaps.txt"
file = open(outputFile, 'w')
# First line
outputStr = "Cutoff Freq:\t\t"
for i, cutoffFreq in enumerate(cutoffFreqs):
	outputStr += str(cutoffFreq) + "\t" + str(cutoffFreq) + "\t"
outputStr += "\n"
file.write(outputStr)	

# Other lines
for j, taps in enumerate(numberOfTaps):
	outputStr = ""
	if j == 0:
		outputStr += "Taps:\t"
	else:
		outputStr += " \t"
	outputStr += str(taps) + "\t"
	for i, cutoffFreq in enumerate(cutoffFreqs):
		outputStr += str(errorCurves[i][j]) + "\t" + str(delayCurves[i][j]) + "\t"
	
	outputStr += "\n"	
	file.write(outputStr)
file.close()

	
	