#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:34:56 2024
-Created to generate data files for SUIT image analysis.
-Spatial, OOB and tilt data is processed and %tx is derived.
-Output is saved as text files.
-User has to maintain project folder structure.
-Raw data has to be stored at {PROJECT}/data/raw.
-User has to enter the folder name containing the ascii files of the raw data.
-User has to define what data is to be prepped (spatial, tilt, oob).
-Output will be saved at {PROJECT}/data/processed.
-Output folder should have {PROJECT}/data/processed/{filter_name}/{spatial,oob,tilt} structure.
@author: janmejoyarch
"""
import glob, os
import numpy as np
import matplotlib.pyplot as plt

def avg_normalize(lis): 
    '''
    returns averaged exp time normalized counts
    '''
    summ=0
    data= open(lis[0], 'r')
    lines= data.readlines()[:35]
    for line in lines:
        if line.startswith('Exposure Time'):
            exptime=float(line.split(':')[1])
    data.close()
    wavelength= np.loadtxt(lis[0], skiprows=35, usecols=0)
    for file in lis:
        y= np.loadtxt(file, skiprows=35, usecols=1)
        summ= summ+y
    mean= summ/len(lis)
    return(wavelength, mean/exptime)

def tx_percent(flt, dark, source, dark_source):
    '''
    Returns transmission %
    '''
    return (flt-dark)*100/(source-dark_source)
    
def wl_calib(wvlen, filt):
    '''
    Calibrates wavelength axis of the data. Applies spectroscope wl calibration,
    air to vacuum correction and wl shift due to temp.
    '''
    filt_list=['BB01', 'BB02', 'BB03', 'BP02', 'BP03', 'BP04', 'NB01', 
               'NB02', 'NB03', 'NB04', 'NB05', 'NB06', 'NB07', 'NB08']
    air_to_vac_list= [0.069, 0.082, 0.092, 0.082, 0.100, 0.090, 0.068, 
                 0.082, 0.083, 0.083, 0.083, 0.087, 0.110, 0.112]
    temp_pm=np.array([0.88*25, 1.95*25, 2.2*24, 1.95*25, 2.45*25, 2.17*25, 3*25, 
             1.9*24, 2.0*25, 2.0*25, 2.0*25, 2.1*24, 2.7*24, 2.8*25])*10**-3
    a, b, c= -8.21e-7, 9.96e-5, 1.51e-1
    hrs_calib_dev= (a*wvlen**2)+(b*wvlen)+c
    a2v_shift= air_to_vac_list[filt_list.index(filt)]
    temp_shift= temp_pm[filt_list.index(filt)]
    wl_corrected= (wvlen-hrs_calib_dev)+a2v_shift+temp_shift
    return wl_corrected
def plot(x,y_ls, lo=None, hi=None):
    '''
    Generates plots if needed.
    '''
    plt.figure()
    for y in y_ls:
        plt.plot(x[lo:hi],y[lo:hi]) if lo is not None else plt.plot(x,y)
     
if __name__=='__main__':
    #####USER-DEFINED###
    FLD= 'BP4_2_390_OOB' #folder name for raw data
    TYP= 'oob' #type of data
    SAVE= True
    project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/science_filter_charactrerization_scripts/science_filter_plots_project/')
    ####################
    
    path_list= sorted(glob.glob(os.path.join(project_path+f'data/raw/*/{TYP}/*')))
    filter_path= [path for path in path_list if path.endswith(FLD)][0]
    filt_name= filter_path.split('raw/')[1][:4]
    sav_path= os.path.join(project_path, 'data/processed/', filt_name, TYP)
    
    if TYP=='spatial':
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
        wl=wl_calib(src[0], filt_name)
        stack= np.array([wl, tx_c, tx_l, tx_r, tx_t, tx_b]).T
        if SAVE: np.savetxt(os.path.join(sav_path, f'{FLD}_spatial.txt'), stack, header='wl center%tx left%tx right%tx top%tx bottom%tx', fmt= '% 1.5f')
        print('Spatial %tx files generated for ', FLD)
        
    elif TYP=='oob':
        src= avg_normalize(glob.glob(os.path.join(filter_path,'src*.asc')))
        dark_src= avg_normalize(glob.glob(os.path.join(filter_path,'dark_src*.asc')))
        wl=wl_calib(src[0], filt_name)

        oob_files= glob.glob(os.path.join(filter_path,'oob*.asc'))
        if (len(oob_files) != 0):
            oob= avg_normalize(oob_files)
            dark_oob= avg_normalize(glob.glob(os.path.join(filter_path,'dark_oob*.asc')))
            #Tx percentages
            tx_oob= tx_percent(oob[1], dark_oob[1], src[1], dark_src[1])
            plot(wl, [tx_oob])
            stack=np.array([wl, tx_oob]).T
            if SAVE: np.savetxt(os.path.join(sav_path, f'{FLD}_oob.txt'), stack, header='wl \t %tx', fmt= '% 1.5f')
            
        flt_c_files= glob.glob(os.path.join(filter_path,'flt_c*.asc'))
        if (len(flt_c_files) != 0):
            flt_c= avg_normalize(flt_c_files)
            dark_flt=avg_normalize(glob.glob(os.path.join(filter_path,'dark_flt*.asc')))
            tx_c= tx_percent(flt_c[1], dark_flt[1], src[1], dark_src[1])
            plot(wl, [tx_c])
            stack= np.array([wl, tx_c]).T    
            if SAVE: np.savetxt(os.path.join(sav_path, f'{FLD}_inband.txt'), stack, header='wl \t %tx', fmt= '% 1.5f')
        
        print('OOB %tx files generated for ', FLD)

    elif TYP=='tilt':
        dark_src= avg_normalize(glob.glob(os.path.join(filter_path,'drk_src*.asc')))
        src= avg_normalize(glob.glob(os.path.join(filter_path,'src*.asc')))
        dark_flt= avg_normalize(glob.glob(os.path.join(filter_path,'drk_f*.asc')))
        tilt_tx_ls=[]
        for tilt in np.arange(-6,7,1):
            tilt_file_list= glob.glob(os.path.join(filter_path,f'f_{tilt}*.asc'))
            data= avg_normalize(tilt_file_list)
            tx= tx_percent(data[1], dark_flt[1], src[1], dark_src[1])
            tilt_tx_ls.append(tx)
        wl= wl_calib(src[0], filt_name)
        tilt_tx_ls.insert(0, wl)
        stack= np.array(tilt_tx_ls).T #.T makes transpose. To make the data in columns.
        if SAVE: np.savetxt(os.path.join(sav_path, f'{FLD}_tilt.txt'), stack, header='wl -6deg%tx -5deg%tx -4deg%tx -3deg%tx -2deg%tx -1deg%tx 0deg%tx 1deg%tx 2deg%tx 3deg%tx 4deg%tx 5deg tx 6deg%tx', fmt= '% 1.5f')
        print('Tilt %tx files generated for ', FLD)

        
