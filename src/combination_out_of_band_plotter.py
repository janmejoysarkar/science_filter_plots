#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 24 Sep 2024.
@author: janmejoyarch

- Created to make consolidated OOB vs IB plots for filter combinations.
- This is to show that filter combinations give good throughput and sufficient
out of band blockage.
- This code converts percentage transmission in data to relative transmission
  and performs all calculation.

2024-09-26: Modified to use relative transmission data instead of %tx data.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.integrate import simpson
import scienceplots
from scipy.interpolate import interp1d


def tx_gen(oob_blue, oob_red, ib, ib_wl_mn, ib_wl_mx, oob_wl_mn, oob_wl_mx):
    '''
    Tx profile generator. Clips the provided ib and oob spectra to avoid
    overlaps during plotting.
    '''
    oob_blue= oob_blue[np.logical_and(oob_blue[:,0]>oob_wl_mn, oob_blue[:,0]<ib_wl_mn)]
    oob_red= oob_red[np.logical_and(oob_red[:,0]>ib_wl_mx, oob_red[:,0]<oob_wl_mx)]
    ib=ib[np.logical_and(ib[:,0]>ib_wl_mn, ib[:,0]<ib_wl_mx)]
    ib[:,1], oob_blue[:,1], oob_red[:,1] =ib[:,1], oob_blue[:,1], oob_red[:,1]
    return(ib, oob_blue, oob_red)

def fill_interval(tx, fill_range, cent=None):
    '''
    picks the center of the tx spectrum and gives intervals within the +- fill range
    The effective fill width is 2*fill_range around center wavelength.
    Input: tx: np array. 2 col. wl and tx; fill_range: +- 
    of this value will be filled.
    Returns: The array (x and y) that has to be integrated 
    (for net tx measurement) or filled (in plots).
    '''
    if len(tx)!=0:
        if cent==None: cent= tx[:,0][int(len(tx)/2)] 
        array=tx[(tx[:,0]>cent-fill_range) & (tx[:,0]<cent+fill_range)]
        #the array to be used for integration or shading the plot.
        return array

def integrate(fill_ib, fill_oob_r, fill_oob_b):
    ib_integrate= simpson(fill_ib[:,1],x=fill_ib[:,0])
    oob_red_integrate= simpson(fill_oob_r[:,1], x=fill_oob_r[:,0])
    oob_red_percent= oob_red_integrate*100/ib_integrate
    if len (fill_oob_b) != 0: #NOTE: This is condition is different from the oob tx code 
        oob_blue_integrate= simpson(fill_oob_b[:,1], x=fill_oob_b[:,0])
        oob_blue_percent= oob_blue_integrate*100/ib_integrate
    else:
        oob_blue_percent= -200
    print(f"{filt_name}\t |oob_b% {round(oob_blue_percent,4)}\t |oob_r% {round(oob_red_percent,4)}")

def combined(FILT1, FILT2, lamda1, lamda2, fill_width, cent=None):
    '''
    - Concatenates OOB and IB profiles to make it into one curve.
    - lamda1, lamda2: Performs linear interpolation to get the interpolated graph in 
                      steps of 0.01 nm starting from lamda1 to lamda2.
    - Returns > Integration ratios taken from integrate function
              > Plots
    - FILT1, FILT2: Contains 3 arrays each for ib, oob_b and oob_r in this sequence.
                    Contains wavelength and % tx.
    - The % tx has to be converted to fraction transmission.
    - Total tx %= (%tx1/100)*(%tx2/100)*100%

    '''
    concatenated_1= np.concatenate((FILT1[1], FILT1[0], FILT1[2])) #combined ib and oob plots for Filt 1
    x_new= np.arange(lamda1, lamda2, 0.01)#USER INPUT NEEDED
    fn= interp1d(concatenated_1[:,0], concatenated_1[:,1]) #Interpolation for filt 1 combined plot
    y_new_1= fn(x_new) #Interpolated filt 1 fractional tx
    if len(FILT2[1])!= 0: #Condition for BP4 as it is missing OOB Blue data
        concatenated_2= np.concatenate((FILT2[1], FILT2[0], FILT2[2])) # combined ib and oob plots for filt 2
    else:
        concatenated_2= np.concatenate((FILT2[0], FILT2[2]))
    fn= interp1d(concatenated_2[:,0], concatenated_2[:,1]) #Interpolation for filt 2 combined plot
    y_new_2= fn(x_new) #Interpolated filt 2 fractional tx
    
    final= np.column_stack((x_new, y_new_1*y_new_2)) #Wavelength vs filt1*filt2 tx% array
    
    fill_ib= fill_interval(final, fill_width, cent) #IB fill area
    fill_oob_b= fill_interval(final, fill_width, FILT1[1][int(len(FILT1[1])/2)][0]) #OOB Blue fill area
    fill_oob_r= fill_interval(final, fill_width, FILT1[2][int(len(FILT1[2])/2)][0]) #OOB Red fill area
    integrate(fill_ib, fill_oob_r, fill_oob_b) #Integration across fill area
    #Plotting 
    with plt.style.context(['science', 'nature']):
        plt.figure(figsize=(6,4))
        plt.plot(final[:,0], final[:,1], color= 'black', label='Out of Band')
        plt.plot(final[:,0][(final[:,0]>FILT1[0][:,0][0]) & (final[:,0]<FILT1[0][:,0][-1])], final[:,1]
                 [(final[:,0]>FILT1[0][:,0][0]) & (final[:,0]<FILT1[0][:,0][-1])], color= 'red', label='Inband')
        plt.fill_between(fill_ib[:,0],fill_ib[:,1], y2=0, linewidth=0, color='red', alpha=0.2)
        plt.fill_between(fill_oob_r[:,0], fill_oob_r[:,1], y2=0, linewidth=0, color='black', alpha=0.2)
        plt.fill_between(fill_oob_b[:,0], fill_oob_b[:,1], y2=0, linewidth=0, color='black', alpha=0.2)
        #plt.yscale('log')
        plt.xlabel('Wavelength (nm)', fontsize=12)
        plt.ylabel('Relative Transmission', fontsize=12)
        plt.title(filt_name+'_combination', fontsize=12)
        plt.tick_params(axis='both', which='major', labelsize=12)
        plt.grid(alpha=0.5)
        plt.legend(fontsize=12)
        if SAVE: plt.savefig(f'{project_path}products/combined/{filt_name}_combined.pdf', dpi=300)
        if not SHOW: plt.close()
        if SHOW: plt.show()

if __name__=='__main__':
    SHOW, SAVE= False, True
    project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/science_filter_charactrerization_scripts/science_filter_plots_project/') 
    folder= os.path.join(project_path, 'data/processed/')
    print("OOB %tx wrt IB")
    
    ## NB1_2 ##
    filt_name="NB01_2"
    oob_blue=np.loadtxt(folder+'NB01/oob/NB1_2_oob_blue_oob.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'NB01/oob/NB1_2_oob_red_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB01/oob/NB1_2_inband_inband.txt', skiprows=1, usecols=(0,1))
    NB01= tx_gen(oob_blue, oob_red, ib, 205, 230, 190, 400)
    
    ## BB1_3 ##
    filt_name="BB01_3"
    oob_blue=np.loadtxt(folder+'BB01/oob/BB1_3_oob_190_oob.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BB01/oob/BB1_3_oob_262.5_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'BB01/oob/BB1_3_spatial_inband.txt', skiprows=1, usecols=(0,1))
    BB01= tx_gen(oob_blue, oob_red, ib, 210, 245, 190, 300)

    ## BB3_3 ##
    filt_name="BB03_3"
    oob_blue=np.loadtxt(folder+'BB03/oob/BB3_3_oob_299nm_oob.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BB03/oob/BB3_3_oob_380nm_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'BB03/oob/BB3_3_spatial_inband.txt', skiprows=1, usecols=(0,1))
    BB03= tx_gen(oob_blue, oob_red, ib, 318, 359, 292, 400)

    ## BB2_3 ##
    filt_name="BB02_3"
    ib1= np.loadtxt(folder+'BB02/oob/BB2_3_spatial_255nm_inband.txt', skiprows=1, usecols= (0,1))
    ib2= np.loadtxt(folder+'BB02/oob/BB2_3_spatial_290nm_inband.txt', skiprows=1, usecols= (0,1))
    ib2=ib2[np.logical_not(ib2[:,0]<276.8)]
    ib= np.concatenate((ib1, ib2))
    oob_blue=np.loadtxt(folder+'BB02/oob/BB2_3_oob_229nm_oob.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BB02/oob/BB2_3_oob_323nm_oob.txt', skiprows=1, usecols= (0,1))
    BB02= tx_gen(oob_blue, oob_red, ib, 245, 304, 190, 400)

    ## BB1_3 ##
    filt_name="BB01_3"
    oob_blue=np.loadtxt(folder+'BB01/oob/BB1_3_oob_190_oob.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BB01/oob/BB1_3_oob_262.5_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'BB01/oob/BB1_3_spatial_inband.txt', skiprows=1, usecols=(0,1))
    BB01= tx_gen(oob_blue, oob_red, ib, 210, 245, 190, 300)

    ## BP2_6 ##
    filt_name= "BP02_6"
    oob_blue=np.loadtxt(folder+'BP02/oob/BP2_8_252-272_OOB_oob.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BP02/oob/BP2_8_290-310_OOB_oob.txt', skiprows=1, usecols= (0,1))
    ib1= np.loadtxt(folder+'BP02/oob/BP2_8_262-282_inband.txt', skiprows=1, usecols= (0,1))
    ib2= np.loadtxt(folder+'BP02/oob/BP2_8_278-297_inband.txt', skiprows=1, usecols= (0,1))
    ib=np.concatenate((ib1[:-300], ib2[90:]))
    BP02= tx_gen(oob_blue, oob_red, ib, 268, 290, 190, 340)
    
    ## BP4_2 ##
    filt_name="BP04_2"
    ib1= np.loadtxt(folder+'BP04/oob/BP4_2_280_inband.txt', skiprows=1, usecols= (0,1))
    ib2= np.loadtxt(folder+'BP04/oob/BP4_2_320_inband.txt', skiprows=1, usecols= (0,1))
    ib3= np.loadtxt(folder+'BP04/oob/BP4_2_360_inband.txt', skiprows=1, usecols= (0,1))
    ib=np.concatenate((ib1[:-50], ib2[90:-50], ib3[67:]))
    oob_red=np.loadtxt(folder+'BP04/oob/BP4_2_390_OOB_oob.txt', skiprows=1, usecols=(0,1))
    oob_blue=np.column_stack((np.zeros(10), np.zeros(10))) #Dummy Value
    BP04= tx_gen(oob_blue, oob_red, ib, 292, 369, 200, 450)

    ## BP3_2 ##
    filt_name="BP03_2"
    ib1= np.loadtxt(folder+'BP03/oob/BP3_2_spatial_310_inband.txt', skiprows=1, usecols= (0,1))
    ib2= np.loadtxt(folder+'BP03/oob/BP3_2_spatial_350_inband.txt', skiprows=1, usecols= (0,1))
    ib3= np.loadtxt(folder+'BP03/oob/BP3_2_spatial_390_inband.txt', skiprows=1, usecols= (0,1))
    ib=np.concatenate((ib1[ib1[:,0]<330], ib2[(ib2[:,0]>330) & (ib2[:,0]<370)], ib3[ib3[:,0]>370]))
    oob_blue=np.loadtxt(folder+'BP03/oob/BP3_2_oob_269_oob.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BP03/oob/BP3_2_oob_427_oob.txt', skiprows=1, usecols= (0,1))
    BP03= tx_gen(oob_blue, oob_red, ib, 292, 407.5, 190, 450)

    ## NB7_2 ##
    filt_name="NB07_2"
    oob=np.loadtxt(folder+'NB07/oob/NB7_2_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB07/oob/NB7_2_inband.txt', skiprows=1, usecols=(0,1))
    NB07= tx_gen(oob, oob, ib, 384, 392, 255, 420)

    ## NB6_1 ##
    filt_name="NB06_1"
    oob=np.loadtxt(folder+'NB06/oob/NB6_1_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB06/oob/NB6_1_inband.txt', skiprows=1, usecols=(0,1))
    NB06= tx_gen(oob, oob, ib, 296, 303, 255, 400)

    ## NB5_3 ##
    filt_name="NB05_3"
    oob=np.loadtxt(folder+'NB05/oob/NB5_3_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB05/oob/NB5_3_inband.txt', skiprows=1, usecols=(0,1))
    NB05= tx_gen(oob, oob, ib, 280, 286, 250, 400)

    ## NB4_2 ##
    filt_name="NB04_2"
    oob=np.loadtxt(folder+'NB04/oob/NB4_2_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB04/oob/NB4_2_inband.txt', skiprows=1, usecols=(0,1))
    NB04= tx_gen(oob, oob, ib, 278, 283, 250, 400)

    ## NB3_2 ##
    filt_name="NB03_2"
    oob=np.loadtxt(folder+'NB03/oob/NB3_2_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB03/oob/NB3_2_inband.txt', skiprows=1, usecols=(0,1))
    NB03= tx_gen(oob, oob, ib, 278, 282, 255, 400)

    ## NB2A_7 ##
    filt_name="NB02A_7"
    oob=np.loadtxt(folder+'NB02/oob/NB2A_7_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB02/oob/NB2A_7_inband.txt', skiprows=1, usecols=(0,1))
    NB02= tx_gen(oob, oob, ib, 275, 279, 255, 400)
   
    #Combined Plots
    filt_name="NB01"; combined(NB01, BB01, int(NB01[1][0][0])+1, int(NB01[2][-1][0]), 5, 214)
    filt_name="NB02"; combined(NB02, BP02, int(NB02[1][0][0])+1, int(NB02[2][-1][0]), 1, 277)
    filt_name="NB03"; combined(NB03, BP02, int(NB03[1][0][0])+1, int(NB03[2][-1][0]), 1, 280.05)
    filt_name="NB04"; combined(NB04, BP02, int(NB04[1][0][0])+1, int(NB04[2][-1][0]), 1, 280.75)
    filt_name="NB05"; combined(NB05, BP02, int(NB05[1][0][0])+1, int(NB05[2][-1][0]), 1, 283.54)
    filt_name="NB06"; combined(NB06, BP03, int(NB06[1][0][0])+1, int(NB06[2][-1][0]), 1, 300)
    filt_name="NB07"; combined(NB07, BP03, int(NB07[1][0][0])+1, int(NB07[2][-1][0]), 1, 388)
    filt_name="BB01"; combined(BB01, BB01, int(BB01[1][0][0])+1, int(BB01[2][-1][0]), 5, BB01[0][int(len(BB01[0])/2)][0])
    filt_name="BB03"; combined(BB03, BP04, 293, int(BB03[2][-1][0]), 5, BB03[0][int(len(BB03[0])/2)][0])
    #BB02 is a special case as the blue end of the BB02 ib and oob_b spectra does not have
    #any overlap with the available BP04 spectra. Therefore, the central ib wl is forcefully
    #set to 295nm with a width of +-1nm.
    filt_name="BB02"; combined(BB02, BP04, 293, int(BB02[2][-1][0]), 1, 295)

