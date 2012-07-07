#!/usr/bin/env python
# encoding: utf-8
"""
Simulator.py

Created by Fredrick Stakem on 2010-03-12.
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
from enum import Enum

from Vector import Vector
from Sample import Sample
from PredictionSample import PredictionSample
from Packet import Packet
from Importer import Importer
from DRPredictor import DRPredictor
from DRTransmitter import DRTransmitter
from Network import Network
from Receiver import Receiver
from SnapReconstructor import SnapReconstructor
from IntReconstructor import IntReconstructor
from VarIntReconstructor import VarIntReconstructor

# Globals
InterpolationType = Enum( 'Time', 'Distance' )

# Output function
def exportData(filename, data):
	file = open(filename, 'w')
	for sample in data:
		file.write(str(sample) + "\n")
	file.close()
	
# Split up data
def splitData(data):
	time = []
	x = []
	y = []
	z = []
	for sample in data:
		time.append(sample.time)
		x.append(sample.position.x)
		y.append(sample.position.y)
		z.append(sample.position.z)
		
	return [time, x, y, z]
	
# Find the distance error
def findDistanceError(dataSetA, dataSetB):
	error = []
	setA, setB = stripFront(dataSetA, dataSetB)
	setA, setB = stripEnd(setA, setB)

	if len(setA) != len(setB):
		print "Error: the lists are not the same length -> " + \
			  str(len(setA)) + "  " + str(len(setB))
		
	for i, sample in enumerate(setA):
		error.append( abs( setA[i].distance(setB[i]) ) )

	return error
	
def timeshift(dataSet, shift):
	shiftedData = []
	for sample in dataSet:
		shiftedSample = Sample(sample)
		shiftedSample.time += shift
		shiftedData.append(shiftedSample)
		
	return shiftedData
	
def findDistanceBetweenSamples(dataSet, threshold, spacing):
	jump = []
	for i in range(spacing, len(dataSet)):
		distance = dataSet[i].distance(dataSet[i-spacing])
		if distance > threshold:
			jump.append(distance)
		
	return jump
	
def findCorrelation(dataSetA, dataSetB):
	correlation = []
	setA, setB = stripFront(dataSetA, dataSetB)
	setA, setB = stripEnd(setA, setB)
	samplingInterval = setA[1].time - setA[0].time

	if len(setA) != len(setB):
		print "Error: the lists are not the same length."

	setA = splitData(setA)
	setB = splitData(setB)
	correlationX = scipy.signal.correlate(setA[1], setB[1])
	correlationY = scipy.signal.correlate(setA[2], setB[2])
	correlationZ = scipy.signal.correlate(setA[3], setB[3])
	
	x = scipy.linspace(0, (len(correlationX)) * samplingInterval, len(correlationX))
	x -= numpy.array([ (len(correlationX)/2) * samplingInterval])
	x = x.tolist()
	
	xCor = []
	yCor = []
	zCor = []
	for index, value in enumerate(x):
		xCor.append( (x[index], correlationX[index]) )
		yCor.append( (x[index], correlationY[index]) )
		zCor.append( (x[index], correlationZ[index]) )
		
	return [ xCor, yCor, zCor ]
	
def findDelayFromCorrelation(dataSets):
	numberToKeep = 5
	cutoffValue = 0
	highestValues = []
	for dataSet in dataSets:
		dataSet.sort( lambda x, y: cmp(y[1], x[1]) )
		dataSet = dataSet[:numberToKeep]
		
		for data in dataSet:
			if data[0] < cutoffValue:
				highestValues.append(data)
		
	highestValues.sort( lambda x, y: cmp(y[1], x[1]) )
	print highestValues
		
	return
	
	
def calculateStats(dataSet):
	if type(dataSet) != numpy.ndarray:
		dataSet = numpy.array(dataSet)
	
	mean = dataSet.mean()
	std = dataSet.std()
	median = numpy.median(dataSet)
	
	return (mean, std, median)
	
def aggregateStats(stats):
	mean = []
	std = []
	median = []
	for stat in stats:
		mean.append(stat[0])
		std.append(stat[1])
		median.append(stat[2])
	
	mean = numpy.array(mean)
	std = numpy.array(std)
	median = numpy.array(median)
	
	return (mean.mean(), std.mean(), median.mean())
	
def stripFront(dataSetA, dataSetB):
	timeA = dataSetA[0].time
	timeB = dataSetB[0].time
	setA = dataSetA
	setB = dataSetB
	if timeA > timeB:
		i = 0
		while dataSetB[i].time != timeA and i < len(dataSetB) - 1:
			i += 1
		setB = dataSetB[i:]
	elif timeA < timeB:
		i = 0
		while dataSetA[i].time != timeB and i < len(dataSetA) - 1:
			i += 1
		setA = dataSetA[i:]
		
	return [setA, setB]
	
def stripEnd(dataSetA, dataSetB):
	timeA = dataSetA[-1].time
	timeB = dataSetB[-1].time
	setA = dataSetA
	setB = dataSetB
	if timeA > timeB:
		i = -1
		while dataSetA[i].time != timeB:
			i -= 1
		setA = dataSetA[:i+1]
	elif timeA < timeB:
		i = -1
		while dataSetB[i].time != timeA:
			print i, dataSetB[i].time, timeA
			i -= 1
		setB = dataSetB[:i+1]
		
	return [setA, setB]
	
# Perform the fft
def fft(data, inDb):
	time, x, y, z = splitData(data)
	xFft = scipy.fft(x)
	yFft = scipy.fft(y)
	zFft = scipy.fft(z)
	
	xFftMag = 2 * scipy.fftpack.fftshift( abs(xFft) ) / len(xFft)
	yFftMag = 2 * scipy.fftpack.fftshift( abs(yFft) ) / len(yFft)
	zFftMag = 2 * scipy.fftpack.fftshift( abs(zFft) ) / len(zFft)
	
	xFftPhase = numpy.arctan2(xFft.imag, xFft.real) * (180/math.pi)
	yFftPhase = numpy.arctan2(yFft.imag, yFft.real) * (180/math.pi)
	zFftPhase = numpy.arctan2(zFft.imag, zFft.real) * (180/math.pi)
	
	freq = len(data) * scipy.fftpack.fftshift( scipy.fftpack.fftfreq( len(data) ) )
	freq = freq.tolist()
	
	if inDb:
		xFftMag = 20 * scipy.log10(xFftMag)
		yFftMag = 20 * scipy.log10(yFftMag)
		zFftMag = 20 * scipy.log10(zFftMag)
		
	return [freq, xFftMag, xFftPhase, yFftMag, yFftPhase, zFftMag, zFftPhase]
	
def amplifyData(data, gain):
	amplifiedData = []
	for sample in data:
		newSample = Sample(sample)
		newSample.position.x *= gain
		newSample.position.y *= gain
		newSample.position.z *= gain
		amplifiedData.append(newSample)
		
	return amplifiedData
	
# Crop data to bounds	
def cropData(x, y, lowerBound, upperBound):
	if len(x) != len(y):
		print "Error: lists must be of same length"
		return
		
	lowerIndex = 0
	upperIndex = len(x)
	lowerDiff = abs(x[0] - x[1]) * 100
	upperDiff = abs(x[0] - x[1]) * 100
	
	for i, v in enumerate(x):
		diff = abs(lowerBound - v)
		if diff < lowerDiff:
			lowerDiff = diff
			lowerIndex = i
			
		diff = abs(upperBound - v)
		if diff < upperDiff:
			upperDiff = diff
			upperIndex = i
	
	return [ x[lowerIndex:upperIndex], y[lowerIndex:upperIndex] ]
	
# Main simulator	
def transmitData(inputFile, logDir, predictionInterval, samplingInterval, 
                 heartbeat, drThreshold, delay, jitter, packetLoss):
	# Import data
	print "Importing data..."
	importer = Importer()
	rawInputData = importer.getInputData(inputFile, samplingInterval)
	exportData(logDir + "RawInputData.txt", rawInputData)
	
	# Filtering input data
	print "Filtering data..."
	samplingFreq = int(1e3/samplingInterval)
	taps = 80
	bands = [0.0, 10, 11, 50.0]
	weights = [1, 0]
	coefficients = scipy.signal.remez(taps, bands, weights, Hz=samplingFreq)
	gain = 1.0 / sum(coefficients)
	filteredInputData = filterData(rawInputData, logDir, "cc", samplingInterval, coefficients)[0]
	filteredInputData = amplifyData(filteredInputData, gain)
	exportData(logDir + "FilteredInputData.txt", filteredInputData)

	# Create the prediction vectors
	print "Creating the prediction vectors..."
	predictor = DRPredictor()
	predictedData = predictor.getPredictedData(filteredInputData, predictionInterval, samplingInterval)
	exportData(logDir + "PredictionData.txt", predictedData)

	# Run the transmission algorithm
	print "Simulating the transmission algorithm..."
	transmitter = DRTransmitter(heartbeat)
	drTxPackets = transmitter.getTransmittedPackets(drThreshold, predictedData)
	exportData(logDir + "DRTxPackets.txt", drTxPackets)

	# Simulate the transmission of the packets
	print "Simulating the network..."
	network = Network()
	drRxPackets = network.getReceivedPackets(drTxPackets, delay, jitter, packetLoss)
	exportData(logDir + "DRRxPackets.txt", drRxPackets)

	# Receive the packets
	print "Receiving the packets..."
	receiver = Receiver()
	drRxFilteredPackets = receiver.getFilteredData(drRxPackets)
	exportData(logDir + "DRRxData.txt", drRxFilteredPackets)

	return [rawInputData, filteredInputData, predictedData, drTxPackets, 
	        drRxPackets, drRxFilteredPackets]

def snapReconstructData(packetData, logDir, fileEnding, samplingInterval):
	# Snap reconstruct the transmitted and received data
	#print "Snap reconstructing the signals..."
	snapReconstructor = SnapReconstructor()
	snapData = snapReconstructor.getReconstructedSignal(packetData, samplingInterval)
	exportData(logDir + "SnapData_" + fileEnding + ".txt", snapData)
	
	return [snapData]
	
def filterData(reconData, logDir, fileEnding, samplingInterval, coefficients):
	# Filter the reconstructed data
	#print "Filtering the data..."
	filteredData = []
	time, x, y, z = splitData(reconData)
	xFiltered = scipy.signal.convolve(coefficients, x)
	yFiltered = scipy.signal.convolve(coefficients, y)
	zFiltered = scipy.signal.convolve(coefficients, z)
	
	numberToDrop = len(coefficients) - 1
	time = time[numberToDrop:]
	xFiltered = xFiltered[numberToDrop:]
	yFiltered = yFiltered[numberToDrop:]
	zFiltered = zFiltered[numberToDrop:]
	
	for i, v in enumerate(time):
		sample = Sample()
		sample.time = time[i]
		sample.position.x = xFiltered[i]
		sample.position.y = yFiltered[i]
		sample.position.z = zFiltered[i]
		filteredData.append(sample)
	
	filteredData = filteredData[:-200]
	exportData(logDir + "FilteredData_" + fileEnding + ".txt", filteredData)
	
	return [filteredData]
	
def convergeData(packetData, logDir, fileEnding, samplingInterval,
  			     convergenceTime):
	# Interpolation reconstruct the transmitted and received data
	#print "Interpolation reconstructing the signals..."
	intReconstructor = IntReconstructor()
	convergedData = intReconstructor.getReconstructedSignal(packetData, samplingInterval, 
	    												    convergenceTime, 500)
	exportData(logDir + "ConvergedData_" + fileEnding + ".txt", convergedData)
	
	return [convergedData]
	
def varConvergeData(packetData, logDir, fileEnding, samplingInterval,
  			       shortConvergenceTime, longConvergenceTime):
	# Interpolation reconstruct the transmitted and received data
	#print "Interpolation reconstructing the signals..."
	varIntReconstructor = VarIntReconstructor()
	varIntReconstructor.logFile = logDir + "VarConInternal.txt"
	convergedData = varIntReconstructor.getReconstructedSignal(packetData, samplingInterval, 
	    												       shortConvergenceTime, 
															   longConvergenceTime, 1500)
	exportData(logDir + "VarConvergedData_" + fileEnding + ".txt", convergedData)

	return [convergedData]
	
	
	
	