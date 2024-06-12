#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 12:04:00 2023

-Prepared to plot vacuum corrected transmission data at different tilt angles.
-Use the function to generate the tilt plot for required filter.

@author: janmejoy
"""
import numpy as np
import matplotlib.pyplot as plt
import glob


def tilt_plotter(folder, wl_min, wl_max, target, filter_name):
    ls=sorted(glob.glob(path+folder+'*deg*'))
    plt.figure(figsize=(6,4))
    for i in ls:
        data=np.loadtxt(i)
        plot_data=data[np.logical_and(data[:,0]>wl_min, data[:,0]<wl_max)] #selects the requisite wavelength
        wl=plot_data[:,0]
        plt.plot(wl, plot_data[:,1]*100)
    plt.axvline(target, color='black')
    plt.legend(["0°", "1°", "2°", "3°", "4°", "5°", "6°", 'Central λ'])
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('% Transmission')
    plt.title(filter_name+'_tilt | λ= '+str(target))
    plt.grid()
    plt.savefig('/home/janmejoy/Documents/'+filter_name+'_tilt.png', dpi=300)
    plt.show()

#global common path to the data
path='/home/janmejoyarch/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/'

### NB1_2_QM_tilt ###
folder='NB1/NB1_2_QM_tilt/trans_profile/'
wl_min= 200
wl_max= 240
filter_name= folder[4:9]
tilt_plotter(folder, wl_min, wl_max, 214, filter_name)

### NB2A_7_QM_tilt ###
folder='NB2A/NB2A_7_QM_tilt/trans_profile/'
wl_min= 275
wl_max= 279
filter_name= folder[5:11]
tilt_plotter(folder, wl_min, wl_max, 276.6, filter_name)

### NB3_2_QM_tilt ###
folder='NB3/NB3_2_QM_tilt/trans_profile/'
wl_min= 278.5
wl_max= 281.5
filter_name= folder[4:9]
tilt_plotter(folder, wl_min, wl_max, 279.6, filter_name)

### NB4_2_QM_tilt ###
folder='NB4/NB4_2_QM_tilt/trans_profile/'
wl_min= 278.5
wl_max= 283
filter_name= folder[4:9]
tilt_plotter(folder, wl_min, wl_max, 280.3, filter_name)

### NB5_3_QM_tilt ###
folder='NB5/NB5_3_QM_tilt/trans_profile/'
wl_min= 280.5
wl_max= 286
filter_name= folder[4:9]
tilt_plotter(folder, wl_min, wl_max, 283.2, filter_name)

### NB6_1_QM_tilt ###
folder='NB6/NB6_1_QM_tilt/trans_profile/'
wl_min= 296
wl_max= 304
filter_name= folder[4:9]
tilt_plotter(folder, wl_min, wl_max, 300, filter_name)

### NB7_2_QM_tilt ###
folder='NB7/NB7_2_QM_tilt/trans_profile/'
wl_min= 385
wl_max= 391
filter_name= folder[4:9]
tilt_plotter(folder, wl_min, wl_max, 388, filter_name)
