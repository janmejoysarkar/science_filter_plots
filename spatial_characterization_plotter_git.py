#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 20:53:45 2023
Created to replot the data generated by Nidhi. 
The data should be air-to-vacuum shift corrected and should give absolute 
transmission values.

@author: janmejoy
"""
import matplotlib.pyplot as plt
import numpy as np
import glob
from scipy.optimize import curve_fit

#### Concatenator takes all the single files for spatial transmission and
#### combines them into one file.

def concatenator(save_name, folder):
    ls= "*center*", "*top*", "*left*", "*right*", "*bottom*"
    
    wl= np.loadtxt(glob.glob(folder+ls[0])[0])[:,0]
    center= np.loadtxt(glob.glob(folder+ls[0])[0])[:,1]
    top= np.loadtxt(glob.glob(folder+ls[1])[0])[:,1]
    left= np.loadtxt(glob.glob(folder+ls[2])[0])[:,1]
    right= np.loadtxt(glob.glob(folder+ls[3])[0])[:,1]
    bottom= np.loadtxt(glob.glob(folder+ls[4])[0])[:,1]
    
    stack=np.column_stack((wl, center, top, left, right, bottom))
    #np.savetxt(folder+save_name, stack, delimiter=' ', newline='\n')
    
#### Plotter takes a single spatial transmission file and plots it.
   
def plotter (filter_name, input_data, wl_min, wl_mx):
    data=input_data[np.logical_and(input_data[:,0]>wl_min, input_data[:,0]<wl_mx)]
    plt.figure(filter_name, figsize=(6,4))
    plt.plot(data[:,0], data[:,1], color= '#1f77b4')#, label= "Center")
    plt.plot(data[:,0], data[:,2], color='#ff7f0e')#, label= "Top")
    plt.plot(data[:,0], data[:,3], color='#2ca02c')#, label= "Left")
    plt.plot(data[:,0], data[:,4], color='#d62728')#, label= "Right")
    plt.plot(data[:,0], data[:,5], color='#9467bd')#, label= "Bottom")
    plt.title("Spatial transmission- "+filter_name)
    plt.legend(["Center", "Top", "Left", "Right", "Bottom"])
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Transmission %")
    plt.grid()
    #plt.savefig("/home/janmejoy/Documents/"+filter_name+"_spatial.png", dpi=300)
    plt.show()

def gauss (x, a, x0, sig):
    return a*np.exp(-(x-x0)**2/2*sig**2)

'''

### Max finder ###
def gauss_fit (filter_name, input_data, wl_min, wl_mx):
    data=input_data[np.logical_and(input_data[:,0]>wl_min, input_data[:,0]<wl_mx)]
    fit1, fit2= curve_fit(gauss, data[:,0], data[:,1], p0=(0.2, ((wl_mx+wl_min)/2), 0.5))
    print(fit1)
    y_fit= gauss(data[:,0], *fit1)
    plt.plot(data[:,0], data[:,1])#, label= "Center")
    plt.scatter(data[:,0][np.where(data[:,1]==np.max(data[:,1]))], np.max(data[:,1]))
    print(data[:,0][np.where(data[:,1]==np.max(data[:,1]))])
    #plt.plot(data[:,0], y_fit)
    plt.show()

#columns are wl, tx_c, tx_t, tx_l, tx_r, tx_b
folder="/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/"

# NB2A_7 #
file= folder+ 'NB2A/NB2A_7_QM/trans_profile/NB2A_7_qm_spatial.txt' 
#plotter("NB2A_7", np.loadtxt(file, skiprows=1), 275, 279)
gauss_fit("NB2A_7", np.loadtxt(file, skiprows=1), 276.8, 277.2)
'''

'''
# NB5_4 #
save_name="NB5_4_fm_spatial.txt"
folder="/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/NB5/NB5_4_FM_spatial/trans_profile/"
concatenator(save_name, folder)

# NB8_2 #
save_name="NB8_2_fm_spatial.txt"
folder="/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/NB8/NB8_2_FM_spatial/trans_profile/"
concatenator(save_name, folder)

# NB2A_7 #
save_name="NB2A_7_qm_spatial.txt"
folder="/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/NB2A/NB2A_7_QM/trans_profile/"
concatenator(save_name, folder)

# BB1_5 #
save_name= "BB1_5_fm_spatial.txt"
folder= "/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/BB1/BB1_5_QM/trans_profile/"
concatenator(save_name, folder)

# BB1_3 #
save_name= "BB1_3_fm_spatial.txt"
folder= "/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/BB1/BB1_3_FM/trans_profile/"
concatenator(save_name, folder)

# BB3_3 #
save_name= "BB3_3_fm_spatial.txt"
folder= "/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/BB3/BB3_3_FM_spatial_OOB/trans_profile/spatial/"
concatenator(save_name, folder)

# BP3_2 #
save_name= "BP3_2_fm_spatial_310.txt"
folder= "/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/BP3/BP3_2_FM_Spatial_OOB/trans_profile/spatial_310/"
concatenator(save_name, folder)
save_name= "BP3_2_fm_spatial_350.txt"
folder= "/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/BP3/BP3_2_FM_Spatial_OOB/trans_profile/spatial_350/"
concatenator(save_name, folder)
save_name= "BP3_2_fm_spatial_390.txt"
folder= "/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/BP3/BP3_2_FM_Spatial_OOB/trans_profile/spatial_390/"
concatenator(save_name, folder)

# BP4_4 #
save_name= "BP4_4_fm_spatial_270.txt"
folder= "/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/BP4/BP4_4_FM_spatial/trans_profile/spatial_270/"
concatenator(save_name, folder)
save_name= "BP4_4_fm_spatial_310.txt"
folder= "/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/BP4/BP4_4_FM_spatial/trans_profile/spatial_310/"
concatenator(save_name, folder)
save_name= "BP4_4_fm_spatial_350.txt"
folder= "/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/BP4/BP4_4_FM_spatial/trans_profile/spatial_350/"
concatenator(save_name, folder)

# NB1_1 #
save_name= "NB1_1_fm_spatial_214.txt"
folder= "/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/NB1/NB1_1_FM_spatial/trans_profile/NB1_1_spatial_214/"
concatenator(save_name, folder)
save_name= "NB1_1_fm_spatial_254.txt"
folder= "/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/NB1/NB1_1_FM_spatial/trans_profile/NB1_1_spatial_254/"
concatenator(save_name, folder)

# BB2_3 # 
save_name= "BB2_3_fm_spatial_255.txt"
folder= "/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/BB2/BB2_3_FM_spatial_OOB/trans_profile/spatial_255/"
concatenator(save_name, folder)
save_name= "BB2_3_fm_spatial_290.txt"
folder= "/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/BB2/BB2_3_FM_spatial_OOB/trans_profile/spatial_290/"
concatenator(save_name, folder)
'''
#####################################################################

### Plotting ###
    
folder="/home/janmejoy/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/results/filter_data_compiled/"
'''
# NB2A_7 #
file= folder+ 'NB2A/NB2A_7_QM/trans_profile/NB2A_7_qm_spatial.txt' 
plotter("NB2A_7", np.loadtxt(file, skiprows=1), 275, 279)

# NB3_3 #
file= folder+'NB3/NB3_3_FM/trans_profile/NB3_3_fm_spatial.txt'
plotter("NB3_3", np.loadtxt(file, skiprows=1), 278.5, 281.5)

# NB4_2 #
file= folder+ 'NB4/NB4_2_QM/trans_profile/NB4_2_qm_spatial_oob.txt'
plotter("NB4_2", np.loadtxt(file, skiprows=1), 278.5, 283)''

# NB5_4 #
file= folder+'NB5/NB5_4_FM_spatial/trans_profile/NB5_4_fm_spatial.txt'
plotter("NB5_4", np.loadtxt(file, skiprows=1), 280.5, 286)

# NB6_3 #
file= folder+ 'NB6/NB6_3_spatial_FM/trans_profile/NB6_3_fm_spatial.txt'
plotter("NB6_3", np.loadtxt(file, skiprows=1), 296, 304)

# NB7_1 #
file= folder+ 'NB7/NB7_1_FM/trans_profile/NB7_1_fm_spatial.txt'
plotter("NB7_1", np.loadtxt(file, skiprows=1), 385, 391)

# NB8_1 #
file= folder+ 'NB8/NB8_1_spatial/trans_profile/NB8_1_qm_spatial_oob.txt'
plotter("NB8_1", np.loadtxt(file, skiprows=1), 396.25, 397.25)

# NB8_2 #
file= folder+ 'NB8/NB8_2_FM_spatial/trans_profile/NB8_2_fm_spatial.txt'
plotter("NB8_2", np.loadtxt(file, skiprows=1), 396.25, 397.25)

# BB1_5 #
file= folder+'BB1/BB1_5_QM/trans_profile/BB1_5_fm_spatial.txt'
plotter("BB1_5", np.loadtxt(file, skiprows=1), 100, 400)

# BB1_3 #
file= folder+'BB1/BB1_3_FM/trans_profile/BB1_3_fm_spatial.txt'
plotter("BB1_3", np.loadtxt(file, skiprows=1), 100, 400)

# BB3_3 #
file= folder+"BB3/BB3_3_FM_spatial_OOB/trans_profile/spatial/BB3_3_fm_spatial.txt"
plotter("BB3_3", np.loadtxt(file, skiprows=1), 100, 400)

# BP2_8 #
file= folder+"BP2/BP2_8_Qm/trans_profile/BP2_8_qm_spatial.txt"
plotter("BP2_8", np.loadtxt(file, skiprows=1), 265, 295)

# BP3_2 #
file= folder+"BP3/BP3_2_FM_Spatial_OOB/trans_profile/spatial_310/BP3_2_fm_spatial_310.txt"
plotter("BP3_2", np.loadtxt(file, skiprows=1), 200, 400)

file= folder+"BP3/BP3_2_FM_Spatial_OOB/trans_profile/spatial_350/BP3_2_fm_spatial_350.txt"
plotter("BP3_2", np.loadtxt(file, skiprows=1), 200, 400)

file= folder+"BP3/BP3_2_FM_Spatial_OOB/trans_profile/spatial_390/BP3_2_fm_spatial_390.txt"
plotter("BP3_2", np.loadtxt(file, skiprows=1), 200, 500)

# BP4_4 #
file= folder+"BP4/BP4_4_FM_spatial/trans_profile/spatial_270/BP4_4_fm_spatial_270.txt"
plotter("BP4_4", np.loadtxt(file, skiprows=1), 200, 400)

file= folder+"BP4/BP4_4_FM_spatial/trans_profile/spatial_310/BP4_4_fm_spatial_310.txt"
plotter("BP4_4", np.loadtxt(file, skiprows=1), 200, 400)

file= folder+"BP4/BP4_4_FM_spatial/trans_profile/spatial_350/BP4_4_fm_spatial_350.txt"
plotter("BP4_4", np.loadtxt(file, skiprows=1), 200, 500)

# NB1_1 #
file= folder+"NB1/NB1_1_FM_spatial/trans_profile/NB1_1_spatial_214/NB1_1_fm_spatial_214.txt"
plotter("NB1_1", np.loadtxt(file, skiprows=1), 180, 400)

file= folder+"NB1/NB1_1_FM_spatial/trans_profile/NB1_1_spatial_254/NB1_1_fm_spatial_254.txt"
plotter("NB1_1", np.loadtxt(file, skiprows=1), 180, 400)

# BB2_3 #
file= folder+"BB2/BB2_3_FM_spatial_OOB/trans_profile/spatial_255/BB2_3_fm_spatial_255.txt"
plotter("BB2_3", np.loadtxt(file, skiprows=1), 200, 400)
file= folder+"BB2/BB2_3_FM_spatial_OOB/trans_profile/spatial_290/BB2_3_fm_spatial_290.txt"
plotter("BB2_3", np.loadtxt(file, skiprows=1), 276, 400)
'''