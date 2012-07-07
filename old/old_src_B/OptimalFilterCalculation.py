#!/usr/bin/env python
# encoding: utf-8
"""
OptimalFilterCalculation.py

Created by Fredrick Stakem on 2010-03-05.
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

"""
The optimal filter is found according to the following set of criteria:
1) numtaps - the number of taps or coefficients desired
2) bands - the frequency bands desired
3) weight - the weight of the frequency bands desired

Considerations:
1) Start with the cutoff at 20 Hz
2) Move the cutoff down to 10 Hz and see what the effects are
"""

# Filter parameters
numberOfTaps = 10
bands = [0, 10, 11, 50]
weight = [1, 0]

# Run algorithm
coefficients = scipy.signal.remez(numberOfTaps, bands, weight, Hz=100)

# Output results
output = ""
for i, value in enumerate(coefficients):
	output += str(value)
	if i != len(coefficients) - 1:
		output += ", "
	
print output

