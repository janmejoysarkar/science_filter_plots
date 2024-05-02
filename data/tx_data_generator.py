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
    mean=0
    file= open(lis[0], 'r')
    lines= file.readlines()[:35]
    for line in lines:
        if line.startswith('Exposure Time'):
            exptime=float(line.split(':')[1])
    wl= np.loadtxt(lis[0], skiprows=35, usecols=0)
    for file in lis:
        y= np.loadtxt(file, skiprows=35, usecols=1)
        mean= mean+y
    return(wl, mean/exptime)

def tx_percent(flt, dark, src, dark_src):
    return((flt-dark)*100/(src-dark_src))
    
def wl_calib(x):
    a= -8.21e-7 
    b = 9.96e-5
    c = 1.51e-1
    return((a*x**2)+(b*x)+c)

def plot(x,y_ls):
    plt.figure()
    for y in y_ls:
        plt.plot(x,y)

if __name__=='__main__':
    fld= 'BP2_8_262-282'
    typ= 'spatial'
    
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
        wl=src[0]
        
        #plot(wl_calib(wl), [tx_c, tx_l, tx_r, tx_t, tx_b])
        plt.plot(wl, tx_c)
        plt.plot(wl-wl_calib(wl),tx_c)
        
        
    elif typ=='oob':
        dark_oob= avg_normalize(glob.glob(os.path.join(filter_path,'dark_oob*.asc')))
        dark_src= avg_normalize(glob.glob(os.path.join(filter_path,'dark_src*.asc')))
        oob= avg_normalize(glob.glob(os.path.join(filter_path,'oob*.asc')))
        src= avg_normalize(glob.glob(os.path.join(filter_path,'src*.asc')))
        #Tx percentages
        tx_oob= tx_percent(oob[1], dark_oob[1], src[1], dark_src[1])
        wl= src[0]
        plot(wl[:-5], [tx_oob[:-5]])
