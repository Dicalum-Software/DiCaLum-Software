import numpy as np
from dicalum.coeffs import *
from dicalum.DclExif import *

__all__ = ['setvig']
def setvig():
    kame=dclinst.camera
    lens=dclinst.lens
    nx=CamList[kame].nx
    ny=CamList[kame].ny
    dx=CamList[kame].dx
    dy=CamList[kame].dy
    vv=LensList[lens].vign
    rm=LensList[lens].radi
    yy=(np.linspace(1,ny,ny)-ny/2.-dy)/ny
    xx=(np.linspace(1,nx,nx)-nx/2.-dx)/ny
    [xxx,yyy]=np.meshgrid(xx,yy)
    rrr=np.sqrt(xxx*xxx+yyy*yyy)/rm
    dcldat.M=rrr<1.0
    rrr[rrr>1.0]=0.0
    r=np.linspace(0,1,vv.size)
    dcldat.V=np.interp(rrr,r,vv)
    return vv.size
