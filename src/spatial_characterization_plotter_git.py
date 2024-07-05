#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 20:53:45 2023
Created to replot the data generated by Nidhi. 
The data should be air-to-vacuum shift corrected and should give absolute 
transmission values.

2023-12-27: Function added to measure deviation of spatial transmission spectra.
2023-05-20: Multiplotter function added. Used on newly generated data. Code rewritten
to make it compatible with newly generated data by JJ.
@author: janmejoy
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import os
import scienceplots

   
def plotter (filter_name, input_data, wl_mn, wl_mx, save_plot=None):
    data=input_data[np.logical_and(input_data[:,0]>wl_mn, input_data[:,0]<wl_mx)]
    with plt.style.context(['science','nature']):
        plt.figure(filter_name, figsize=(6,4))
        plt.tick_params(axis='both', which='major', labelsize=12)
        plt.plot(data[:,0], data[:,1], color= '#1f77b4')#, label= "Center")
        plt.plot(data[:,0], data[:,2], color='#ff7f0e')#, label= "Top")
        plt.plot(data[:,0], data[:,3], color='#2ca02c')#, label= "Left")
        plt.plot(data[:,0], data[:,4], color='#d62728')#, label= "Right")
        plt.plot(data[:,0], data[:,5], color='#9467bd')#, label= "Bottom")
        plt.title("Spatial transmission- "+filter_name, fontsize=12)
        plt.legend(["Center", "Left", "Right", "Top", "Bottom"], fontsize=12)
        plt.xlabel("Wavelength (nm)", fontsize=12)
        plt.ylabel("Transmission \%", fontsize=12)
        plt.grid(alpha=0.5)
        if save_plot==True: plt.savefig(os.path.join(folder,f'products/spatial/{filter_name}_spatial.pdf'), dpi=300)
        plt.show()

def multiplotter (filter_name, input_data_ls, wl_mn_ls, wl_mx_ls, save_plot=None):
    #For plots requiring multiple inputs to be concatenated for plotting.
    data= input_data_ls[0]
    if (len(input_data_ls) > 1):
        for i in range(1, len(input_data_ls)):
            data_interim=input_data_ls[i][np.logical_and(input_data_ls[i][:,0]>wl_mn_ls[i], input_data_ls[i][:,0]<wl_mx_ls[i])]
            data= np.concatenate((data, data_interim))
    with plt.style.context(['science','nature']):
        plt.figure(filter_name, figsize=(6,4))
        plt.tick_params(axis='both', which='major', labelsize=12)
        plt.plot(data[:,0], data[:,1], color= '#1f77b4')#, label= "Center")
        plt.plot(data[:,0], data[:,2], color='#ff7f0e')#, label= "Top")
        plt.plot(data[:,0], data[:,3], color='#2ca02c')#, label= "Left")
        plt.plot(data[:,0], data[:,4], color='#d62728')#, label= "Right")
        plt.plot(data[:,0], data[:,5], color='#9467bd')#, label= "Bottom")
        plt.title("Spatial transmission- "+filter_name, fontsize=12)
        plt.legend(["Center", "Left", "Right", "Top", "Bottom"], fontsize=12)
        plt.xlabel("Wavelength (nm)", fontsize=12)
        plt.ylabel("Transmission \%", fontsize=12)
        plt.grid(alpha=0.5)
        if save_plot==True: plt.savefig(os.path.join(folder,f'products/spatial/{filter_name}_spatial.pdf'), dpi=300)
        plt.show()

def deviation(filter_name, input_data, wl_min, wl_mx):
    data=input_data[np.logical_and(input_data[:,0]>wl_min, input_data[:,0]<wl_mx)]
    wl=data[:,0]
    tx_list=[data[:,1], data[:,2], data[:,3], data[:,4], data[:,5]]
    pos_list=["center","top","left","right","bottom"]
    wl_interp=np.linspace(wl[0], wl[-1], 100000)
    i=0
    wl_mx_ls=[]
    fwhm_ls=[]
    tx_mx_ls=[]
    print("\nXXXXXX", filter_name, "XXXXXX")
    print("Pos \t Max_tx_wl \t FWHM(nm)") #table head
    for tx in tx_list:
        interpolation=interp1d(wl, tx, kind='cubic')
        tx_interp=interpolation(wl_interp)
        tx_mx= np.max(tx_interp)
        wl_mx=wl_interp[np.where(tx_interp==tx_mx)][0]
        wl_half= wl_interp[np.where(tx_interp>=tx_mx/2)]
        fwhm= round(wl_half[-1]-wl_half[0], 3)
        print(pos_list[i],"\t", round(wl_mx, 3), "\t", fwhm) #"Position \t Max_tx_wl \t FWHM(nm)"
        plt.figure(pos_list[i])
        plt.plot(wl_interp, tx_interp)
        plt.axvline(wl_mx, color='black')
        plt.axvline(wl_half[0], color='red'); plt.axvline(wl_half[-1], color='red')
        plt.title(pos_list[i]+filter_name)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Transmission %")
        plt.grid()
        plt.show()
        i=i+1
        wl_mx_ls.append(wl_mx)
        fwhm_ls.append(fwhm)
        tx_mx_ls.append(tx_mx)
    
    print("tx_mx-- Mean, Std, %dev:", round(np.mean(tx_mx_ls), 2), round(np.std(tx_mx_ls), 2), round(np.std(tx_mx_ls)*100/np.mean(tx_mx_ls), 2))        
    print("mx_wl-- Mean, Std, %dev:", round(np.mean(wl_mx_ls),2), round(np.std(wl_mx_ls), 2), round(np.std(wl_mx_ls)*100/np.mean(wl_mx_ls), 2))       
    print("fwhm-- Mean, Std, %dev:", round(np.mean(fwhm_ls), 2), round(np.std(fwhm_ls), 2), round(np.std(fwhm_ls)*100/np.mean(fwhm_ls), 2))        
    

if __name__=='__main__':
    
    ### Plotting & deviation analysis ###
    folder=os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/science_filter_charactrerization_scripts/science_filter_plots_project/')
    
    # NB2A_7 #
    ftr_name= "NB02"
    file= f'{folder}data/processed/{ftr_name}/spatial/NB2A_7_spatial.txt' 
    wl_mn, wl_mx= 275, 279
    plotter(ftr_name, np.loadtxt(file, skiprows=1), wl_mn, wl_mx, save_plot=True)
    deviation(ftr_name, np.loadtxt(file, skiprows=1),  wl_mn, wl_mx)
    
    # NB3_3 #
    ftr_name= "NB03"
    file= f'{folder}data/processed/{ftr_name}/spatial/NB3_3_spatial.txt' 
    wl_mn, wl_mx= 278.5, 281.5
    plotter(ftr_name, np.loadtxt(file, skiprows=1), wl_mn, wl_mx, save_plot=True)
    deviation(ftr_name, np.loadtxt(file, skiprows=1),  wl_mn, wl_mx)
    
    # NB4_2 #
    ftr_name= "NB04"
    file= f'{folder}data/processed/{ftr_name}/spatial/NB4_2_spatial.txt' 
    wl_mn, wl_mx= 278.5, 283
    plotter(ftr_name, np.loadtxt(file, skiprows=1), wl_mn, wl_mx, save_plot=True)
    deviation(ftr_name, np.loadtxt(file, skiprows=1),  wl_mn, wl_mx)
    
    # NB5_4 #
    ftr_name= "NB05"
    file= f'{folder}data/processed/{ftr_name}/spatial/NB5_4_1200lpmm_500blaze_spatial.txt' 
    wl_mn, wl_mx= 280.5, 286
    plotter(ftr_name, np.loadtxt(file, skiprows=1), wl_mn, wl_mx, save_plot=True)
    deviation(ftr_name, np.loadtxt(file, skiprows=1),  wl_mn, wl_mx)
    
    # NB6_3 #
    ftr_name= "NB06"
    file= f'{folder}data/processed/{ftr_name}/spatial/NB6_3_spatial.txt' 
    wl_mn, wl_mx= 296, 304
    plotter(ftr_name, np.loadtxt(file, skiprows=1), wl_mn, wl_mx, save_plot=True)
    deviation(ftr_name, np.loadtxt(file, skiprows=1),  wl_mn, wl_mx)
    
    # NB7_1 #
    ftr_name= "NB07"
    file= f'{folder}data/processed/{ftr_name}/spatial/NB7_1_spatial.txt' 
    wl_mn, wl_mx= 385, 391
    plotter(ftr_name, np.loadtxt(file, skiprows=1), wl_mn, wl_mx, save_plot=True)
    deviation(ftr_name, np.loadtxt(file, skiprows=1),  wl_mn, wl_mx)
    
    # NB8_1 #
    ftr_name= "NB08"
    file= f'{folder}data/processed/{ftr_name}/spatial/NB8_1_spatial.txt' 
    wl_mn, wl_mx= 396.4, 397.3
    plotter(ftr_name, np.loadtxt(file, skiprows=1), wl_mn, wl_mx, save_plot=True)
    deviation(ftr_name, np.loadtxt(file, skiprows=1),  wl_mn, wl_mx)
    
    # NB8_2 #
    ftr_name= "NB08"
    file= f'{folder}data/processed/{ftr_name}/spatial/NB8_2_1200lpmm_500blaze_spatial.txt' 
    wl_mn, wl_mx= 396.4, 397.3
    plotter(ftr_name, np.loadtxt(file, skiprows=1), wl_mn, wl_mx, save_plot=True)
    deviation(ftr_name, np.loadtxt(file, skiprows=1),  wl_mn, wl_mx)
    
    # BB1_5 #
    ftr_name= "BB01"
    file= f'{folder}data/processed/{ftr_name}/spatial/BB1_5_inband_spatial.txt' 
    wl_mn, wl_mx= 100, 400
    plotter(ftr_name, np.loadtxt(file, skiprows=1), wl_mn, wl_mx, save_plot=True)
    
    # BB1_3 #
    ftr_name= "BB01"
    file= f'{folder}data/processed/{ftr_name}/spatial/BB1_3_spatial_spatial.txt' 
    wl_mn, wl_mx= 100, 400
    plotter(ftr_name, np.loadtxt(file, skiprows=1), wl_mn, wl_mx, save_plot=True)
    
    # BB3_3 #
    ftr_name= "BB03"
    file= f'{folder}data/processed/{ftr_name}/spatial/BB3_3_spatial_spatial.txt' 
    wl_mn, wl_mx= 100, 400
    plotter(ftr_name, np.loadtxt(file, skiprows=1), wl_mn, wl_mx, save_plot=True)
    
    # NB1_1 #
    ftr_name= "NB01"
    file1= f'{folder}data/processed/{ftr_name}/spatial/NB1_1_spatial_214_spatial.txt' 
    wl_mn1, wl_mx1= 180, 400
    file2= f'{folder}data/processed/{ftr_name}/spatial/NB1_1_spatial_254_spatial.txt' 
    wl_mn2, wl_mx2= 180, 400
    multiplotter (ftr_name, [np.loadtxt(file1, skiprows=1), np.loadtxt(file2, skiprows=1)], [wl_mn1, wl_mn2], [wl_mx1, wl_mx2], save_plot=True)

    # BB2_3 #
    ftr_name= "BB02"
    file1= f'{folder}data/processed/{ftr_name}/spatial/BB2_3_spatial_255nm_spatial.txt' 
    wl_mn1, wl_mx1= 200, 400
    file2= f'{folder}data/processed/{ftr_name}/spatial/BB2_3_spatial_290nm_spatial.txt' 
    wl_mn2, wl_mx2=  276, 400
    multiplotter (ftr_name, [np.loadtxt(file1, skiprows=1), np.loadtxt(file2, skiprows=1)], [wl_mn1, wl_mn2], [wl_mx1, wl_mx2], save_plot=True)
    
    # BP2_8 #
    ftr_name= "BP02"
    file1= f'{folder}data/processed/{ftr_name}/spatial/BP2_8_262-282_spatial.txt' 
    wl_mn1, wl_mx1= 265, 275
    file2= f'{folder}data/processed/{ftr_name}/spatial/BP2_8_278-297_spatial.txt' 
    wl_mn2, wl_mx2= 282, 295
    multiplotter (ftr_name, [np.loadtxt(file1, skiprows=1), np.loadtxt(file2, skiprows=1)], [wl_mn1, wl_mn2], [wl_mx1, wl_mx2], save_plot=True)

    # BP3_2 #
    ftr_name= "BP03"
    file1= f'{folder}data/processed/{ftr_name}/spatial/BP3_2_spatial_310_spatial.txt' 
    wl_mn1, wl_mx1= 200, 400
    file2= f'{folder}data/processed/{ftr_name}/spatial/BP3_2_spatial_350_spatial.txt' 
    wl_mn2, wl_mx2= 200, 400
    file3= f'{folder}data/processed/{ftr_name}/spatial/BP3_2_spatial_390_spatial.txt'
    wl_mn3, wl_mx3= 200, 500
    multiplotter (ftr_name, [np.loadtxt(file1, skiprows=1), np.loadtxt(file2, skiprows=1), np.loadtxt(file3, skiprows=1)], 
                  [wl_mn1, wl_mn2, wl_mn3], [wl_mx1, wl_mx2, wl_mx3], save_plot=True)

    # BP4_4 #
    ftr_name= "BP04"
    file1= f'{folder}data/processed/{ftr_name}/spatial/BP4_4_spatial_270_spatial.txt' 
    wl_mn1, wl_mx1= 200, 400
    file2= f'{folder}data/processed/{ftr_name}/spatial/BP4_4_spatial_310_spatial.txt' 
    wl_mn2, wl_mx2= 200, 400
    file3= f'{folder}data/processed/{ftr_name}/spatial/BP4_4_spatial_350_spatial.txt'
    wl_mn3, wl_mx3= 200, 500
    multiplotter (ftr_name, [np.loadtxt(file1, skiprows=1), np.loadtxt(file2, skiprows=1), np.loadtxt(file3, skiprows=1)], 
                  [wl_mn1, wl_mn2, wl_mn3], [wl_mx1, wl_mx2, wl_mx3], save_plot=True)
