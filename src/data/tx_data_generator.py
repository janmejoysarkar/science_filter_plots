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

2024-06-26: Updated in band fill intervals.
#Bash for generating folder list
#for fld in */tilt/* ; do echo \"$(echo $fld | cut -d "/" -f3)\",; done

2024-06-27: Wl shift due to temperature has been commented out because the lab
measurements were done at the same temperature at which SUIT FW Mount is
functioning- 21 deg C.

2024-09-26: Modified to output relative transmission instead of %tx.
            Changed file reading pattern.
            All processed files replaced with relative tx data.

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
        if line.startswith('Grating Groove Density (l/mm)'):
            grating=float(line.split(':')[1])
    data.close()
    wavelength= np.loadtxt(lis[0], skiprows=35, usecols=0)
    for file in lis:
        y= np.loadtxt(file, skiprows=35, usecols=1)
        summ= summ+y
    mean= summ/len(lis)
    return(wavelength, mean/exptime, grating)

def tx_percent(flt, dark, source, dark_source):
    '''
    Returns relative transmission
    '''
    return (flt-dark)/(source-dark_source)
    
def wl_calib(wvlen, filt, grating):
    '''
    Calibrates wavelength axis of the data. Applies spectroscope wl calibration,
    air to vacuum correction.
    Wl shift due to temperature has been commented out because the lab
    measurements were done at the same temperature at which SUIT FW Mount is
    functioning- 21 deg C.
    '''
    filt_list=['BB01', 'BB02', 'BB03', 'BP02', 'BP03', 'BP04', 'NB01', 
               'NB02', 'NB03', 'NB04', 'NB05', 'NB06', 'NB07', 'NB08']
    air_to_vac_list= [0.069, 0.082, 0.092, 0.082, 0.100, 0.090, 0.068, 
                 0.082, 0.083, 0.083, 0.083, 0.087, 0.110, 0.112]
    #temp shift should be applied if operating temp and measurement temperatures
    #of filter spectrum are different. The amount of shift is coeff*delta T (degC)
    #For our case, measurement temp and operating temp are both 21 deg. delta T =0
    #temp_pm=np.array([0.88*25, 1.95*25, 2.2*24, 1.95*25, 2.45*25, 2.17*25, 3*25, 
             #1.9*24, 2.0*25, 2.0*25, 2.0*25, 2.1*24, 2.7*24, 2.8*25])*10**-3
    if grating < 1201:
        a, b, c= -6.48e-7, 1.08e-3, -3.10e-1 #for 1200 lpmm
    elif grating > 2399:
        a, b, c= -8.21e-7, 9.96e-5, 1.51e-1 #for 2400 lpmm
    hrs_calib_dev= (a*wvlen**2)+(b*wvlen)+c 
    a2v_shift= air_to_vac_list[filt_list.index(filt)]
    #temp_shift= temp_pm[filt_list.index(filt)]
    wl_corrected= (wvlen-hrs_calib_dev)+a2v_shift #+temp_shift
    return wl_corrected

def plot(x,y_ls, lo=None, hi=None):
    '''
    Generates plots if needed.
    '''
    plt.figure()
    for y in y_ls:
        plt.plot(x[lo:hi],y[lo:hi]) if lo is not None else plt.plot(x,y)
    plt.grid()
    plt.show()

     
if __name__=='__main__':
    #Bash for generating folder list
    #for fld in */tilt/* ; do echo \"$(echo $fld | cut -d "/" -f3)\",; done
    #for FLD in ["NB1_2",
    #            "NB2A_7",
    #            "NB3_2",
    #            "NB4_2",
    #            "NB5_3",
    #            "NB6_1",
    #            "NB7_2"]:
        
    #####USER-DEFINED###
    TYP= 'tilt' #type of data {'spatial', 'oob', 'tilt'}
    SAVE= True
    PLOT= False
    project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/science_filter_characterization/science_filter_charactrerization_scripts/science_filter_plots_project/')
    ####################
   
    #    FLD= os.path.basename(path)
    #    path_list= sorted(glob.glob(os.path.join(project_path+f'data/raw/*/{TYP}/*')))
    #    filter_path= [path for path in path_list if path.endswith(FLD)][0]
        

    for filter_path in sorted(glob.glob(f'{project_path}/data/raw/*/{TYP}/*')):
        filt_name= filter_path.split('raw/')[1][:4]
        sav_path= os.path.join(project_path, 'data/processed/', filt_name, TYP)
        FLD= os.path.basename(filter_path)
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
            wl=wl_calib(src[0], filt_name, src[2])
            stack= np.array([wl, tx_c, tx_l, tx_r, tx_t, tx_b]).T
            if PLOT: plot(stack[:,0], [tx_c, tx_l, tx_r, tx_t, tx_b], lo=900, hi=1300)
            if SAVE: 
                np.savetxt(os.path.join(sav_path, f'{FLD}_spatial.txt'), stack, header='wl center_tx left_tx right_tx top_tx bottom_tx', fmt='%.7f')
                print('Spatial tx files generated for ', FLD)
            
        elif TYP=='oob':
            src= avg_normalize(glob.glob(os.path.join(filter_path,'src*.asc')))
            dark_src= avg_normalize(glob.glob(os.path.join(filter_path,'dark_src*.asc')))
            wl=wl_calib(src[0], filt_name, src[2])
    
            oob_files= glob.glob(os.path.join(filter_path,'oob*.asc'))
            if (len(oob_files) != 0):
                oob= avg_normalize(oob_files)
                dark_oob= avg_normalize(glob.glob(os.path.join(filter_path,'dark_oob*.asc')))
                #Tx percentages
                tx_oob= tx_percent(oob[1], dark_oob[1], src[1], dark_src[1])
                if PLOT: plot(wl, [tx_oob])
                stack=np.array([wl, tx_oob]).T
                if SAVE: 
                    np.savetxt(os.path.join(sav_path, f'{FLD}_oob.txt'), stack, header='wl \t tx', fmt='%.7f')
                
            flt_c_files= glob.glob(os.path.join(filter_path,'flt_c*.asc'))
            if (len(flt_c_files) != 0):
                flt_c= avg_normalize(flt_c_files)
                dark_flt=avg_normalize(glob.glob(os.path.join(filter_path,'dark_flt*.asc')))
                tx_c= tx_percent(flt_c[1], dark_flt[1], src[1], dark_src[1])
                if PLOT: plot(wl, [tx_c])
                stack= np.array([wl, tx_c]).T    
                if SAVE:
                    np.savetxt(os.path.join(sav_path, f'{FLD}_inband.txt'), stack, header='wl \t tx', fmt='%.7f')
                    print('OOB tx files generated for ', FLD)
    
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
            wl= wl_calib(src[0], filt_name, src[2])
            tilt_tx_ls.insert(0, wl)
            stack= np.array(tilt_tx_ls).T #.T makes transpose. To make the data in columns.
            if PLOT: plot(stack[:,0], [stack[:,i] for i in range (7,14)], lo=970, hi=1100)
    
            if SAVE:
                header='wl -6deg_tx -5deg_tx -4deg_tx -3deg_tx -2deg_tx -1deg_tx 0deg_tx 1deg_tx 2deg_tx 3deg_tx 4deg_tx 5deg tx 6deg_tx'
                np.savetxt(os.path.join(sav_path, f'{FLD}_tilt.txt'), stack, header=header, fmt='%.7f')
                print('Tilt tx files generated for ', FLD)
