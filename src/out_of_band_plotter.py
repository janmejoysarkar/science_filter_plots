#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 14:48:31 2023

@author: janmejoy

-Created to plot the OOB tx of science filters with inband at 0deg angle of
incidence.

-2023-11-15
-2023-12-15
-2024-04-23: Modification made to project form.
-2024-09-26: Code changed to use relative transmission instead of %tx.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.integrate import simpson
import scienceplots


def tx_gen(oob_blue, oob_red, ib, ib_wl_mn, ib_wl_mx, oob_wl_mn, oob_wl_mx):
    '''
    Tx profile generator. Clips the provided ib and oob spectra to avoid
    The effective fill width is 2*fill_range around center wavelength.
    overlaps during plotting.
    Relative transmission introduced.
    '''
    oob_blue= oob_blue[np.logical_and(oob_blue[:,0]>oob_wl_mn, oob_blue[:,0]<ib_wl_mn)]
    oob_red= oob_red[np.logical_and(oob_red[:,0]>ib_wl_mx, oob_red[:,0]<oob_wl_mx)]
    ib=ib[np.logical_and(ib[:,0]>ib_wl_mn, ib[:,0]<ib_wl_mx)]
    ib[:,1], oob_blue[:,1], oob_red[:,1] =ib[:,1], oob_blue[:,1], oob_red[:,1]  
    return(ib, oob_blue, oob_red)

def plotter(filt_name, ib, oob_blue, oob_red, limit, fill_ib, fill_oob_r, fill_oob_b):  
    with plt.style.context(['science', 'nature']):
        plt.figure(filt_name, figsize=(6,4))
        plt.plot(oob_blue[:,0], oob_blue[:,1], color= 'black', label="Out of band")
        plt.plot(oob_red[:,0], oob_red[:,1], color= 'black')
        plt.plot(ib[:,0], ib[:,1], color='red', label="In band")
        plt.fill_between(fill_ib[:,0],fill_ib[:,1], y2=0, linewidth=0, color='red', alpha=0.2)
        plt.fill_between(fill_oob_r[:,0], fill_oob_r[:,1], y2=0, linewidth=0, color='black', alpha=0.2)
        if len(oob_blue != 0):
            plt.fill_between(fill_oob_b[:,0], fill_oob_b[:,1], y2=0, linewidth=0, color='black', alpha=0.2)
        plt.tick_params(axis='both', which='major', labelsize=12)
        plt.yscale('log')
        plt.xlabel('Wavelength (nm)', fontsize=12)
        plt.ylabel('Relative Transmission (log scale)', fontsize=12)
        #plt.axhline(y=limit, color='#2ca02c', label= "Acceptable limit")
        plt.title(filt_name+'_out_of_band', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(alpha=0.5)
        sav= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/science_filter_charactrerization_scripts/science_filter_plots_project/products/out_of_band/')
        if (SAVE == True): plt.savefig(sav+filt_name+"_out_of_band.pdf", dpi=300)
        if SHOW: plt.show()
        if not SHOW: plt.close()

def fill_interval(tx, fill_range, cent=None):
    '''
    picks the center of the tx spectrum and gives intervals within the +- fill range
    
    Input: tx: np array. 2 col. wl and tx; fill_range: +- 
    of this value will be filled.
    Returns: The array (x and y) that has to be integrated 
    (for net tx measurement) or filled (in plots).
    '''
    if len(tx)!=0:
        if cent==None: cent= tx[:,0][int(len(tx)/2)] #cent= tx[:,0][np.where (tx[:,1]==np.max(tx[:,1]))]
        array=tx[(cent-fill_range<tx[:,0]) & (tx[:,0]<cent+fill_range)]
        #the array to be used for integration or shading the plot.
        return array

def integrate(fill_ib, fill_oob_r, fill_oob_b):
    '''
    Integrates the curve under the fill regions.
    Compares the integrated out of band flux with inband flux.
    '''
    ib_integrate= simpson(fill_ib[:,1], x=fill_ib[:,0])
    oob_red_integrate= simpson(fill_oob_r[:,1], x=fill_oob_r[:,0])
    oob_red_percent= oob_red_integrate*100/ib_integrate
    if fill_oob_b is not None:
        oob_blue_integrate= simpson(fill_oob_b[:,1], x=fill_oob_b[:,0])
        oob_blue_percent= oob_blue_integrate*100/ib_integrate
    else:
        oob_blue_percent= -200
    print(f"{filt_name}\t |oob_b% {(oob_blue_percent):.2e}\t |oob_r% {(oob_red_percent):.2e}")
    
def wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, oob_limit, fill_range, cent=None):
    fill_ib, fill_oob_r, fill_oob_b= fill_interval(tx_ib_plt, fill_range, cent), fill_interval(tx_oob_r_plt, fill_range), fill_interval(tx_oob_b_plt, fill_range) 
    plotter(filt_name, tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt,oob_limit, fill_ib, fill_oob_r, fill_oob_b)
    integrate(fill_ib, fill_oob_r, fill_oob_b)


if __name__=='__main__':
    SHOW, SAVE=True, True
    project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/science_filter_charactrerization_scripts/science_filter_plots_project/') 
    folder= os.path.join(project_path, 'data/processed/')
    print("OOB %tx wrt IB")

    ## NB1_2 ##
    filt_name="NB01"
    oob_blue=np.loadtxt(folder+'NB01/oob/NB1_2_oob_blue_oob.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'NB01/oob/NB1_2_oob_red_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB01/oob/NB1_2_inband_inband.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob_blue, oob_red, ib, 205, 230, 190, 400)
    wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, 1e-4, 5, 214)

    ## BB3_3 ##
    filt_name="BB03"
    oob_blue=np.loadtxt(folder+'BB03/oob/BB3_3_oob_299nm_oob.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BB03/oob/BB3_3_oob_380nm_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'BB03/oob/BB3_3_spatial_inband.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob_blue, oob_red, ib, 318, 359, 292, 400)
    wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, 1e-4, 5)

    ## BB2_3 ##
    filt_name="BB02"
    ib1= np.loadtxt(folder+'BB02/oob/BB2_3_spatial_255nm_inband.txt', skiprows=1, usecols= (0,1))
    ib2= np.loadtxt(folder+'BB02/oob/BB2_3_spatial_290nm_inband.txt', skiprows=1, usecols= (0,1))
    ib2=ib2[np.logical_not(ib2[:,0]<276.8)]
    ib= np.concatenate((ib1, ib2))
    oob_blue=np.loadtxt(folder+'BB02/oob/BB2_3_oob_229nm_oob.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BB02/oob/BB2_3_oob_323nm_oob.txt', skiprows=1, usecols= (0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob_blue, oob_red, ib, 245, 304, 190, 400)
    wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, 1e-4, 5)

    ## BB1_3 ##
    filt_name="BB01"
    oob_blue=np.loadtxt(folder+'BB01/oob/BB1_3_oob_190_oob.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BB01/oob/BB1_3_oob_262.5_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'BB01/oob/BB1_3_spatial_inband.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob_blue, oob_red, ib, 210, 245, 190, 300)
    wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, 1e-4, 5)

    ## BP2_6 ##
    filt_name= "BP02"
    oob_blue=np.loadtxt(folder+'BP02/oob/BP2_8_252-272_OOB_oob.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BP02/oob/BP2_8_290-310_OOB_oob.txt', skiprows=1, usecols= (0,1))
    ib1= np.loadtxt(folder+'BP02/oob/BP2_8_262-282_inband.txt', skiprows=1, usecols= (0,1))
    ib2= np.loadtxt(folder+'BP02/oob/BP2_8_278-297_inband.txt', skiprows=1, usecols= (0,1))
    ib=np.concatenate((ib1[:-300], ib2[90:]))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob_blue, oob_red, ib, 268, 290, 190, 340)
    wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, 1e-4, 5)
    
    ## BP4_2 ##
    filt_name="BP04"
    ib1= np.loadtxt(folder+'BP04/oob/BP4_2_280_inband.txt', skiprows=1, usecols= (0,1))
    ib2= np.loadtxt(folder+'BP04/oob/BP4_2_320_inband.txt', skiprows=1, usecols= (0,1))
    ib3= np.loadtxt(folder+'BP04/oob/BP4_2_360_inband.txt', skiprows=1, usecols= (0,1))
    ib=np.concatenate((ib1[:-50], ib2[90:-50], ib3[67:]))
    oob_red=np.loadtxt(folder+'BP04/oob/BP4_2_390_OOB_oob.txt', skiprows=1, usecols=(0,1))
    oob_blue=np.vstack((np.arange(1,10,1), np.arange(1,10,1))) #Dummy Value
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob_blue, oob_red, ib, 292, 369, 200, 450)
    wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, 1e-5, 5)
    
    ## BP3_2 ##
    filt_name="BP03"
    ib1= np.loadtxt(folder+'BP03/oob/BP3_2_spatial_310_inband.txt', skiprows=1, usecols= (0,1))
    ib2= np.loadtxt(folder+'BP03/oob/BP3_2_spatial_350_inband.txt', skiprows=1, usecols= (0,1))
    ib3= np.loadtxt(folder+'BP03/oob/BP3_2_spatial_390_inband.txt', skiprows=1, usecols= (0,1))
    ib=np.concatenate((ib1[ib1[:,0]<330], ib2[(ib2[:,0]>330) & (ib2[:,0]<370)], ib3[ib3[:,0]>370]))
    oob_blue=np.loadtxt(folder+'BP03/oob/BP3_2_oob_269_oob.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BP03/oob/BP3_2_oob_427_oob.txt', skiprows=1, usecols= (0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob_blue, oob_red, ib, 292, 407.5, 190, 450)
    wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, 1e-5, 5)

    ## NB7_2 ##
    filt_name="NB07"
    oob=np.loadtxt(folder+'NB07/oob/NB7_2_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB07/oob/NB7_2_inband.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob, oob, ib, 384, 392, 255, 420)
    wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, 1e-4, 1, 388)

    ## NB6_1 ##
    filt_name="NB06"
    oob=np.loadtxt(folder+'NB06/oob/NB6_1_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB06/oob/NB6_1_inband.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob, oob, ib, 296, 303, 255, 400)
    wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, 1e-4, 1, 300)

    ## NB5_3 ##
    filt_name="NB05"
    oob=np.loadtxt(folder+'NB05/oob/NB5_3_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB05/oob/NB5_3_inband.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob, oob, ib, 280, 286, 250, 400)
    wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, 1e-4, 1, 283.54)

    ## NB4_2 ##
    filt_name="NB04"
    oob=np.loadtxt(folder+'NB04/oob/NB4_2_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB04/oob/NB4_2_inband.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob, oob, ib, 278, 283, 250, 400)
    wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, 1e-4, 1, 280.75)

    ## NB3_2 ##
    filt_name="NB03"
    oob=np.loadtxt(folder+'NB03/oob/NB3_2_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB03/oob/NB3_2_inband.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob, oob, ib, 278, 282, 255, 400)
    wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, 1e-4, 1, 280.05)

    ## NB2A_7 ##
    filt_name="NB02"
    oob=np.loadtxt(folder+'NB02/oob/NB2A_7_oob.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB02/oob/NB2A_7_inband.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob, oob, ib, 275, 279, 255, 400)
    wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, 1e-4, 1, 277)
