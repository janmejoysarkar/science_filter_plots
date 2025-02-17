#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 12:04:00 2023

-Prepared to plot vacuum corrected transmission data at different tilt angles.
-Use the function to generate the tilt plot for required filter.

2024-09-26: Modified notations to plot using relative transmission data instead
            of %tx data.

@author: janmejoy
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import scienceplots

def tilt_plotter(file, wl_min, wl_max, target, filter_name, saveplot=None):
    data=np.loadtxt(file, skiprows=1)
    plot_data=data[np.logical_and(data[:,0]>wl_min, data[:,0]<wl_max)] #selects the requisite wavelength
    with plt.style.context(['science', 'nature']):
        plt.figure(figsize=(6,4))
        angle=0
        plt.tick_params(axis='both', which='major', labelsize=12)
        for i in range(7,14):
            plt.plot(plot_data[:,0], plot_data[:,i], label=f"{angle}°")
            angle+=1
        plt.axvline(target, color='black', label= r'Central $\lambda$')
        plt.legend(fontsize=12)
        plt.xlabel('Wavelength (nm)', fontsize=12)
        plt.ylabel('Relative Transmission', fontsize=12)
        plt.title(filter_name+'-tilt | $\lambda$= '+str(target), fontsize=12)
        plt.grid(alpha=0.5)
        if saveplot: plt.savefig(f'{project_path}products/tilt/{filter_name}_tilt.pdf', dpi=300)
        if SHOW: plt.show()
        if not SHOW: plt.close()
        print("Generating Tx vs tilt for", filter_name)

if __name__=='__main__':
    #global common path to the data
    project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/science_filter_charactrerization_scripts/science_filter_plots_project/')
    SHOW, saveplot= False, True

    ### NB3_2_QM_tilt ###
    filter_name= 'NB03'
    file= f'{project_path}data/processed/{filter_name}/tilt/NB3_2_tilt.txt'
    wl_min, wl_max, cwl= 278.5, 281.5, 279.6
    tilt_plotter(file, wl_min, wl_max, cwl, filter_name, saveplot)

    ### NB1_2_QM_tilt ###
    filter_name= 'NB01' #CHECK
    wl_min, wl_max, cwl= 200, 240, 214
    file= f'{project_path}data/processed/{filter_name}/tilt/NB1_2_tilt.txt'
    tilt_plotter(file, wl_min, wl_max, cwl, filter_name, saveplot)
    
    ### NB2A_7_QM_tilt ###
    filter_name= 'NB02'
    file= f'{project_path}data/processed/{filter_name}/tilt/NB2A_7_tilt.txt'
    wl_min, wl_max, cwl= 275, 279, 276.6
    tilt_plotter(file, wl_min, wl_max, cwl, filter_name, saveplot)
    
    ### NB4_2_QM_tilt ###
    filter_name= 'NB04'
    file= f'{project_path}data/processed/{filter_name}/tilt/NB4_2_tilt.txt'
    wl_min, wl_max, cwl= 278.5, 283, 280.3
    tilt_plotter(file, wl_min, wl_max, cwl, filter_name, saveplot)
    
    ### NB5_3_QM_tilt ###
    filter_name= 'NB05'
    file= f'{project_path}data/processed/{filter_name}/tilt/NB5_3_tilt.txt'
    wl_min, wl_max, cwl= 280.5, 286, 283.2
    tilt_plotter(file, wl_min, wl_max, cwl, filter_name, saveplot)
    
    ### NB6_1_QM_tilt ###
    filter_name= 'NB06'
    file= f'{project_path}data/processed/{filter_name}/tilt/NB6_1_tilt.txt'
    wl_min, wl_max, cwl= 296, 304, 300
    tilt_plotter(file, wl_min, wl_max, cwl, filter_name, saveplot)
    
    ### NB7_2_QM_tilt ###
    filter_name= 'NB07'
    file= f'{project_path}data/processed/{filter_name}/tilt/NB7_2_tilt.txt'
    wl_min, wl_max, cwl= 385, 391, 388
    tilt_plotter(file, wl_min, wl_max, cwl, filter_name, saveplot)
