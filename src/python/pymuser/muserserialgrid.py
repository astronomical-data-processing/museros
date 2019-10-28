# #!python
# #!/usr/bin/env python -tt
# # encoding: utf-8
# #
# # Created by Holger Rapp on 2009-03-11.
# # HolgerRapp@gmx.net
# #
# error
# sub_cuda_cyclic_shift_kernel
# sub_dot_mul_kernel



import numpy as np
from math import pi,cos,sin
import matplotlib.pylab as plt

WIDTH = 6
NCGF = 12
HWIDTH = 3
STEP = 4
#*********************
#    MAP KERNELS
#*********************

def gridVis_wBM_kernel(Grd, bm,sf, cnt, d_u, d_v, d_re,d_im, nu, du, gcount, umax, vmax,cgf):
    u0 = np.int(0.5*nu)
    for iu in range(u0,u0+umax):
        for iv in range(u0+vmax):
           for ivis in range(gcount):
                mu = d_u[ivis]
                mv = d_v[ivis]
                hflag = 1
                if (mu < 0):
                    hflag = -1
                    mu = -1*mu
                    mv = -1*mv
                uu = mu/du + u0
                vv = mv/du + u0
                cnu=np.abs(iu-uu)
                cnv=np.abs(iv-vv)
                if (cnu < HWIDTH and cnv < HWIDTH):
                    round1 = np.int(np.round(4.6*cnu+NCGF-0.5))
                    round2 = np.int(np.round(4.6*cnv+NCGF-0.5))
                    wgt =  cgf[round1]*cgf[round2];
                    Grd[iv][iu] += wgt*d_re[ivis]+hflag*wgt*d_im[ivis]*1j
                    cnt[iv][iu] += 1
                    bm[iv][iu] += wgt
                    sf[iv][iu] = 1+1j
                if (iu-u0 < HWIDTH and mu/du < HWIDTH):
                    mu = -1*mu
                    mv = -1*mv
                    uu = mu/du+u0
                    vv = mv/du+u0
                    cnu=np.abs(iu-uu)
                    cnv=np.abs(iv-vv)
                    if (cnu < HWIDTH and cnv < HWIDTH):
                        wgt = cgf[np.int(np.round(4.6*cnu+NCGF-0.5))]*cgf[np.int(np.round(4.6*cnv+NCGF-0.5))]
                        Grd[iv][iu] += wgt*d_re[ivis]-1*hflag*wgt*d_im[ivis]*1j
                        cnt[iv][iu] += 1
                        bm[iv][iu] += wgt
                        sf[iv][iu] = 1+1j
# '''
def dblGrid_kernel(Grd, nu,hfac):
    u0 = np.int(0.5*nu)
    for iu in range(1,u0):
        for iv in range(1,nu):
            niu = nu - iu
            niv = nu - iv
            Grd[iv][iu] = Grd[niv][niu].real + hfac*Grd[niv][niu].imag*1j

def wgtGrid_kernel(Grd,cnt, briggs,nu):
    u0 = np.int(0.5*nu)
    for iu in range(u0,nu):
        for iv in range(nu):
            if cnt[iv][iu] != 0:
                foo = cnt[iv][iu]
                wgt = 1./np.sqrt(1 + foo*foo/(briggs*briggs))
                Grd[iv][iu] = Grd[iv][iu]*wgt

def nrmGrid_kernel(Grd,nrm,nu):
    for iu in range(nu):
        for iv in range(nu):
            Grd[iv][iu] = Grd[iv][iu]*nrm

def corrGrid_kernel(Grd, corr,nu):
    for iu in range(nu):
        for iv in range(nu):
            Grd[iv][iu] = Grd[iv][iu]*corr[nu/2]*corr[nu/2]/(corr[iu]*corr[iv])

#
#     // *********************
#     // BEAM KERNELS
#     // *********************
def nrmBeam_kernel(bmR,nrm,nu):
    for iu in range(nu):
        for iv in range(nu):
            bmR[iv][iu] = nrm*bmR[iv][iu]
#     // *********************
#     // MORE semi-USEFUL KERNELS
#     // *********************
#
def shiftGrid_kernel(Grd, nGrd,nu):
    for iu in range(nu):
        for iv in range(nu):
            niu = 0.5*nu
            niv = 0.5*nu
            nud2 = 0.5*nu
            if iu < nud2:
                niu = nud2+iu
            else:
                niu = iu-nud2
            if iv < nud2:
                niv = nud2+iv
            else:
                niv = iv-nud2
            nGrd[niv][niu]=Grd[iv][iu]

def trimIm_kernel(im,nim,nx,nnx):
    # print nx,nnx
    for ix in range(nnx):
        for iy in range(nnx):
            nim[iy][ix] = im[(nx/2-nnx/2)+iy][(nx/2-nnx/2)+ix].real

###-------------------------------------------------------------------10.04------------------------------------##

def copyRIm_kernel(im, nim, nx):
    for ix in range(nx):
        for iy in range(nx):
            nim[iy][ix] = im[iy][ix]
            # nim[iy][ix].imag = 0

def copyIm_kernel(im,nim, nx):
      # int ix = blockDim.x*blockIdx.x + threadIdx.x;
      # int iy = blockDim.y*blockIdx.y + threadIdx.y;
      # if(iy < nx && ix < nx)
      for ix in range(nx):
          for iy in range(nx):
              nim[iy][ix] = im[iy][ix].real;

def sub_dot_mul_kernel(A, B, C, width, height):
    # Identify place on grid
    # idx = blockIdx.x * blockDim.x + threadIdx.x;
    # idy = blockIdx.y * blockDim.y + threadIdx.y;
    # id  = idy+idx*width;
    for idx in range(width):
        for idy in range(height):
            # C[idx][idy].real = A[idx][idy].real*B[idx][idy].real - A[idx][idy].imag*B[idx][idy].imag
            # C[idx][idy].imag = A[idx][idy].imag*B[idx][idy].real + A[idx][idy].real*B[idx][idy].imag
            C[idx][idy] = (A[idx][idy].real*B[idx][idy].real - A[idx][idy].imag*B[idx][idy].imag)+(A[idx][idy].imag*B[idx][idy].real + A[idx][idy].real*B[idx][idy].imag)*1j

def diskGrid_kernel(Grd, nu, radius, light):
      # int iu = blockDim.x*blockIdx.x + threadIdx.x;
      # int iv = blockDim.y*blockIdx.y + threadIdx.y;
      u0 = np.int(0.5*nu)
      for iu in range(0,u0+1):
          for iv in range(0,u0+1):
              if (np.sqrt(np.float(iu-u0)*(iu-u0)+np.float(iv-u0)*(iv-u0))<=np.float(radius)):
                  Grd[iv][iu] = light
                  # Grd[iv][iu].imag = 0
                  niu = nu- iu
                  niv = iv
                  Grd[niv][niu] = light
                  # Grd[niv][niu].imag = 0
                  niu = iu
                  niv = nu- iv
                  Grd[niv][niu] = light
                  # Grd[niv][niu].imag = 0
                  niu = nu- iu
                  niv = nu- iv
                  Grd[niv][niu] = light
                  # Grd[niv][niu].imag = 0


def sub_cuda_cyclic_shift_kernel(inarray, outarray, N, x_offset, y_offset):
    for tidx in range(N):
        for tidy in range(N):
            # index=tidx*N+tidy;
            angle=2*3.1415926535*(x_offset*(tidx-N/2)+y_offset*(tidy-N/2))/N;
            sinv = sin(angle)
            cosv = cos(angle)                                                    #sincos(angle,&sinv,&cosv);
            # outarray[tidx][tidy].real = inarray[tidx][tidy].real*cosv-inarray[tidx][tidy].imag*sinv;
            # outarray[tidx][tidy].imag = inarray[tidx][tidy].real*sinv+inarray[tidx][tidy].imag*cosv;
            outarray[tidx][tidy] = (inarray[tidx][tidy].real*cosv-inarray[tidx][tidy].imag*sinv)+(inarray[tidx][tidy].real*sinv+inarray[tidx][tidy].imag*cosv)*1j

###--------------------------------------------10.07------------------------------------------------------------##
def sub_histogram_kernel(dimg, W,  H, histo, max, min,binsize):
    #Identify place on grid
    #atomicAdd exp: for (i=0;i<N;i+=M) transformed in for (i=0;i<N;atomicAdd(&i,M))
    for idx in range(H):
        for idy in range(W):
            offset = int((dimg[idy][idx] - min)*(binsize-1.)/(max-min))
            if (offset<binsize):
                histo[offset] += 1
                # atomicAdd (&histo[offset] , 1 )

def sub_mean_average_kernel(innum, outnum, height, width, radius):
    # // Identify place on grid
    # int idx = blockIdx.x * blockDim.x + threadIdx.x;
    # int idy = blockIdx.y * blockDim.y + threadIdx.y;
    # int id  = idy+idx*width;
    for idx in range(height):
        for idy in range(width-radius-1):
            i = 0
            ss = 0
            id = idy + idx*width
            outnum[id] = 0
            if idy<width-radius-1:
                for i in range(radius):
                    # ss += innum[idx+(i/width)][idy+(i%width)]
                    ss += innum[id+i]
                # outnum[idx][idy] = int(ss/radius)
                outnum[id] = int(ss/radius)
###-----------------------------------------------------------------------------------------------------------------##

