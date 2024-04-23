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

def tx_gen(oob_blue, oob_red, ib, ib_wl_mn, ib_wl_mx, oob_wl_mn, oob_wl_mx):
    '''
    Tx profile generator. Clips the provided ib and oob spectra to avoid
    overlaps during plotting.
    '''
    oob_blue= oob_blue[np.logical_and(oob_blue[:,0]>oob_wl_mn, oob_blue[:,0]<ib_wl_mn)]
    oob_red= oob_red[np.logical_and(oob_red[:,0]>ib_wl_mx, oob_red[:,0]<oob_wl_mx)]
    ib=ib[np.logical_and(ib[:,0]>ib_wl_mn, ib[:,0]<ib_wl_mx)]
    return(ib, oob_blue, oob_red)

def fill_interval(tx):
    '''
    picks the center of the tx spectrum and gives intervals within the +- fill range
    Input type: np array. 2 col. wl and tx.
    Returns: The array (x and y) that has to be integrated (for net tx measurement) or filled (in plots).
    '''
    fill_range= 5 #+- of this value will be filled
    if (len(tx)!=0):
        array=tx[(tx[:,0][int(len(tx)/2)]-fill_range<tx[:,0]) & (tx[:,0]<tx[:,0][int(len(tx)/2)]+fill_range)]
        #the array to be used for integration or shading the plot.
        return(array)

def plotter(ib, oob_blue, oob_red, limit):  
    plt.figure(filt_name, figsize=(6,4))
    plt.plot(oob_blue[:,0], oob_blue[:,1], color= '#1f77b4', label="Out of band")
    plt.plot(oob_red[:,0], oob_red[:,1], color= '#1f77b4')
    plt.plot(ib[:,0], ib[:,1], color='#ff7f0e', label="In band")
        
    plt.fill_between(fill_interval(ib)[:,0], fill_interval(ib)[:,1], y2=0, linewidth=0, color='orange', alpha=0.3)
    plt.fill_between(fill_interval(oob_red)[:,0], fill_interval(oob_red)[:,1], y2=0, linewidth=0, color='blue', alpha=0.3)
    if len(oob_blue != 0):
        plt.fill_between(fill_interval(oob_blue)[:,0], fill_interval(oob_blue)[:,1], y2=0, linewidth=0, color='blue', alpha=0.3)
    
    plt.yscale('log')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Transmission %')
    plt.axhline(y=limit, color='#2ca02c', label= "Acceptable limit")
    plt.title(filt_name+'_out_of_band')
    plt.legend()
    plt.grid()
    sav= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/science_filter_charactrerization_scripts/science_filter_plots_project/products/out_of_band/')
    if (save_figure == True): plt.savefig(sav+filt_name+"_out_of_band.pdf", dpi=300)
    plt.show()

def integrate(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt):
    ib_integrate= simpson(fill_interval(tx_ib_plt)[:,1], fill_interval(tx_ib_plt)[:,0])
    
    oob_red_integrate= simpson(fill_interval(tx_oob_r_plt)[:,1], fill_interval(tx_oob_r_plt)[:,0])
    oob_red_percent= oob_red_integrate*100/ib_integrate
   
    if (len(tx_oob_b_plt) != 0):
        oob_blue_integrate= simpson(fill_interval(tx_oob_b_plt)[:,1], fill_interval(tx_oob_b_plt)[:,0])
        oob_blue_percent= oob_blue_integrate*100/ib_integrate
    else:
        oob_blue_percent= -200
    print(f"{filt_name}\t |oob_b% {round(oob_blue_percent,2)}\t |oob_r% {round(oob_red_percent,2)}")
    


if __name__=='__main__':
    save_figure=False
    folder= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/science_filter_charactrerization_scripts/science_filter_plots_project/data/processed/')
   
    ## BP2_6 ##
    filt_name= "BP02_6"
    oob_blue=np.loadtxt(folder+'BP2/BP2_6_FM_Spatial_OOB/trans_profile/Trans_Profile_blue_249.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BP2/BP2_6_FM_Spatial_OOB/trans_profile/Trans_Profile_red_311.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'BP2/BP2_6_FM_Spatial_OOB/trans_profile/Trans_Profile_center.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob_blue, oob_red, ib, 268, 290, 190, 340)
    plotter(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt, 0.01)
    integrate(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt)
    
    ## BP3_2 ##
    filt_name="BP03_2"
    ib1= np.loadtxt(folder+'BP3/BP3_2_FM_Spatial_OOB/trans_profile/spatial_310/Trans_Profile_center.txt', skiprows=1, usecols= (0,1))
    ib2= np.loadtxt(folder+'BP3/BP3_2_FM_Spatial_OOB/trans_profile/spatial_350/Trans_Profile_center.txt', skiprows=1, usecols= (0,1))
    ib3= np.loadtxt(folder+'BP3/BP3_2_FM_Spatial_OOB/trans_profile/spatial_390/Trans_Profile_center.txt', skiprows=1, usecols= (0,1))
    ib=np.concatenate((ib1, ib2, ib3))
    oob_blue=np.loadtxt(folder+'BP3/BP3_2_FM_Spatial_OOB/trans_profile/Trans_Profile_oob_blue_269.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BP3/BP3_2_FM_Spatial_OOB/trans_profile/Trans_Profile_oob_red_427.txt', skiprows=1, usecols= (0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob_blue, oob_red, ib, 292, 407, 190, 450)
    plotter( tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt, 0.001)
    integrate(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt)

    ## BP4_2 ##
    filt_name="BP04_2"
    ib=np.loadtxt(folder+'BP4/BP4_2_QM_spatial_oob/trans_profile/BP4_2_qm_spatial.txt', skiprows=1, usecols=(0,1))
    oob_red=np.loadtxt(folder+'BP4/BP4_2_QM_spatial_oob/trans_profile/BP4_2_qm_oob.txt', skiprows=1, usecols=(0,1))
    oob_blue=np.vstack((np.arange(1,10,1), np.arange(1,10,1))) #Dummy Value
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob_blue, oob_red, ib, 292, 369, 200, 450)
    plotter(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt, 0.001)
    integrate(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt)

    ## BB1_3 ##
    filt_name="BB01_3"
    oob_blue=np.loadtxt(folder+'BB1/BB1_3_FM/trans_profile/Trans_Profile_oob_blue_190.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BB1/BB1_3_FM/trans_profile/Trans_Profile_oob_red_262.5.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'BB1/BB1_3_FM/trans_profile/Trans_Profile_center.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob_blue, oob_red, ib, 210, 245, 190, 300)
    plotter(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt, 0.01)
    integrate(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt)

    
    ## BB2_3 ##
    filt_name="BB02_3"
    ib1= np.loadtxt(folder+'BB2/BB2_3_FM_spatial_OOB/trans_profile/spatial_255/Trans_Profile_center.txt', skiprows=1, usecols= (0,1))
    ib2= np.loadtxt(folder+'BB2/BB2_3_FM_spatial_OOB/trans_profile/spatial_290/Trans_Profile_center.txt', skiprows=1, usecols= (0,1))
    ib2=ib2[np.logical_not(ib2[:,0]<276)]
    ib= np.concatenate((ib1, ib2))
    oob_blue=np.loadtxt(folder+'BB2/BB2_3_FM_spatial_OOB/trans_profile/Trans_Profile_oob_blue_299.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BB2/BB2_3_FM_spatial_OOB/trans_profile/Trans_Profile_oob_red_323.txt', skiprows=1, usecols= (0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob_blue, oob_red, ib, 245, 304, 190, 400)
    plotter(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt, 0.01)
    integrate(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt)

    ## BB3_3 ##
    filt_name="BB03_3"
    oob_blue=np.loadtxt(folder+'BB3/BB3_3_FM_spatial_OOB/trans_profile/Trans_Profile_oob_blue_299.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'BB3/BB3_3_FM_spatial_OOB/trans_profile/Trans_Profile_oob_red_380.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'BB3/BB3_3_FM_spatial_OOB/trans_profile/spatial/Trans_Profile_center.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob_blue, oob_red, ib, 318, 359, 292, 400)
    plotter(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt, 0.01)
    integrate(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt)

    ## NB1_2 ##
    filt_name="NB01_2"
    oob_blue=np.loadtxt(folder+'NB1/NB1_2_QM_spatial_oob/trans_profile/Trans_Profile_oob_blue_side_NB1_2.txt', skiprows=1, usecols= (0,1))
    oob_red=np.loadtxt(folder+'NB1/NB1_2_QM_spatial_oob/trans_profile/Trans_Profile_oob_red_side_NB1_2.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB1/NB1_2_QM_spatial_oob/trans_profile/Trans_Profile_center_NB1_2.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob_blue, oob_red, ib, 205, 230, 190, 400)
    plotter(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt, 0.01)
    integrate(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt)

    ## NB2A_7 ##
    filt_name="NB02A_7"
    oob=np.loadtxt(folder+'NB2A/NB2A_7_QM/trans_profile/Trans_Profile_OOB_NB2_7.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB2A/NB2A_7_QM/trans_profile/NB2A_7_qm_spatial.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob, oob, ib, 275, 279, 255, 400)
    plotter(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt, 0.01)
    integrate(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt)

    ## NB3_2 ##
    filt_name="NB03_2"
    oob=np.loadtxt(folder+'NB3/NB3_2_QM/trans_profile/NB3_2_qm_spatial_oob.txt', skiprows=1, usecols= (0,6))
    ib= np.loadtxt(folder+'NB3/NB3_2_QM/trans_profile/NB3_2_qm_spatial_oob.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob, oob, ib, 278, 282, 255, 400)
    plotter(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt, 0.01)
    integrate(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt)

    ## NB4_2 ##
    oob=np.loadtxt(folder+'NB4/NB4_2_QM/trans_profile/NB4_2_qm_spatial_oob.txt', skiprows=1, usecols= (0,6))
    ib= np.loadtxt(folder+'NB4/NB4_2_QM/trans_profile/NB4_2_qm_spatial_oob.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob, oob, ib, 278, 283, 250, 400)
    plotter(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt, 0.01)
    integrate(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt)

    ## NB5_3 ##
    filt_name="NB05_3"
    oob=np.loadtxt(folder+'NB5/NB5_3_QM/trans_profile/Trans_Profile_oob_NB5_3.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB5/NB5_3_QM/trans_profile/Trans_Profile_center_NB5_3.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob, oob, ib, 280, 286, 250, 400)
    plotter(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt, 0.01)
    integrate(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt)

    ## NB6_1 ##
    filt_name="NB06_1"
    oob=np.loadtxt(folder+'NB6/NB6_1_QM/trans_profile/trans_profile_oob_NB6_1.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB6/NB6_1_QM_tilt/trans_profile/Trans_Profile_Qm_tilt_0deg_vaccum_NB6_1.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob, oob, ib, 296, 303, 255, 400)
    plotter(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt, 0.01)
    integrate(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt)

    ## NB7_2 ##
    filt_name="NB07_2"
    oob=np.loadtxt(folder+'NB7/NB7_2_QM/trans_profile/trans_profile_oob_NB7_2.txt', skiprows=1, usecols= (0,1))
    ib= np.loadtxt(folder+'NB7/NB7_2_QM_tilt/trans_profile/Trans_Profile_Qm_tilt_0deg_vaccum_NB7_2.txt', skiprows=1, usecols=(0,1))
    tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt= tx_gen(oob, oob, ib, 384, 392, 255, 420)
    plotter(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt, 0.01)
    integrate(tx_ib_plt, tx_oob_b_plt, tx_oob_r_plt)



