#!/usr/bin/env python
# encoding: utf-8
"""
FftExample.py

Created by Fredrick Stakem on 2010-02-25.
Copyright (c) 2010 __Research__. All rights reserved.
"""

import numpy
import scipy
import pylab
import math
import scipy.stats
import scipy.fftpack


# Test parameters
size = 10000
frequencyA = 10
frequencyB = 2
useNoise = False

# Viewing parameters
plotTimeDomain = True
plotFreqDomain = True
plotPhaseResponse = True
lowerFreqBound = -40
upperFreqBound = 40

# Create test data
time = scipy.linspace(0,1,size)
dt = time[1] - time[0]
print dt
fmax = 1 / (dt)
print fmax
npts = 131072
f = scipy.linspace(0,fmax,npts) - fmax/2

noise = scipy.stats.uniform.rvs(0,0.8,size=size)
signalA = scipy.sin( frequencyA * 2 * math.pi * time)
signalB = scipy.sin( frequencyB * 2 * math.pi * time)
signalC = signalA + signalB

if useNoise:
	signalC = signalC + noise
	
# Do the fft on the signals -> output is complex number
fftA = scipy.fft(signalA, npts)
fftB = scipy.fft(signalB, npts)
fftC = scipy.fft(signalC, npts)
print len(fftC), len(f)

# Calculate the magnitude and phase of the fft
freq = len(time) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(time) ) )
fftMagA = 2 * scipy.fftpack.fftshift( abs(fftA) ) / len(time)
fftMagB = 2 * scipy.fftpack.fftshift( abs(fftB) ) / len(time)
fftMagC = 2 * scipy.fftpack.fftshift( abs(fftC) ) / len(time)
fftPhaseA = numpy.arctan2(fftA.imag, fftA.real) * (180/math.pi)
fftPhaseB = numpy.arctan2(fftB.imag, fftB.real) * (180/math.pi)
fftPhaseC = numpy.arctan2(fftC.imag, fftC.real) * (180/math.pi)

# Plot the time domain signals
if plotTimeDomain:
	pylab.figure(1)
	pylab.subplot(311)
	pylab.plot(time, signalA)
	pylab.subplot(312)
	pylab.plot(time, signalB)
	pylab.subplot(313)
	pylab.plot(time, signalC)
	
# Show the fft of the signal
if plotFreqDomain:
	pylab.figure(2)
	#pylab.plot( freq, fftMagC )
	pylab.plot( f, fftMagC )
	#pylab.axis([lowerFreqBound, upperFreqBound, 0, fftMagC.max()])
	
pylab.show()