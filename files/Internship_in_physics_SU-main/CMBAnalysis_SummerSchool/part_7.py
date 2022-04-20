import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import astropy.io.fits as fits

#%cd /Users/Your/place/for/code
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
atmospheric_noise_level = 0 #cs.atmospheric_noise_level
one_over_f_noise_level = 0 #cs.one_over_f_noise_level

## we will need a window function below, so we create it here
window = (cosine_window(N))

nbig = 10000
# read in the input CMB spectra
ell, DlTT,DlEE,DlBB, DlTE= np.loadtxt("CMB_fiducial_totalCls.dat", usecols=(0, 1,2,3,4), unpack=True) 

##
ell_big = np.arange(nbig)
DlTT_big = np.zeros(nbig)
DlTT_big[ell.astype(int)] = DlTT
DlEE_big = np.zeros(nbig)
DlEE_big[ell.astype(int)] = DlEE
DlBB_big = np.zeros(nbig)
DlBB_big[ell.astype(int)] = DlBB
DlTE_big = np.zeros(nbig)
DlTE_big[ell.astype(int)] = DlTE

ell = ell_big
DlTT = DlTT_big + 1e-3   ### the 1e-3 factor maps plotting easy
DlEE = DlEE_big + 1e-3
DlBB = DlBB_big + 1e-3
DlTE = DlTE_big

Temp_point_source_spectrum = DlTT[3000]*(ell/3000.)**2.
Pol_point_source_spectrum = DlEE[4500]*(ell/4500.)**2.

DlTT_PS = DlTT + Temp_point_source_spectrum   ### these are used for computing the transer functions
DlEE_PS = DlEE + Pol_point_source_spectrum
DlBB_PS = DlBB + Pol_point_source_spectrum


plt.semilogy(ell,DlTT,'r')
plt.semilogy(ell,DlEE,'g')
plt.semilogy(ell,DlBB,'b')
plt.title('TT (red), EE (green), BB (blue) spectra')
plt.ylabel('$D^{XX}_{\ell}$ [$\mu$K$^2$]')
plt.xlabel('$\ell$')
plt.show()

plt.plot(ell,DlTE,'y')
plt.ylabel('$D^{TE}_{\ell}$ [$\mu$K$^2$]')
plt.xlabel('$\ell$')
plt.title('TE spectrum')
plt.show()

def make_CMB_maps(N,pix_size,ell,DlTT,DlEE,DlTE,DlBB):
    "makes a realization of a simulated CMB sky map"

    # convert Dl to Cl, we use np.divide to avoid dividing by zero.
    dell = ell * (ell + 1) / 2 / np.pi
    ClTT = np.divide(DlTT, dell, where=ell>1)
    ClEE = np.divide(DlEE, dell, where=ell>1)
    ClTE = np.divide(DlTE, dell, where=ell>1)
    ClBB = np.divide(DlBB, dell, where=ell>1)
    
    # set the \ell = 0 and \ell =1 modes to zero as these are unmeasurmable and blow up with the above transform
    ClTT[0:2] = 0.
    ClEE[0:2] = 0.
    ClTE[0:2] = 0.
    ClBB[0:2] = 0.

    # separate the correlated and uncorrelated part of the EE spectrum
    correlated_part_of_E = np.divide(ClTE, np.sqrt(ClTT), where=ell>1)
    uncorrelated_part_of_EE = ClEE - np.divide(ClTE**2., ClTT, where=ell>1)
    
    correlated_part_of_E[0:2] = 0.
    uncorrelated_part_of_EE[0:2] = 0.
    
    # make a 2d coordinate system
    ones = np.ones(N)
    inds  = (np.arange(N) - N/2.) /(N-1.)
    X = np.outer(ones,inds)
    Y = np.transpose(X)
    R = np.sqrt(X**2. + Y**2.)
    ang = np.arctan2(Y,X)   ## we now need this angle to handle the EB <--> QU rotation
    
    # now make a set of 2d CMB masks for the T, E, and B maps
    ell_scale_factor = 2. * np.pi / (pix_size/60. * np.pi/180.)
    ell2d = R * ell_scale_factor
    ClTT_expanded = np.zeros(int(ell2d.max())+1)
    ClTT_expanded[0:(ClTT.size)] = ClTT
    ClEE_uncor_expanded = np.zeros(int(ell2d.max())+1)
    ClEE_uncor_expanded[0:(uncorrelated_part_of_EE.size)] = uncorrelated_part_of_EE
    ClE_corr_expanded = np.zeros(int(ell2d.max())+1)
    ClE_corr_expanded[0:(correlated_part_of_E.size)] = correlated_part_of_E
    ClBB_expanded = np.zeros(int(ell2d.max())+1)
    ClBB_expanded[0:(ClBB.size)] = ClBB
    CLTT2d = ClTT_expanded[ell2d.astype(int)]
    ClEE_uncor_2d = ClEE_uncor_expanded[ell2d.astype(int)]
    ClE_corr2d = ClE_corr_expanded[ell2d.astype(int)]
    CLBB2d = ClBB_expanded[ell2d.astype(int)]
    
    # now make a set of gaussian random fields that will be turned into the CMB maps
    randomn_array_for_T = np.fft.fft2(np.random.normal(0,1,(N,N)))
    randomn_array_for_E = np.fft.fft2(np.random.normal(0,1,(N,N))) 
    randomn_array_for_B = np.fft.fft2(np.random.normal(0,1,(N,N))) 
    
    ## make the T, E, and B maps by multiplying the masks against the random fields
    FT_2d = np.sqrt(CLTT2d) * randomn_array_for_T
    FE_2d = np.sqrt(ClEE_uncor_2d) * randomn_array_for_E + ClE_corr2d* randomn_array_for_T
    FB_2d = np.sqrt(CLBB2d) * randomn_array_for_B
    
    ## now conver E abd B to Q and U
    FQ_2d = FE_2d* np.cos(2.*ang) - FB_2d * np.sin(2. *ang)
    FU_2d = FE_2d* np.sin(2.*ang) + FB_2d * np.cos(2. *ang)
    
    ## convert from fourier space to real space
    CMB_T = np.fft.ifft2(np.fft.fftshift(FT_2d)) /(pix_size /60.* np.pi/180.)
    CMB_T = np.real(CMB_T)
    CMB_Q = np.fft.ifft2(np.fft.fftshift(FQ_2d)) /(pix_size /60.* np.pi/180.)
    CMB_Q = np.real(CMB_Q)
    CMB_U = np.fft.ifft2(np.fft.fftshift(FU_2d)) /(pix_size /60.* np.pi/180.)
    CMB_U = np.real(CMB_U)

    ## optional code for spitting out E and B maps 
    CMB_E = np.fft.ifft2(np.fft.fftshift(FE_2d)) /(pix_size /60.* np.pi/180.)
    CMB_E = np.real(CMB_E)
    CMB_B = np.fft.ifft2(np.fft.fftshift(FB_2d)) /(pix_size /60.* np.pi/180.)
    CMB_B = np.real(CMB_B)
    
    ## return the maps
    return(CMB_T,CMB_Q,CMB_U,CMB_E,CMB_B)
  ###############################


    
## make a CMB T map
CMB_T,CMB_Q,CMB_U,CMB_E,CMB_B = make_CMB_maps(N,pix_size,ell,DlTT,DlEE,DlTE,DlBB)


p = Plot_CMB_Map(CMB_T,c_min,c_max,X_width,Y_width)
p = Plot_CMB_Map(CMB_Q,c_min/20.,c_max/20.,X_width,Y_width)
p = Plot_CMB_Map(CMB_U,c_min/20.,c_max/20.,X_width,Y_width)
p = Plot_CMB_Map(CMB_E,c_min/20.,c_max/20.,X_width,Y_width)
p = Plot_CMB_Map(CMB_B,c_min/200.,c_max/200.,X_width,Y_width)

def plot_quiver(Q, U, X_width, Y_width, background=None):
    '''Visualize Stokes Q, U as headless vectors'''
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    
    # Smooth maps for nicer images
    fwhm_pix = 30
    Q = convolve_map_with_gaussian_beam(N,pix_size,fwhm_pix,Q)
    U = convolve_map_with_gaussian_beam(N,pix_size,fwhm_pix,U)
    if background is not None:
        # If provided, we overplot the vectors on top of the smoothed background.
        background = convolve_map_with_gaussian_beam(N,pix_size,fwhm_pix,background)
    
    Q = Q[::int(fwhm_pix),::int(fwhm_pix)]
    U = U[::int(fwhm_pix),::int(fwhm_pix)]
    
    p_amp = np.sqrt(Q**2 + U**2)
    ang = np.arctan2(U, Q) / 2.
    
    u = p_amp * np.cos(ang)
    v = p_amp * np.sin(ang)

    x = np.linspace(0,X_width,u.shape[1])
    y = np.linspace(0,X_width,u.shape[0])    
        
    fig, ax = plt.subplots(figsize=(10,10))
    if background is not None:
        im = ax.imshow(background, interpolation='bilinear', origin='lower',cmap=cm.RdBu_r,
                       extent=([0,X_width,0,Y_width]))
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = plt.colorbar(im, cax=cax)
        cbar.set_label('temperature [uK]', rotation=270)
        
    ax.quiver(x, y, u, v, headwidth=1, headlength=0, pivot='mid', units='xy',
              scale_units='xy', scale=2 * p_amp.max(), linewidth=1)
        
    ax.set_ylabel('angle $[^\circ]$')
    ax.set_xlabel('angle $[^\circ]$')
    
    plt.show(fig)

plot_quiver(CMB_Q,CMB_U,X_width,Y_width,background=CMB_E)

def QU2EB(N,pix_size,Qmap,Umap,):
    '''Calcalute E, B maps given input Stokes Q, U maps'''
    
    # Create 2d Fourier coordinate system.
    ones = np.ones(N)
    inds  = (np.arange(N) - N/2.) /(N-1.)
    kX = np.outer(ones,inds) / (pix_size/60. * np.pi/180.)
    kY = np.transpose(kX)
    ang = np.arctan2(kY,kX)
  
    # Convert to Fourier domain.
    fQ = np.fft.fftshift(np.fft.fft2(Qmap))
    fU = np.fft.fftshift(np.fft.fft2(Umap))
    
    # Convert Q, U to E, B in Fourier domain.
    fE = fQ * np.cos(2.*ang) + fU * np.sin(2. *ang)
    fB = - fQ * np.sin(2.*ang) + fU * np.cos(2. *ang)
    
    # Convert E, B from Fourier to real space.
    Emap = np.real(np.fft.ifft2(np.fft.fftshift(fE)))
    Bmap = np.real(np.fft.ifft2(np.fft.fftshift(fB)))

    return Emap, Bmap

# Convert masked Q, U to E and B.
Emap, Bmap = QU2EB(N,pix_size,CMB_Q * window,CMB_U * window)

Plot_CMB_Map(window,0,1,X_width,Y_width)
Plot_CMB_Map(Emap,-20,20,X_width,Y_width)
Plot_CMB_Map(Bmap,-2,2,X_width,Y_width)

def kendric_method_precompute_window_derivitives(win,pix_size):
    delta = pix_size * np.pi /180. /60.
    dwin_dx =    ((-1.) * np.roll(win,-2,axis =1)      +8. * np.roll(win,-1,axis =1)     - 8. *np.roll(win,1,axis =1)      +np.roll(win,2,axis =1) ) / (12. *delta)
    dwin_dy =    ((-1.) * np.roll(win,-2,axis =0)      +8. * np.roll(win,-1,axis =0)     - 8. *np.roll(win,1,axis =0)      +np.roll(win,2,axis =0) ) / (12. *delta)
    d2win_dx2 =  ((-1.) * np.roll(dwin_dx,-2,axis =1)  +8. * np.roll(dwin_dx,-1,axis =1) - 8. *np.roll(dwin_dx,1,axis =1)  +np.roll(dwin_dx,2,axis =1) ) / (12. *delta)
    d2win_dy2 =  ((-1.) * np.roll(dwin_dy,-2,axis =0)  +8. * np.roll(dwin_dy,-1,axis =0) - 8. *np.roll(dwin_dy,1,axis =0)  +np.roll(dwin_dy,2,axis =0) ) / (12. *delta)
    d2win_dxdy = ((-1.) * np.roll(dwin_dy,-2,axis =1)  +8. * np.roll(dwin_dy,-1,axis =1) - 8. *np.roll(dwin_dy,1,axis =1)  +np.roll(dwin_dy,2,axis =1) ) / (12. *delta)
    return(dwin_dx,dwin_dy,d2win_dx2,d2win_dy2,d2win_dxdy)

def kendrick_method_TQU_to_fourier_TEB(N,pix_size,Tmap,Qmap,Umap,window,dwin_dx,dwin_dy,d2win_dx2,d2win_dy2,d2win_dxdy):
    ### the obvious FFTs
    fft_TxW = np.fft.fftshift(np.fft.fft2(Tmap * window))
    fft_QxW = np.fft.fftshift(np.fft.fft2(Qmap * window))
    fft_UxW = np.fft.fftshift(np.fft.fft2(Umap * window))

    ### the less obvious FFTs that go into the no-leak estiamte
    fft_QxdW_dx = np.fft.fftshift(np.fft.fft2(Qmap * dwin_dx))
    fft_QxdW_dy = np.fft.fftshift(np.fft.fft2(Qmap * dwin_dy))
    fft_UxdW_dx = np.fft.fftshift(np.fft.fft2(Umap * dwin_dx))
    fft_UxdW_dy = np.fft.fftshift(np.fft.fft2(Umap * dwin_dy))
    fft_QU_HOT  = np.fft.fftshift(np.fft.fft2( (2. * Qmap * d2win_dxdy) + Umap * (d2win_dy2 - d2win_dx2) ))
    
    ### generate the polar coordinates needed to cary out the EB-QU conversion
    ones = np.ones(N)
    inds  = (np.arange(N) - N/2.) /(N-1.)
    X = np.outer(ones,inds)
    Y = np.transpose(X)
    R = np.sqrt(X**2. + Y**2. + 1e-9)  ## the small offset regularizes the 1/ell factors below
    ang =  np.arctan2(Y,X)
    ell_scale_factor = 2. * np.pi / (pix_size/60. * np.pi/180.)
    ell2d = R * ell_scale_factor
        
    #p=Plot_CMB_Map(np.real( ang),-np.pi,np.pi,N,N)
    
    
    ### now compute the estimator
    fTmap = fft_TxW
    fEmap = fft_QxW * np.cos(2. * ang) + fft_UxW * np.sin(2. * ang)
    fBmap = (fft_QxW * (-1. *np.sin(2. * ang)) + fft_UxW * np.cos(2. * ang))  ## this line is the nominal B estimator
    fBmap = fBmap - complex(0,2.) / ell2d * (fft_QxdW_dx * np.sin(ang) + fft_QxdW_dy * np.cos(ang))
    fBmap = fBmap - complex(0,2.) / ell2d * (fft_UxdW_dy * np.sin(ang) - fft_UxdW_dx * np.cos(ang))
    fBmap = fBmap +  ell2d**(-2.) * fft_QU_HOT

    ### return the complex fourier maps in 2d
    return(fTmap,fEmap,fBmap)

    
    
dwin_dx,dwin_dy,d2win_dx2,d2win_dy2,d2win_dxdy = kendric_method_precompute_window_derivitives(window,pix_size)

### plots of the window function derivatives
#p=Plot_CMB_Map(dwin_dx,-10,10,X_width,Y_width)
#p=Plot_CMB_Map(dwin_dy,-10,10,X_width,Y_width)
#p=Plot_CMB_Map(d2win_dx2,-10,10,X_width,Y_width)
#p=Plot_CMB_Map(d2win_dy2,-10,10,X_width,Y_width)
#p=Plot_CMB_Map(d2win_dxdy,-10,10,X_width,Y_width)

fTmap,fEmap,fBmap = kendrick_method_TQU_to_fourier_TEB(N,pix_size,CMB_T,CMB_Q,CMB_U,window,dwin_dx,dwin_dy,d2win_dx2,d2win_dy2,d2win_dxdy)

p=Plot_CMB_Map(np.real( (np.fft.ifft2(np.fft.fftshift(fTmap)))),c_min,c_max,X_width,Y_width)
p=Plot_CMB_Map(np.real( (np.fft.ifft2(np.fft.fftshift(fEmap)))),c_min/20.,c_max/20.,X_width,Y_width)
p=Plot_CMB_Map(np.real( (np.fft.ifft2(np.fft.fftshift(fBmap))-np.mean(np.fft.ifft2(np.fft.fftshift(fBmap))))),c_min/400.,c_max/400.,X_width,Y_width)