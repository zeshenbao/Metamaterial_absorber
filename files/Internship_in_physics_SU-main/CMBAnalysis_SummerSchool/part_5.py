import numpy as np
import matplotlib
import sys
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import astropy.io.fits as fits


#%matplotlib inline
import constants as cs # the constants module

from cmb_modules import * # the module of functions

N = cs.N
N_iterations = cs.N_iterations
c_min = cs.c_min
c_max = cs.c_max
X_width =cs.X_width
Y_width = cs.Y_width
beam_size_fwhp = cs.beam_size_fwhp

pix_size = cs.pix_size

Number_of_Sources  = cs.Number_of_Sources
Amplitude_of_Sources = cs.Amplitude_of_Sources
Number_of_Sources_EX = cs.Number_of_Sources_EX
Amplitude_of_Sources_EX = cs.Amplitude_of_Sources_EX

Number_of_SZ_Clusters  = cs.Number_of_SZ_Clusters
Mean_Amplitude_of_SZ_Clusters = cs.Mean_Amplitude_of_SZ_Clusters
SZ_beta = cs.SZ_beta
SZ_Theta_core = cs.SZ_Theta_core

white_noise_level = cs.white_noise_level
atmospheric_noise_level = 0#cs.atmospheric_noise_level
one_over_f_noise_level = 0#cs.one_over_f_noise_level

## Make a CMB map
ell, DlTT = np.loadtxt("CAMB_fiducial_cosmo_scalCls.dat", usecols=(0, 1), unpack=True) 
CMB_T = make_CMB_T_map(N,pix_size,ell,DlTT)

N=int(N)
## make a point source map
PSMap = Poisson_source_component(N,pix_size,Number_of_Sources,Amplitude_of_Sources) 
PSMap +=  Exponential_source_component(N,pix_size,Number_of_Sources_EX,Amplitude_of_Sources_EX)

## make an SZ map
SZMap,SZCat = SZ_source_component(N,pix_size,Number_of_SZ_Clusters,Mean_Amplitude_of_SZ_Clusters,SZ_beta,SZ_Theta_core,False)

## add them all together to get the sky map at a single freuqency
total_map = CMB_T + PSMap + SZMap

## incorperate the impact of the instrument
    ## beam
CMB_T_convolved =convolve_map_with_gaussian_beam(N,pix_size,beam_size_fwhp,total_map)
    ## noise
Noise = make_noise_map(N,pix_size,white_noise_level,atmospheric_noise_level,one_over_f_noise_level)

total_map_plus_noise = CMB_T_convolved + Noise

total_map_plus_noise_original = total_map_plus_noise
SZCat_original = SZCat
## plot the result
p=Plot_CMB_Map(total_map_plus_noise,c_min,c_max,X_width,Y_width)

## we will need a window funciton below, so we creat that here
window = (cosine_window(N))

def matched_filter(input_map,beam_and_filt,signal_profile,FT_noise_covar):
    ## input_map: the map we are processing
    ## beam_and_filt: the beam convolved with any map filtering, in real space
    ## signal_profile: the shape of the signal we are looking for, in real spcae
    ## FT_noise_covar: the B_N_{ap}^2 + N_{ins}^2 in fourier space
             ## calculating FT_npoise_covar is expensive so it is done externally
        
    FT_beam_and_filt = np.fft.fft2(np.fft.fftshift(beam_and_filt))  ## tranform beam_and_filt to fourier space
    FT_signal = np.fft.fft2(np.fft.fftshift(signal_profile))       ## tranform cluster_profile to fourier space
    
    psi = FT_beam_and_filt * FT_signal / FT_noise_covar             ## define the matchedfilter funciton
    
    filtered = psi * np.fft.fft2(np.fft.fftshift(input_map))        ## filter the map
    filtered = np.fft.fftshift(np.fft.ifft2(filtered))              ## center the filter
    filtered = np.real(filtered)                                    ## change the data type to real
    return(filtered)


def Plot_Matched_Filtered_Map(Map_to_Plot,X_width,Y_width):
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    print("map mean:",np.mean(Map_to_Plot),"map rms:",np.std(Map_to_Plot))
    plt.figure(figsize=[10,10])
    im = plt.imshow(Map_to_Plot, interpolation='bilinear', origin='lower',cmap=cm.RdBu_r)
    #im.set_clim(c_min,c_max)
    ax=plt.gca()
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = plt.colorbar(im, cax=cax)
    im.set_extent([0,X_width,0,Y_width])
    plt.ylabel('angle $[^\circ]$')
    plt.xlabel('angle $[^\circ]$')
    cbar.set_label('matched_filter [S/N]', rotation=270)
    plt.show()
    return(0)
  ###############################

  ## construct the 2d noise noise covariance in fourier space
FT_noise_covar = np.zeros((N,N))  ## a 2d array to hold the result
     
N_iterations = 16

## make a series of simulated maps, find the power spectrum, and average these to esitmae the noise covariance
i = 0
while (i <N_iterations):
    ## sumilate the astrophysical map
    CMB_T = make_CMB_T_map(N,pix_size,ell,DlTT)
    PSMap = Poisson_source_component(N,pix_size,Number_of_Sources,Amplitude_of_Sources) 
    PSMap +=  Exponential_source_component(N,pix_size,Number_of_Sources_EX,Amplitude_of_Sources_EX)
    SZMap,trash = SZ_source_component(N,pix_size,Number_of_SZ_Clusters,Mean_Amplitude_of_SZ_Clusters,SZ_beta,SZ_Theta_core,False)
    CMB_T  = CMB_T + PSMap + SZMap  ## the astrophysical map
    
    ## fold in the instrument response
    CMB_T_convolved = convolve_map_with_gaussian_beam(N,pix_size,beam_size_fwhp,CMB_T)
    Noise = make_noise_map(N,pix_size,white_noise_level,atmospheric_noise_level,one_over_f_noise_level)
    
    ## fourier trasfomr the map
    temp =  np.fft.fft2(np.fft.fftshift(window* (CMB_T_convolved + Noise)))  ## these are the two terms in the denominator

    ## now average
    FT_noise_covar += np.real(np.conj(temp)*temp/(N_iterations*1.0))
    ## note the progress
    sys.stdout.write("\r matched filter noise realization, iterations complete: %d of %d" % ((i+1),N_iterations) )
    sys.stdout.flush()
    ## iterate
    i = i + 1



## construct the beam and cluster profile for the numerator of the matched filter
beam_and_filt = make_2d_gaussian_beam(N,pix_size,beam_size_fwhp)  ## this is the filtering we did on the map
cluster_profile = beta_function(N,pix_size,SZ_beta,SZ_Theta_core) ## this is the singnal we are looking for

## Apply the matched filter to our map
filtered_map = matched_filter(total_map_plus_noise_original,beam_and_filt,cluster_profile,FT_noise_covar)

## make a S/N map
SN_map = filtered_map / np.std(filtered_map)

## make a few plots
p = Plot_CMB_Map(total_map_plus_noise,c_min,c_max,X_width,Y_width)
p = Plot_Matched_Filtered_Map(SN_map,X_width,Y_width)

hist,bin_edges = np.histogram(SN_map,bins = 100,range=[SN_map.min(),SN_map.max()])
plt.semilogy(bin_edges[0:-1],hist)
plt.ylabel('number of pixels')
plt.xlabel('matched filter signal to noise')
plt.show()

## take SZCat and stack total_map_plus_noise on the SZ positions, do this in a mass bin

def Stack_on_Positions(map,N,cat,N_objects,bin_min,bin_max,Radius):
    Radius = np.int(Radius)
    stack = np.zeros([Radius*2,Radius*2])
    counter = 0
    i = 0
    while (i < N_objects):
        ampl = cat[2,i]
        if ((ampl > bin_min) and (ampl <= bin_max)):
            xc = cat[0,i]
            yc = cat[1,i]
            if ((xc > Radius) and (xc < N-Radius)):
                if ((yc > Radius) and (yc < N-Radius)):
                    
                    stack += map[int(xc-Radius):int(xc+Radius),int(yc-Radius):int(yc+Radius)]
                    counter +=1
        i = i + 1
    return(stack/counter)



stack = Stack_on_Positions(total_map_plus_noise,N,SZCat,Number_of_SZ_Clusters,-100000,100000,50)
stack_SN = Stack_on_Positions(SN_map,N,SZCat,Number_of_SZ_Clusters,-100000,100000,50)

p = Plot_CMB_Map(stack,c_min/4.,c_max/4.,X_width*50*2/N,Y_width*50*2/N)
p2 = Plot_Matched_Filtered_Map(stack_SN,X_width*50*2/N,Y_width*50*2/N)


centering_errors_x = np.random.normal(0,2,Number_of_SZ_Clusters)
centering_errors_y = np.random.normal(0,2,Number_of_SZ_Clusters)
SZCat_centering_errs = SZCat
SZCat_centering_errs[0,:]  += centering_errors_x
SZCat_centering_errs[1,:]  += centering_errors_y

stack = Stack_on_Positions(total_map_plus_noise,N,SZCat_centering_errs,Number_of_SZ_Clusters,-100000,100000,50)
p = Plot_CMB_Map(stack,c_min/4.,c_max/4.,X_width*50*2/N,Y_width*50*2/N)
