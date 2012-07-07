#!/usr/bin/env python
# encoding: utf-8
"""
FftSingleMovement.py

Created by Fredrick Stakem on 2010-02-25.
Copyright (c) 2010 __Research__. All rights reserved.
"""

import numpy
import scipy
import pylab
import math
import scipy.stats
import scipy.fftpack

from Vector import Vector
from Sample import Sample
from Importer import Importer


# Filesystem paramters
dataRoot = "/Users/fstakem/Data/Movements_5_1_08/"
root = "/Users/fstakem/Research/OptimalFiltering/"
movement = "Stacking"
simulationNumber = 1
inputFile = dataRoot + movement + "/Simulation" + str(simulationNumber) + "/positionLog.txt"

# Test parameters
samplingInterval = 1

# Viewing parameters
plotTimeDomain = True
plotFreqDomain = True
plotPhaseResponse = True
lowerFreqBound = -30
upperFreqBound = 30

# Import data
importer = Importer()
data = importer.getInputData(inputFile, samplingInterval)

# Split data into components
time = range(0, len(data) * samplingInterval, samplingInterval)
x = []
y = []
z = []

for sample in data:
	x.append(sample.position.x)
	y.append(sample.position.y)
	z.append(sample.position.z)

# Do the fft on the signals -> output is complex number
fftX = scipy.fft(x)
fftY = scipy.fft(y)
fftZ = scipy.fft(z)

# Calculate the magnitude and phase of the fft
freq = len(x) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(fftX) ) )
fftMagX = 2 * scipy.fftpack.fftshift( abs(fftX) ) / len(fftX)
fftPhaseX = numpy.arctan2(fftX.imag, fftX.real) * (180/math.pi)
fftMagY = 2 * scipy.fftpack.fftshift( abs(fftY) ) / len(fftY)
fftPhaseY = numpy.arctan2(fftY.imag, fftY.real) * (180/math.pi)
fftMagZ = 2 * scipy.fftpack.fftshift( abs(fftZ) ) / len(fftZ)
fftPhaseZ = numpy.arctan2(fftZ.imag, fftZ.real) * (180/math.pi)

# Plot the time domain signals
if plotTimeDomain:
	pylab.figure(1)
	pylab.subplot(311)
	pylab.plot(time, x)
	pylab.subplot(312)
	pylab.plot(time, y)
	pylab.subplot(313)
	pylab.plot(time, z)
	
# Show the fft of the signal
if plotFreqDomain:
	pylab.figure(2)
	pylab.subplot(311)
	pylab.plot(freq, fftMagX)
	pylab.axis([lowerFreqBound, upperFreqBound, 0, fftMagX.max()])
	pylab.subplot(312)
	pylab.plot(freq, fftMagY)
	pylab.axis([lowerFreqBound, upperFreqBound, 0, fftMagY.max()])
	pylab.subplot(313)
	pylab.plot(freq, fftMagZ)
	pylab.axis([lowerFreqBound, upperFreqBound, 0, fftMagZ.max()])
	
	
pylab.show()


