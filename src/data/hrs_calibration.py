#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 17:18:42 2024

@author: janmejoyarch
"""
import numpy as np


def difference(theoretical, measured):
    '''
    Enter Theoretical HG2 lamp wavelengths and measured central wavelengths
    of the peaks.
    The difference is computed and fitted to 2D polynomial to give the 
    wavelength shift at every wavelength.
    
    D: Difference; M: Measured Val; T: Theoretical Val
    >D = M-T
    =>T= M-D
    
    The Difference should be subtracted from the measured wavelength to get the
    Theoretical (Real) wavelength
    '''
    diff=measured-theoretical
    a, b, c=np.polyfit(measured, diff, deg=2)
    print(a,b,c)


theoretical_1200= np.array([253.652, 296.728, 302.15, 313.155, 334.148, 365.015, 404.656, 407.783])
measured_1200= np.array([253.58, 296.67,302.1, 313.13, 334.13, 365.02, 404.67, 407.81])
#data from 2022-04-26_HG2_calibsource_1200lpmm_500blaze

theoretical_2400= np.array([253.652,296.728,302.15,313.155,334.148,365.015,404.656,407.783,435.833])
measured_2400= np.array([253.77,296.84,302.26,313.27,334.23,365.08,404.72,407.84,435.87])
#data from 2022-04-19_HG2_calibsource_2400lpmm

difference(theoretical_2400, measured_2400)
difference(theoretical_1200, measured_1200)
