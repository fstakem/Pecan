#!/usr/bin/env python
# encoding: utf-8
"""
StitchMovements.py

Created by Fredrick Stakem on 2010-03-01.
Copyright (c) 2010 __Research__. All rights reserved.
"""

import pdb
import numpy
import scipy
import pylab
import math
import scipy.stats
import scipy.fftpack

from Vector import Vector
from Sample import Sample
from PredictionSample import PredictionSample
from Packet import Packet
from Importer import Importer
from DRPredictor import DRPredictor
from DRTransmitter import DRTransmitter
from SynchTransmitter import SynchTransmitter
from Reconstructor import Reconstructor
from Network import Network
from Receiver import Receiver
from SnapReconstructor import SnapReconstructor


# Filesystem paramters
dataRoot = "/Users/fstakem/Data/Movements_5_1_08/"
root = "/Users/fstakem/Research/OptimalFiltering/"
movement = "Stacking"
simulations = range(1,101)
files = []
for i in simulations:
	inputFile = dataRoot + movement + "/Simulation" + str(i) + "/positionLog.txt"
	files.append(inputFile)

# Test parameters
debug = False
samplingInterval = 10
predictionInterval = 100
threshold = .03
heartbeat = 500
delay = 150
jitter = 80
packetLoss = 0

# Viewing parameters
plotTimeDomain = True
plotFreqDomain = True
plotPhaseResponse = True
useDb = True
lowerBoundTime = 17000 		#17000
upperBoundTime = 22000		#22000
lowerBoundFreq = 0
upperBoundFreq = 400

for fileName in files:
	# Import data
	print "Importing data..."
	importer = Importer()
	inputData = importer.getInputData(fileName, samplingInterval)
	print "First: " + str(inputData[0])
	print "Last: " + str(inputData[-1])
	print
	
# ---Code unfinsihed---
# Not sure how to accomplish this task
# a) Stitching together different data sets seems like it would cause high frequency noise
#    TODO-> Look into this problem and solve if applicable to the paper



