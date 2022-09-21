import matplotlib
from matplotlib.colors import ListedColormap, LogNorm
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage, misc

from dicalum.coeffs import *
__all__ = ['DclPlot','DclHist']
def DclPlot(klog,amin,amax):
    iso = float(En_iso.get())
    ape = float(En_ape.get())
    shu = float(En_shu.get())
    epo = 6400*ape*ape/iso/shu
    rr=epo*dcldat.R
    gg=epo*dcldat.G
    bb=epo*dcldat.B
    s=gg.shape
    ny=np.uint16(s[0])
    nx=np.uint16(s[1])
    yy=(np.linspace(1,ny,ny)-ny/2.)/ny
    xx=(np.linspace(1,nx,nx)-nx/2.)/ny
    [xxx,yyy]=np.meshgrid(xx,yy)
    rrr=np.sqrt(xxx*xxx+yyy*yyy)
    #print( rr[rrr<5./90].mean() )
    #print( gg[rrr<5./90].mean() )
    #print( bb[rrr<5./90].mean() )
    if(dcldat.dark>0):
        GG=epo*(dcldat.D - dcldat.dark/ndimage.zoom(dcldat.V,0.25))
    else:
        GG=epo*dcldat.D
    #G=10*dcldat.V
    #GG = ndimage.median_filter(G, size=5)
    GG[GG<1]=1
    plt.figure(figsize=(10,5))
    cbti = [3,5,10,20]
    if(amax>420):
        aj=10**np.floor(np.log10(amax/42.0))
        cbti=[aj*3,aj*5,aj*10,aj*20,aj*40]
    locmap=dclcmap
    if (klog==2):
        cmvv = 1.4696e+09
        GG = -2.5*np.log10(GG/cmvv)
        bmin = amin
        amin = -2.5*np.log10(amax/cmvv)
        amax = -2.5*np.log10(bmin/cmvv)
        cbti = [20.0,21.0,21.3,21.7]
        locmap=dclimap
    if (klog==1):
        psm = plt.imshow(GG, cmap=locmap, interpolation='none', rasterized=True, norm=LogNorm(vmin=amin, vmax=amax))
    else:
        psm = plt.imshow(GG, cmap=locmap, interpolation='none', rasterized=True, vmin=amin, vmax=amax)
    plt.axis('off')
    psm.axes.get_xaxis().set_visible(False)
    psm.axes.get_yaxis().set_visible(False)
    plt.contour(GG, cbti, colors='w', linewidths=0.5, origin='lower')
    cbar=plt.colorbar(psm)
    cbar.set_ticks(cbti)
    cbar.set_ticklabels(cbti)
    #cbar.set_label('dsu', verticalalignment='top')
    ax = cbar.ax
    ax.text(80.0,38.0,'dsu')
    plt.show()

def DclHist():
    iso = float(En_iso.get())
    ape = float(En_ape.get())
    shu = float(En_shu.get())
    epo = 6400*ape*ape/iso/shu
    #rr=epo*dcldat.R
    gg=epo*dcldat.G
    #bb=epo*dcldat.B
    mask=dcldat.M
    gmax=epo*dcldat.max
    gm=42
    gi=2.5
    if(gmax>420):
       while(gm<gmax):
          gm = 10*gm
          gi = 10*gi
    En_sat.set(str(gm))
    En_low.set(str(gi))
    plt.figure(figsize=(10,5))
    plt.hist(gg[mask].flatten(), bins=100, range=(0, gmax))
    plt.xlabel('DSU$_{\mathrm{G}}$')
    plt.ylabel('N')
    #plt.yscale('log')
    plt.show()
