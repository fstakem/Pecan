#!/usr/bin/env python
# encoding: utf-8
"""
TestImporter.py

Created by Fredrick Stakem on 2010-03-21.
Copyright (c) 2010 __Research__. All rights reserved.
"""

import pdb
import sys
import os
import numpy
import scipy
import pylab
import math
import scipy.stats
import scipy.fftpack
import scipy.signal

from Vector import Vector
from Sample import Sample
from Importer import Importer
import Simulator as sim

# Filesystem paramters
dataRoot = "/Users/fstakem/Data/Movements_5_1_08/"
root = "/Users/fstakem/Research/OptimalFiltering/"
logDir = root + "code/log/"
outputDir = root + "code/output/"
movement = "Stacking"
inputFile = dataRoot + movement + "/Simulation" + str(1) + "/positionLog.txt"
samplingInterval = 10
upperBounds = 1
lowerBounds = 1

# Import data
print "Importing data..."
importer = Importer()
inputData = importer.getInputData(inputFile, samplingInterval)
t1, x1, y1, z1 = sim.splitData(inputData)

# Filter parameters
samplingFreq = 100
taps = 80
bands = [0.0, 10, 11, 50.0]
weights = [1, 0]
coefficients = scipy.signal.remez(taps, bands, weights, Hz=samplingFreq)
gain = 1.0 / sum(coefficients)

filteredData = sim.simulateFilterRecon(inputData, logDir, "cc", samplingInterval, coefficients)[0]
sim.amplifyData(filteredData, gain)
t2, x2, y2, z2 = sim.splitData(filteredData)

# Plot data
pylab.figure(1)
pylab.plot(t1, x1, 'k-', t2, x2, 'g-')
pylab.show()





