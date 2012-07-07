#!/usr/bin/env python
# encoding: utf-8
"""
WindowFilterExample.py

Created by Fredrick Stakem on 2010-02-25.
Copyright (c) 2010 __Research__. All rights reserved.
"""

import numpy
import scipy
import pylab
import math
import scipy.stats
import scipy.fftpack
import scipy.signal

# Test parameters
size = 1000
frequencyA = 20
frequencyB = 10
windowLength = 10

# Viewing parameters
plotTimeDomain = True
plotFreqDomain = True
plotPhaseResponse = True
lowerFreqBound = -40
upperFreqBound = 40

# Create test data
time = scipy.linspace(0,1,size)
noise = scipy.stats.uniform.rvs(0,0.8,size=size)
signalA = scipy.sin( frequencyA * 2 * math.pi * time)
signalB = scipy.sin( frequencyB * 2 * math.pi * time)
signalC = signalA + signalB
signalD = signalC + noise

# Filter the test data
window = numpy.hamming(windowLength)
filteredD = numpy.convolve(window / window.sum(), signalD, mode='same')

# Do the fft on the signals -> output is complex number
fftA = scipy.fft(signalA)
fftB = scipy.fft(signalB)
fftC = scipy.fft(signalC)
fftD = scipy.fft(signalD)
fftFilteredD = scipy.fft(filteredD)

# Calculate the magnitude and phase of the fft
freq = len(fftA) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(fftA) ) )
fftMagA = 2 * scipy.fftpack.fftshift( abs(fftA) ) / len(fftA)
fftMagB = 2 * scipy.fftpack.fftshift( abs(fftB) ) / len(fftB)
fftMagC = 2 * scipy.fftpack.fftshift( abs(fftC) ) / len(fftC)
fftMagD = 2 * scipy.fftpack.fftshift( abs(fftD) ) / len(fftD)
fftMagFilteredD = 2 * scipy.fftpack.fftshift( abs(fftFilteredD)) / len(fftFilteredD)
fftPhaseA = numpy.arctan2(fftA.imag, fftA.real) * (180/math.pi)
fftPhaseB = numpy.arctan2(fftB.imag, fftB.real) * (180/math.pi)
fftPhaseC = numpy.arctan2(fftC.imag, fftC.real) * (180/math.pi)
fftPhaseD = numpy.arctan2(fftD.imag, fftD.real) * (180/math.pi)
fftPhaseFilteredD = numpy.arctan2(fftFilteredD.imag, fftFilteredD.real) * (180/math.pi)

# Plot the time domain signals
if plotTimeDomain:
	pylab.figure(1)
	pylab.subplot(311)
	pylab.plot(time, signalA)
	pylab.subplot(312)
	pylab.plot(time, signalB)
	pylab.subplot(313)
	pylab.plot(time, signalC)
	
	pylab.figure(2)
	pylab.subplot(211)
	pylab.plot(time, signalD)
	pylab.subplot(212)
	pylab.plot(time, filteredD)
	
# Show the fft of the signal
if plotFreqDomain:
	pylab.figure(3)
	pylab.subplot(211)
	pylab.plot(freq, fftMagD)
	pylab.axis([lowerFreqBound, upperFreqBound, 0, fftMagD.max()])
	pylab.subplot(212)
	pylab.plot(freq, fftMagFilteredD)
	pylab.axis([lowerFreqBound, upperFreqBound, 0, fftMagFilteredD.max()])
	
# Show the phase response of the signal
if plotPhaseResponse:
	pylab.figure(4)
	pylab.subplot(211)
	pylab.plot(freq, fftPhaseD)

pylab.show()

