#!/usr/bin/env python
# encoding: utf-8
"""
Technique1.py

Created by Fredrick Stakem on 2010-03-10.
Copyright (c) 2010 __Technique #1__. All rights reserved.
"""

import inspect

# Many times you have an error in your code and you need to find out the the lines
# of code that lead to that line. You can find the calling functions with the 
# inspect module. The code below prints out the line number and calling function.

frames = inspect.getouterframes(inspect.currentframe())
for frame in frames:
	a = ""
	for i, value in enumerate(frame):
		if i == 2 or i == 3:
			a += str(value) + "  "
	print a
