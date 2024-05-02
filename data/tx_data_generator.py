#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:34:56 2024

@author: janmejoyarch
"""
import numpy as np
import glob
import os
import matplotlib.pyplot as plt

def avg_normalize(lis): #returns averaged exp time normalized counts
    summ=0
    file= open(lis[0], 'r')
    lines= file.readlines()[:35]
    for line in lines:
        if line.startswith('Exposure Time'):
            exptime=float(line.split(':')[1])
    wl= np.loadtxt(lis[0], skiprows=35, usecols=0)
    for file in lis:
        y= np.loadtxt(file, skiprows=35, usecols=1)
        summ= summ+y
    mean= summ/len(lis)
    return(wl, mean/exptime)

def tx_percent(flt, dark, src, dark_src):
    return((flt-dark)*100/(src-dark_src))
    
def wl_calib(wl, filt):
    filt_list=['BB01', 'BB02', 'BB03', 'BP02', 'BP03', 'BP04', 'NB01', 
               'NB02', 'NB03', 'NB04', 'NB05', 'NB06', 'NB07', 'NB08']
    air_to_vac_list= [0.069, 0.082, 0.092, 0.082, 0.100, 0.090, 0.068, 
                 0.082, 0.083, 0.083, 0.083, 0.087, 0.110, 0.112]
    temp_pm=np.array([0.88*25, 1.95*25, 2.2*24, 1.95*25, 2.45*25, 2.17*25, 3*25, 
             1.9*24, 2.0*25, 2.0*25, 2.0*25, 2.1*24, 2.7*24, 2.8*25])*10**-3
    
    a, b, c= -8.21e-7, 9.96e-5, 1.51e-1
    hrs_calib_dev= (a*wl**2)+(b*wl)+c
    
    a2v_shift= air_to_vac_list[filt_list.index(filt)]
    temp_shift= temp_pm[filt_list.index(filt)]
    
    wl_corrected= (wl-hrs_calib_dev)+a2v_shift+temp_shift
    return(wl_corrected)

def plot(x,y_ls):
    plt.figure()
    for y in y_ls:
        plt.plot(x,y)

if __name__=='__main__':
    fld= 'NB4_2'
    typ= 'tilt'
    
    project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/science_filter_charactrerization_scripts/science_filter_plots_project/')
    
    path_list= sorted(glob.glob(os.path.join(project_path+f'data/raw/*/{typ}/*')))
    filter_path= [path for path in path_list if path.endswith(fld)][0]
    
    if typ=='spatial':
        dark_flt=avg_normalize(glob.glob(os.path.join(filter_path,'dark_flt*.asc')))
        dark_src= avg_normalize(glob.glob(os.path.join(filter_path,'dark_src*.asc')))
        flt_c= avg_normalize(glob.glob(os.path.join(filter_path,'flt_c*.asc')))
        flt_l= avg_normalize(glob.glob(os.path.join(filter_path,'flt_l*.asc')))
        flt_r= avg_normalize(glob.glob(os.path.join(filter_path,'flt_r*.asc')))
        flt_t= avg_normalize(glob.glob(os.path.join(filter_path,'flt_t*.asc')))
        flt_b= avg_normalize(glob.glob(os.path.join(filter_path,'flt_b*.asc')))
        src= avg_normalize(glob.glob(os.path.join(filter_path,'src*.asc')))
        #Tx percentages
        tx_c= tx_percent(flt_c[1], dark_flt[1], src[1], dark_src[1])
        tx_l= tx_percent(flt_l[1], dark_flt[1], src[1], dark_src[1])
        tx_r= tx_percent(flt_r[1], dark_flt[1], src[1], dark_src[1])
        tx_t= tx_percent(flt_t[1], dark_flt[1], src[1], dark_src[1])
        tx_b= tx_percent(flt_b[1], dark_flt[1], src[1], dark_src[1])
        wl=wl_calib(src[0], filter_path.split('raw/')[1][:4])
        
        #plot(wl_calib(wl), [tx_c, tx_l, tx_r, tx_t, tx_b])
        plt.plot(wl, tx_c)
        
        
    elif typ=='oob':
        dark_oob= avg_normalize(glob.glob(os.path.join(filter_path,'dark_oob*.asc')))
        dark_src= avg_normalize(glob.glob(os.path.join(filter_path,'dark_src*.asc')))
        oob= avg_normalize(glob.glob(os.path.join(filter_path,'oob*.asc')))
        src= avg_normalize(glob.glob(os.path.join(filter_path,'src*.asc')))
        #Tx percentages
        tx_oob= tx_percent(oob[1], dark_oob[1], src[1], dark_src[1])
        wl=wl_calib(src[0], filter_path.split('raw/')[1][:4])
        plot(wl, [tx_oob])

    elif typ=='tilt':
        dark_src= avg_normalize(glob.glob(os.path.join(filter_path,'drk_src*.asc')))
        src= avg_normalize(glob.glob(os.path.join(filter_path,'src*.asc')))
        dark_flt= avg_normalize(glob.glob(os.path.join(filter_path,'drk_f*.asc')))
        
