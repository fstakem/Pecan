#!/usr/bin/env python
# encoding: utf-8
"""
FftExample.py

Created by Fredrick Stakem on 2010-04-07.
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
from Importer import Importer

# Filesystem paramters
dataRoot = "/Users/fstakem/Data/Movements_5_1_08/"
root = "/Users/fstakem/Research/PhD/2010_Research/OptimalFiltering/"
logDir = root + "code/log/"
outputDir = root + "code/output/"
movement = "Stacking"
inputFile = inputFile = dataRoot + movement + "/Simulation" + str(1) + "/positionLog.txt"

# Parameters for all algorithms
samplingInterval = 10
numPoints = 131072

# Importing the raw data
print "Importing data..."
importer = Importer()
rawInputData = importer.getInputData(inputFile, samplingInterval)
s.exportData(logDir + "RawInputData.txt", rawInputData)

# Filtering input data
print "Filtering data..."
samplingFreq = int(1e3/samplingInterval)
taps = 80
bands = [0.0, 10, 11, 50.0]
weights = [1, 0]
coefficients = scipy.signal.remez(taps, bands, weights, Hz=samplingFreq)
gain = 1.0 / sum(coefficients)
filteredInputData = s.filterData(rawInputData, logDir, "cc", samplingInterval, coefficients)[0]
filteredInputData = s.amplifyData(filteredInputData, gain)
s.exportData(logDir + "FilteredInputData.txt", filteredInputData)

# FFT the data
print "Analyzing the data..."
time, x, y, z = s.splitData(filteredInputData)
dt = (time[1] - time[0]) * 1e-3
freqMax = 1 / dt
freq = scipy.linspace(0, freqMax, numPoints) - freqMax/2
print dt, freqMax, len(freq)

xFft = scipy.fft(x, numPoints)
yFft = scipy.fft(y, numPoints)
zFft = scipy.fft(z, numPoints)
print len(xFft)

xFftMag = 2 * scipy.fftpack.fftshift( abs(xFft) ) / len(time)
yFftMag = 2 * scipy.fftpack.fftshift( abs(yFft) ) / len(time)
zFftMag = 2 * scipy.fftpack.fftshift( abs(zFft) ) / len(time)

xFftPhase = numpy.arctan2(xFft.imag, xFft.real) * (180/math.pi)
yFftPhase = numpy.arctan2(yFft.imag, yFft.real) * (180/math.pi)
zFftPhase = numpy.arctan2(zFft.imag, zFft.real) * (180/math.pi)

# Ouptut data to a file
lowerFreqLimit = 0
upperFreqLimit = 1

inputDataFile = logDir + "InputData_Graph.txt"
file = open(inputDataFile, 'w')
for i, f in enumerate(freq):
	if f >= lowerFreqLimit and f <= upperFreqLimit and i % 10 == 0:
		file.write(str(f) + "\t" + str(xFftMag[i]) + "\n")
file.close()

# Plot the freq response
pylab.figure(1)
pylab.plot(time,x)

pylab.figure(2)
pylab.plot( freq, xFftMag )
pylab.axis([0, 1, 0, 0.28])

pylab.show()

