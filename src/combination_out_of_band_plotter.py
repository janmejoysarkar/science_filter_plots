#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 14:48:31 2023

@author: janmejoy

-Created to plot the OOB tx of science filters with inband at 0deg angle of
incidence.
-Data is in wl vs tx% form.
-2024-04-23: Modification made to project form.

Modification log
--Nov 15 2023
--Dec 15 2023
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
        plt.ylabel('Transmission \%', fontsize=12)
        plt.axhline(y=limit, color='#2ca02c', label= "Acceptable limit")
        plt.title(filt_name+'_out_of_band', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(alpha=0.5)
        sav= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/science_filter_charactrerization_scripts/science_filter_plots_project/products/out_of_band/')
        if (save_figure == True): plt.savefig(sav+filt_name+"_out_of_band.pdf", dpi=300)
        plt.show()
    
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
    ib_integrate= simpson(fill_ib[:,1],x=fill_ib[:,0])
    oob_red_integrate= simpson(fill_oob_r[:,1], x=fill_oob_r[:,0])
    oob_red_percent= oob_red_integrate*100/ib_integrate
    if fill_oob_b is not None:
        oob_blue_integrate= simpson(fill_oob_b[:,1], x=fill_oob_b[:,0])
        oob_blue_percent= oob_blue_integrate*100/ib_integrate
    else:
        oob_blue_percent= -200
    print(f"{filt_name}\t |oob_b% {round(oob_blue_percent,2)}\t |oob_r% {round(oob_red_percent,2)}")
    
def wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, oob_limit, fill_range, cent=None):
    fill_ib, fill_oob_r, fill_oob_b= fill_interval(tx_ib_plt, fill_range, cent), fill_interval(tx_oob_r_plt, fill_range), fill_interval(tx_oob_b_plt, fill_range) 
    plotter(filt_name, tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt,oob_limit, fill_ib, fill_oob_r, fill_oob_b)
    integrate(fill_ib, fill_oob_r, fill_oob_b)

def combined(FILT1, FILT2, lamda1, lamda2, fill_width, cent=None):
    '''
    - Concatenates OOB and IB profiles to make it into one curve.
    - Performs linear interpolation to get the interpolated graph in
    steps of 0.01 nm.
    - Returns > Integration ratios taken from integrate function
              > Plots
    '''

    concatenated_1= np.concatenate((FILT1[1], FILT1[0], FILT1[2]))
    x_new= np.arange(lamda1, lamda2, 0.01)#USER INPUT NEEDED
    fn= interp1d(concatenated_1[:,0], concatenated_1[:,1])
    y_new_1= fn(x_new)
    if len(FILT2[1])!= 0:
        concatenated_2= np.concatenate((FILT2[1], FILT2[0], FILT2[2]))
    else:
        concatenated_2= np.concatenate((FILT2[0], FILT2[2]))
    fn= interp1d(concatenated_2[:,0], concatenated_2[:,1])
    y_new_2= fn(x_new)
    
    final= np.column_stack((x_new, y_new_1*y_new_2))

    fill_ib= fill_interval(final, fill_width, cent)
    fill_oob_b= fill_interval(final, fill_width, FILT1[1][int(len(FILT1[1])/2)][0])
    fill_oob_r= fill_interval(final, fill_width, FILT1[2][int(len(FILT1[2])/2)][0])
    integrate(fill_ib, fill_oob_r, fill_oob_b)
    
    with plt.style.context(['science', 'nature']):
        plt.figure(figsize=(6,4))
        plt.plot(final[:,0], final[:,1], color= 'black', label="Out of band")
        plt.fill_between(fill_ib[:,0],fill_ib[:,1], y2=0, linewidth=0, color='red', alpha=0.2)
        plt.fill_between(fill_oob_r[:,0], fill_oob_r[:,1], y2=0, linewidth=0, color='black', alpha=0.2)
        plt.fill_between(fill_oob_b[:,0], fill_oob_b[:,1], y2=0, linewidth=0, color='black', alpha=0.2)
        plt.yscale('log')
        plt.xlabel('Wavelength (nm)', fontsize=12)
        plt.ylabel('Transmission \%', fontsize=12)
        plt.title(filt_name+'_out_of_band', fontsize=12)
        plt.grid(alpha=0.5)
        plt.show()

if __name__=='__main__':
    save_figure=False
    project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/science_filter_charactrerization_scripts/science_filter_plots_project/') 
    folder= os.path.join(project_path, 'data/processed/')
    print("OOB %tx wrt IB")
    #tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt
    
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
    ib2=ib2[np.logical_not(ib2[:,0]<276)]
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
    ib=np.concatenate((ib1[:-300], ib2))
    BP02= tx_gen(oob_blue, oob_red, ib, 268, 290, 190, 340)

    ## BP4_2 ##
    filt_name="BP04_2"
    ib1= np.loadtxt(folder+'BP04/oob/BP4_2_280_inband.txt', skiprows=1, usecols= (0,1))
    ib2= np.loadtxt(folder+'BP04/oob/BP4_2_320_inband.txt', skiprows=1, usecols= (0,1))
    ib3= np.loadtxt(folder+'BP04/oob/BP4_2_360_inband.txt', skiprows=1, usecols= (0,1))
    ib=np.concatenate((ib1, ib2, ib3))
    oob_red=np.loadtxt(folder+'BP04/oob/BP4_2_390_OOB_oob.txt', skiprows=1, usecols=(0,1))
    oob_blue=np.column_stack((np.zeros(10), np.zeros(10))) #Dummy Value
    BP04= tx_gen(oob_blue, oob_red, ib, 292, 369, 200, 450)

    ## BP3_2 ##
    filt_name="BP03_2"
    ib1= np.loadtxt(folder+'BP03/oob/BP3_2_spatial_310_inband.txt', skiprows=1, usecols= (0,1))
    ib2= np.loadtxt(folder+'BP03/oob/BP3_2_spatial_350_inband.txt', skiprows=1, usecols= (0,1))
    ib3= np.loadtxt(folder+'BP03/oob/BP3_2_spatial_390_inband.txt', skiprows=1, usecols= (0,1))
    ib=np.concatenate((ib1, ib2, ib3))
    oob_blue=np.loadtxt(folder+'BP03/oob/BP3_2_oob_269_oob.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BP03/oob/BP3_2_oob_427_oob.txt', skiprows=1, usecols= (0,1))
    BP03= tx_gen(oob_blue, oob_red, ib, 292, 407, 190, 450)

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
    #wrapper(tx_ib_plt, tx_oob_r_plt, tx_oob_b_plt, 0.01, 1, 277)
   
    #Combined Plots
    filt_name="NB01"; combined(NB01, BB01, int(NB01[1][0][0])+1, int(NB01[2][-1][0]), 5, 214)
    filt_name="NB02"; combined(NB02, BP02, int(NB02[1][0][0])+1, int(NB02[2][-1][0]), 1, 277)
    filt_name="NB03"; combined(NB03, BP02, int(NB03[1][0][0])+1, int(NB03[2][-1][0]), 1, 280.05)
    filt_name="NB04"; combined(NB04, BP02, int(NB04[1][0][0])+1, int(NB04[2][-1][0]), 1, 280.75)
    filt_name="NB05"; combined(NB05, BP02, int(NB05[1][0][0])+1, int(NB05[2][-1][0]), 1, 283.54)
    filt_name="NB06"; combined(NB06, BP03, int(NB06[1][0][0])+1, int(NB06[2][-1][0]), 1, 300)
    filt_name="NB07"; combined(NB07, BP03, int(NB07[1][0][0])+1, int(NB07[2][-1][0]), 1, 388)
    filt_name="BB01"; combined(BB01, BB01, int(BB01[1][0][0])+1, int(BB01[2][-1][0]), 5, cent=None)
    filt_name="BB03"; combined(BB03, BP04, 293, int(BB03[2][-1][0]), 5, cent=None)
    #filt_name="BB02"; combined(BB02, BP04, 293, int(BB02[2][-1][0]), 5, cent=None)

    '''

    191, 256,
    256, 298,
    270, 288,
    272, 289,
    262, 304,
    279, 321,
    368, 408,
    191, 284,
    '''
