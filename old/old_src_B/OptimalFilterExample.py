#!/usr/bin/env python
# encoding: utf-8
"""
OptimalFilterExample.py

Created by Fredrick Stakem on 2010-03-03.
Copyright (c) 2010 __Research__. All rights reserved.
"""

import pdb
import numpy
import scipy
import pylab
import math
import scipy.stats
import scipy.fftpack
import scipy.signal

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


# Signal paramters
size = 1000
frequencyA = 5
frequencyB = 10
frequencyC = 20
frequencyD = 30
useNoise = True

# Create test signals
time = scipy.linspace(0,1,size)
noise = scipy.stats.uniform.rvs(-1,1,size=size)
signalA = scipy.sin( frequencyA * 2 * math.pi * time)
signalB = scipy.sin( frequencyB * 2 * math.pi * time)
signalC = scipy.sin( frequencyC * 2 * math.pi * time)
signalD = scipy.sin( frequencyD * 2 * math.pi * time)
signalE = signalA + signalB + signalC + signalD

if useNoise:
	signalE = signalE + noise

# Test parameters
debug = False

# Filter parameters
numberOfTaps = 3
bands = [0, 2, 3, 50]
weight = [1, 0]
coefficients = scipy.signal.remez(numberOfTaps, bands, weight, Hz=100)

# Filter signal 
filtered = scipy.signal.convolve(coefficients, signalE)
timeFiltered = scipy.linspace(0, 1 + (len(filtered) - size) * time[1]-time[0], len(filtered))

# Viewing parameters
plotTimeDomain = True
plotFreqDomain = True
useDb = False
lowerBoundTime = 0 			
upperBoundTime = size		
lowerBoundFreq = -40
upperBoundFreq = 40

# Do the fft on the signals -> output is complex number
fftE = scipy.fft(signalE)
fftFilterd = scipy.fft(filtered)

# Calculate the magnitude and phase of the fft
freq = len(time) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(fftE) ) )
freqOut = len(timeFiltered) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(fftFilterd) ) )
fftMagE = 2 * scipy.fftpack.fftshift( abs(fftE) ) / len(fftE)
fftPhaseE = numpy.arctan2(fftE.imag, fftE.real) * (180/math.pi)
fftMagFilterd = 2 * scipy.fftpack.fftshift( abs(fftFilterd) ) / len(fftFilterd)
fftPhaseFilterd = numpy.arctan2(fftFilterd.imag, fftFilterd.real) * (180/math.pi)

# Plot the time domain signals
if plotTimeDomain:
	pylab.figure(1)
	pylab.subplot(211)
	pylab.plot(time, signalE)
	pylab.axis([0, time.max(), signalE.min(), signalE.max()])
	pylab.subplot(212)
	pylab.plot(timeFiltered, filtered)
	pylab.axis([0, time.max(), filtered.min(), filtered.max()])
	
# Show the fft of the signal
if plotFreqDomain:
	pylab.figure(2)
	pylab.subplot(211)
	pylab.plot(freq, fftMagE)
	pylab.axis([lowerBoundFreq, upperBoundFreq, 0, fftMagE.max()])
	pylab.subplot(212)
	pylab.plot(freqOut, fftMagFilterd)
	pylab.axis([lowerBoundFreq, upperBoundFreq, 0, fftMagFilterd.max()])

pylab.show()
