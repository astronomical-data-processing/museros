import numpy as np
import time, pdb, sys, pyfits
import os
import logging
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import muserserialgrid as mk
import gaussfitter as gf
from muserGMM_kernel import*
# from sklearn.mixture import GMM

logger = logging.getLogger('muser')

class Clean:

    def spheroid(self, eta, m, alpha):
        """
        Calculates spheriodal wave functions. See Schwab 1984 for details.
        This implementation follows MIRIAD's grid.for subroutine.
        """
        # parameter alpha = 0,0.5,1,1.5,or 2   twoalp = 1,2,3,4   m = 5,6,7,8
        # m = 6 and  a = 1
        twoalp = 2 * alpha
        if np.abs(eta) > 1:
            logger.debug('bad eta value!')
        if (twoalp < 1 or twoalp > 4):
            logger.debug('bad alpha value!')
        if (m < 4 or m > 8):
            logger.debug('bad width value!')

        etalim = np.float32([1., 1., 0.75, 0.775, 0.775])
        nnum = np.int8([5, 7, 5, 5, 6])
        ndenom = np.int8([3, 2, 3, 3, 3])
        p = np.float32(
                [
                    [[5.613913E-2, -3.019847E-1, 6.256387E-1,
                      -6.324887E-1, 3.303194E-1, 0.0, 0.0],
                     [6.843713E-2, -3.342119E-1, 6.302307E-1,
                      -5.829747E-1, 2.765700E-1, 0.0, 0.0],
                     [8.203343E-2, -3.644705E-1, 6.278660E-1,
                      -5.335581E-1, 2.312756E-1, 0.0, 0.0],
                     [9.675562E-2, -3.922489E-1, 6.197133E-1,
                      -4.857470E-1, 1.934013E-1, 0.0, 0.0],
                     [1.124069E-1, -4.172349E-1, 6.069622E-1,
                      -4.405326E-1, 1.618978E-1, 0.0, 0.0]
                     ],
                    [[8.531865E-4, -1.616105E-2, 6.888533E-2,
                      -1.109391E-1, 7.747182E-2, 0.0, 0.0],
                     [2.060760E-3, -2.558954E-2, 8.595213E-2,
                      -1.170228E-1, 7.094106E-2, 0.0, 0.0],
                     [4.028559E-3, -3.697768E-2, 1.021332E-1,
                      -1.201436E-1, 6.412774E-2, 0.0, 0.0],
                     [6.887946E-3, -4.994202E-2, 1.168451E-1,
                      -1.207733E-1, 5.744210E-2, 0.0, 0.0],
                     [1.071895E-2, -6.404749E-2, 1.297386E-1,
                      -1.194208E-1, 5.112822E-2, 0.0, 0.0]
                     ]
                ])
        q = np.float32(
                [
                    [[1., 9.077644E-1, 2.535284E-1],
                     [1., 8.626056E-1, 2.291400E-1],
                     [1., 8.212018E-1, 2.078043E-1],
                     [1., 7.831755E-1, 1.890848E-1],
                     [1., 7.481828E-1, 1.726085E-1]
                     ],
                    [[1., 1.101270, 3.858544E-1],
                     [1., 1.025431, 3.337648E-1],
                     [1., 9.599102E-1, 2.918724E-1],
                     [1., 9.025276E-1, 2.575337E-1],
                     [1., 8.517470E-1, 2.289667E-1]
                     ]
                ])

        i = m - 4
        if (np.abs(eta) > etalim[i]):
            ip = 1
            x = eta * eta - 1
        else:
            ip = 0
            x = eta * eta - etalim[i] * etalim[i]
            # numerator via Horner's rule
        mnp = nnum[i] - 1
        num = p[ip, twoalp, mnp]
        for j in np.arange(mnp):
            num = num * x + p[ip, twoalp, mnp - 1 - j]
            # denominator via Horner's rule
        nq = ndenom[i] - 1
        denom = q[ip, twoalp, nq]
        for j in np.arange(nq):
            denom = denom * x + q[ip, twoalp, nq - 1 - j]

        return np.float32(num / denom)

    def gcf(self, n, width):
        """
        Create table with spheroidal gridding function, C
        This implementation follows MIRIAD's grid.for subroutine.
        """
        alpha = 1.
        j = 2 * alpha
        p = 0.5 * j
        phi = np.zeros(n, dtype=np.float32)
        for i in np.arange(n):
            x = np.float32(2 * i - (n - 1)) / (n - 1)
            phi[i] = (np.sqrt(1 - x * x) ** j) * self.spheroid(x, width, p)
        # print phi
        return phi

    def corrfun(self, n, width):
        """
        Create gridding correction function, c
        This implementation follows MIRIAD's grid.for subroutine.
        """
        alpha = 1.
        dx = 2. / n
        i0 = n / 2 + 1
        phi = np.zeros(n, dtype=np.float32)
        for i in np.arange(n):
            x = (i - i0 + 1) * dx
            phi[i] = self.spheroid(x, width, alpha)
        # print phi
        return phi

    def sub_sun_disk_offset(self, A, B):
        # import numpy
        # return np.fft.irfft2(np.fft.rfft2(A) * np.fft.rfft2(B, A.shape))


        nx = A.shape[0]
        # plan = fft.Plan((np.int(nx), np.int(nx)), np.complex64, np.complex64)

        # self.blocksize_2D = (8, 16, 1)
        # self.gridsize_2D = (
        # np.int(np.ceil(1. * nx / self.blocksize_2D[0])), np.int(np.ceil(1. * nx / self.blocksize_2D[1])))

        # d_af = gpu.to_gpu(A)
        # d_bf = gpu.to_gpu(B)
        d_af = A
        d_bf = B

        d_grd = np.zeros((np.int(nx), np.int(nx)), np.complex64)
        d_a = np.zeros_like(d_grd)
        d_b = np.zeros_like(d_grd)
        d_am = np.zeros_like(d_grd)
        d_bm = np.zeros_like(d_grd)
        d_c = np.zeros_like(d_grd)
        d_cm = np.zeros_like(d_grd)
        d_im = np.zeros((np.int(nx), np.int(nx)), np.float32)

        # xykernel.copyRIm_kernel(d_af, d_a, np.int32(nx))
        # xykernel.copyRIm_kernel(d_bf, d_b, np.int32(nx))

        # fft.fft(d_a, d_am, plan)
        d_am = np.fft.fft2(d_af)
        # fft.fft(d_b, d_bm, plan)
        d_bm = np.fft.fft2(d_bf)


        mk.sub_dot_mul_kernel(d_am, d_bm, d_cm, np.int32(nx), np.int32(nx))
        # self.shiftGrid_kernel(d_c, d_cm, np.int32(nx), block=self.blocksize_2D, grid=self.gridsize_2D)

        # fft.fft(d_cm, d_c, plan)
        d_c = np.fft.fft2(d_cm)
        mk.shiftGrid_kernel(d_c, d_cm, np.int32(nx))
        mk.copyIm_kernel(d_cm, d_im, np.int32(nx))

        return d_im

    def gridvis(self,x_offset=0,y_offset=0):
        """
        Grid the visibilities parallelized by pixel.
        References:
          - Chapter 10 in "Interferometry and Synthesis in Radio Astronomy"
              by Thompson, Moran, & Swenson
          - Daniel Brigg's PhD Thesis: http://www.aoc.nrao.edu/dissertations/dbriggs/

        If the size of the image is 1024x1024, the plan should be at least 1024*1.414 (about 25 degrees' rotation)
        And to satisfy the requirements of CLEAN, the dirty image should be 1024* 2.828
        """
        logger.debug("Gridding the visibilities")
        t_start = time.time()
        self.Flag_Ant = [8, 9,10, 11,12, 13, 19, 21,22, 23, 24, 25, 26, 28, 29, 30, 31, 34, 35, 36, 37, 38, 39]
        # f = pyfits.open(settings['vfile'])

        # unpack parameters

        nx = np.int32(2 * self.imsize)
        noff = np.int32((nx - self.imsize) / 2)

        ## constants

        arc2rad = np.float32(np.pi / 180. / 3600.)
        du = np.float32(1. / (arc2rad * self.cell)) / (self.imsize * 2.)
        logger.debug("1 Pixel DU  = %f" % du)
        ## grab data

        h_uu = np.float32(self.h_uu.ravel())
        h_vv = np.float32(self.h_vv.ravel())
        # gcount = len(gcount.ravel())
        h_rere = np.float32(self.h_rere.ravel())
        h_imim = np.float32(self.h_imim.ravel())
        gcount = np.int32(np.size(h_uu))

        blen = 0
        bl_order = np.ndarray(shape=(self.baseline_number, 2), dtype=int)
        good = []

        if self.baseline_number == 780:  # MUSER-I
            antennas = 40
        else:
            antennas = 60
        # print antennas
        for border1 in range(0, antennas - 1):
            for border2 in range(border1 + 1, antennas):
                bl_order[blen][0] = border1
                bl_order[blen][1] = border2
                blen = blen + 1

        h_u = []
        h_v = []
        h_re = []
        h_im = []
        for blen in range(0, self.baseline_number):
            if (bl_order[blen][0] not in self.Flag_Ant) and (bl_order[blen][1] not in self.Flag_Ant):
                good.append(blen)

                h_u.append(h_uu[blen])
                h_v.append(h_vv[blen])
                h_re.append(h_rere[blen])
                h_im.append(h_imim[blen])

        gcount = np.int32(np.size(h_u))

        # ------------------------
        # make gridding kernels
        # ------------------------
        ## make spheroidal convolution kernel (don't mess with these!)
        width = 6.
        ngcf = 26.
        du = np.float32(1. / (arc2rad * self.cell)) / (self.imsize * 2.)
        h_cgf = self.gcf(ngcf, width)
        h_corr = self.corrfun(nx, width)

        d_u = np.array(h_u, dtype='float32')
        d_v = np.array(h_v, dtype='float32')
        d_re = np.array(h_re, dtype='float32')
        d_im = np.array(h_im, dtype='float32')
        d_cnt = np.zeros((np.int(nx), np.int(nx)), np.int32)
        d_grd = np.zeros((np.int(nx), np.int(nx)), np.complex64)
        d_ngrd = np.zeros_like(d_grd)
        d_bm = np.zeros_like(d_grd)
        d_nbm = np.zeros_like(d_grd)
        d_cbm = np.zeros_like(d_grd)

        d_fbm = np.zeros((np.int(nx), np.int(nx)), np.float32)
        d_fim = np.zeros((np.int(self.imsize), np.int(self.imsize)), np.float32)
        d_dim = np.zeros((np.int(self.imsize), np.int(self.imsize)), np.float32)

        d_sun_disk = np.zeros_like(d_grd)
        d_fdisk = np.zeros((np.int(self.imsize), np.int(self.imsize)), np.float32)

        d_umax = np.max(np.fabs(d_u))
        d_vmax = np.max(np.fabs(d_v))
        umax = np.int32(np.ceil(d_umax/du))
        vmax = np.int32(np.ceil(d_vmax/du))
        # print umax,vmax
        # print umax,vmax,nx,gcount
        ## grid ($$)
        #  This should be improvable via:
        #    - shared memory solution? I tried...
        #    - better coalesced memory access? I tried...
        #    - reorganzing and indexing UV data beforehand?
        #       (i.e. http://www.nvidia.com/docs/IO/47905/ECE757_Project_Report_Gregerson.pdf)
        #    - storing V(u,v) in texture memory?
        mk.gridVis_wBM_kernel(d_grd,d_bm,d_cbm,d_cnt,d_u,d_v,d_re,d_im,nx,du,gcount,umax,vmax,h_cgf)
          ## apply weights
        mk.wgtGrid_kernel(d_bm,d_cnt,self.briggs,nx)
        hfac = np.int32(1)
        mk.dblGrid_kernel(d_bm,nx,hfac)
        mk.dblGrid_kernel(d_cbm, nx, hfac)                  #10.6
        mk.shiftGrid_kernel(d_bm,d_nbm,nx)
        mk.shiftGrid_kernel(d_cbm, d_bm, nx)                #10.6
          ## normalize
        mk.wgtGrid_kernel(d_grd,d_cnt,self.briggs,nx)
          ## Reflect grid about v axis
        hfac = np.int32(-1)
        mk.dblGrid_kernel(d_grd,nx,hfac)
          ## Shift both
        mk.shiftGrid_kernel(d_grd,d_ngrd,nx)

##----------------------------------------------------- disk ------------------------------------------------------------#
        # Sun Model
        # Sun disk radius = 16.1164 arcmin
        # radius = 16.1164 * 60 / self.cell
        # self.diskGrid_kernel(d_sun_disk, np.int32(self.imsize * 2), np.int32(radius), np.int32(100),
        #                      block=self.blocksize_2D,
        #                      grid=self.gridsize_2D)
        #
        # fft.fft(d_sun_disk, d_grd, plan)

        # ------------------------
        # Make the beam
        # ------------------------
        ## Transform to image plane
        # Sampling function and multiply disk
        radius = 16.1164 * 60 / self.cell
        mk.diskGrid_kernel(d_sun_disk, np.int32(self.imsize * 2), np.int32(radius), np.int32(100))
        d_grd = np.fft.fft2(d_sun_disk)
        mk.sub_dot_mul_kernel(d_grd,d_bm,d_cbm,nx,nx)
        d_sun_disk = np.fft.fft2(d_cbm)
        mk.trimIm_kernel(d_sun_disk, d_fdisk, nx, self.imsize)
        d_bmax = np.max(d_fdisk)
        bmax1 = np.float32(1. / d_bmax)
        mk.nrmBeam_kernel(d_fdisk, bmax1, self.imsize)
        # plt.imshow(d_fdisk)
        # plt.close()
        # plt.show()

##--------------------------------------------------------------------------------------------------------------------=#
        d_bm = np.fft.fft2(d_nbm)
          ## Shift
        mk.shiftGrid_kernel(d_bm,d_nbm,nx)
          ## Correct for C
        mk.corrGrid_kernel(d_nbm,h_corr,nx)
          # Trim
        mk.trimIm_kernel(d_nbm,d_fim,nx,self.imsize)
          ## Normalize
        # d_bmax = gpu.max(d_fim)
        # bmax = d_bmax.get()
        bmax = np.max(d_fim)
        bmax = np.float32(1./bmax)
        mk.nrmBeam_kernel(d_fim,bmax,self.imsize)
        ## Pull onto CPU
        # dpsf  = d_fim.get()
#--------------------------------------------------------dirty beam 1024----------------------------------#
        # bmax1 = np.max(d_fim)
        # bmax1 = np.float32(1./bmax1)
        # mk.trimIm_kernel(d_nbm,d_dim,nx,self.imsize)
        # mk.nrmBeam_kernel(d_dim,bmax1,self.imsize)
        self.dpsf = d_nbm.real
#---------------------------------------------------------------------------------------------------------#
          # ------------------------
          # Make the map
          # ------------------------
          ## Transform to image plane
        # fft.fft(d_ngrd,d_grd,plan) preence
        if (x_offset <> 0 or y_offset <> 0):
            mk.sub_cuda_cyclic_shift_kernel(d_ngrd, d_cbm, np.int32(nx), np.int32(y_offset), np.int32(x_offset))
            # self.sub_cuda_cyclic_shift_kernel(d_ngrd, d_cbm, np.int32(nx), np.int32(200), np.int32(200), block=self.blocksize_2D, grid=self.gridsize_2D)
            # fft.fft(d_cbm, d_grd, plan)
            d_grd = np.fft.fft2(d_cbm)
        else:
            d_grd = np.fft.fft2(d_ngrd)
        # d_grd = np.fft.fft2(d_ngrd)
          ## Shift
        mk.shiftGrid_kernel(d_grd,d_ngrd,nx)
          ## Correct for C
        mk.corrGrid_kernel(d_ngrd,h_corr,nx)
          ## Trim
        mk.trimIm_kernel(d_ngrd,d_fim,nx,self.imsize)
          ## Normalize (Jy/beam)
        mk.nrmGrid_kernel(d_fim,bmax,self.imsize)
        self.dirtymap = d_fim

          ## Finish timers
        t_end=time.time()
        t_full=t_end-t_start
        print "Gridding execution time %0.5f"%t_full+' s'
        # print "\t%0.5f"%(t_full/gcount)+' s per visibility'
        radius = 16.1164 * 60 / self.cell
        angles_circle = [i*np.pi/180 for i in range(0,360)]
        x = np.cos(angles_circle)
        y = np.sin(angles_circle)


        plt.figure(1)
        axes1 = plt.subplot(111)
        axes1.set_xticks([])
        axes1.set_yticks([])
        plt.imshow(self.dpsf)
        # plt.colorbar()
        plt.savefig('drity_beam.png')
        plt.close()
        # plt.show()   #drity beam

        plt.figure(2)
        axes2 = plt.subplot(111)
        axes2.set_xticks([])
        axes2.set_yticks([])
        plt.plot(radius*x+self.imsize/2, radius*y+self.imsize/2,'w')
        plt.imshow(self.dirtymap,cmap = cm.gist_heat)
        # plt.colorbar()
        plt.savefig('drity_image.png')
        plt.close()
        # plt.show()    #dirty image

        return self.dpsf,self.dirtymap,d_fdisk

    def clean_beam(self,dirtybeam,window=50):
        """
        Clean a dirty beam on the CPU
        A very simple approach - just extract the central beam #improvable#
        Another solution would be fitting a 2D Gaussian,
        e.g. http://code.google.com/p/agpy/source/browse/trunk/agpy/gaussfitter.py
        """
        # print "Cleaning the dirty beam"
        if self.imsize >= 1024:
            window = 50
        elif self.imsize >= 512:
            window = self.imsize / 24.
        elif self.imsize >= 256:
            window = self.imsize / 16.
        dpsf = dirtybeam
        h, w = np.shape(dpsf)

        cpsf = np.zeros([h, w])
        g_dpsf = np.zeros([window, window])
        g_dpsf = dpsf[w / 2 - window / 2:w / 2 + window / 2 - 1, h / 2 - window / 2:h / 2 + window / 2 - 1]
        fit = gf.fitgaussian(g_dpsf)
        fit[2] = w / 2  # fit[2] - window / 2 + w / 2
        fit[3] = h / 2  # fit[3] - window / 2 + h / 2
        cpsf = gf.twodgaussian(fit, shape=(h, w))
        cpsf = cpsf / np.max(cpsf)
        axes = plt.subplot(111)
        axes.set_xticks([])
        axes.set_yticks([])
        plt.imshow(cpsf)
        # plt.colorbar()
        plt.savefig('cpsf')
        # plt.show()
        plt.close()
        return cpsf

    def cuda_histogram(self, image, binsize, no=1):
        ## Calculate histogram

        dirty_map_max = np.max(image)
        dirty_map_min = np.min(image)

        if dirty_map_min < 0:
            dirty_map_min = -int(round(abs(dirty_map_min) + 0.5))
        else:
            dirty_map_min = int(dirty_map_min)

        if dirty_map_max < 0:
            dirty_map_max = -int(round(abs(dirty_map_max) + 0.5))
        else:
            dirty_map_max = int(round(dirty_map_max + 0.5))

        gpu_histogram = np.zeros([binsize], np.int32)

        height, width = np.shape(image)
        ## Grid parameters - #improvable#
        # tsize = 8
        # blocksize = (int(tsize), int(tsize), 1)  # The number of threads per block (x,y,z)
        # gridsize = (self.iDivUp(height, tsize), self.iDivUp(width, tsize))  # The number of thread blocks     (x,y)
        # gridsize = (int(height/tsize), int(width/ tsize))   # The number of thread blocks     (x,y)
        # self.sub_histogram_kernel(image, np.int32(self.imsize), np.int32(self.imsize), gpu_histogram,
        #                           np.int32(dirty_map_max), np.int32(dirty_map_min), np.int32(binsize), block=blocksize,
        #                           grid=gridsize)
        mk.sub_histogram_kernel(image, np.int32(self.imsize), np.int32(self.imsize), gpu_histogram,np.int32(dirty_map_max), np.int32(dirty_map_min), np.int32(binsize))
        print gpu_histogram

        gpu_smooth_histogram = np.zeros([binsize], np.int32)
        gpu_smooth_histogram2 = np.zeros([binsize], np.int32)
        # Temporary Testing
        # tsize = 16
        # blocksize = (int(tsize), int(tsize), 1)             # The number of threads per block (x,y,z)
        # gridsize = (self.iDivUp(1, tsize), self.iDivUp(binsize, tsize))   # The number of thread blocks     (x,y)
        width = binsize
        radius = 32
        height = 1
        mk.sub_mean_average_kernel(gpu_histogram, gpu_smooth_histogram, np.int32(height), np.int32(width), np.int32(radius))
        width = binsize
        radius = 32
        height = 1
        # blocksize = (int(tsize), int(tsize), 1)             # The number of threads per block (x,y,z)
        # gridsize = (self.iDivUp(1, tsize), self.iDivUp(width, tsize))   # The number of thread blocks     (x,y)
        mk.sub_mean_average_kernel(gpu_smooth_histogram, gpu_smooth_histogram2, np.int32(height), np.int32(width), np.int32(radius))

        h_histogram = gpu_smooth_histogram2
        print h_histogram
        # Histogram with NumPy
        # if (int(image.max()) - int(image.min()))>2000:
        #     bins = np.arange(int(image.min()), int(image.max()),(int(image.max())- int(image.min()))//2000 )
        # else:
        #     bins = np.arange(int(image.min()), int(image.max()))
        # item = image[:,:]
        # h_histogram,bins = np.histogram(item,bins)


        #
        # hist_smooth = gaussian_filter(h_histogram, 30)
        #
        # hist_smooth = hist_smooth[:-1]

        # Test the convolution kernel.
        # Generate or load a test image
        # You probably want to display the image using the tool of your choice here.
        # filterx = mfilter.gaussian_kernel()
        # destImage = h_histogram.copy()
        # destImage[:] = np.nan
        # destImage = mfilter.convolution_cuda(h_histogram,  filterx,  filterx)
        # destImage = destImage.reshape(2000)
        # destImage = destImage[:-1]
        bins = np.arange(0, binsize)
        data = np.vstack([bins * 1.0, h_histogram]).transpose()
        # plt.scatter(data[:,0],data[:,1])
        # plt.show()
        print data[:,0],data[:,1]
        # plt.scatter(data[:,0],data[:,1])
        if no == 1:
            gmm = GMM(dim=2, ncomps=3, data=data, method="kmeans")
        else:
            gmm = GMM(dim=2, n_components = 2, data=data, method="kmeans")

        ##if self.Debug:
          #  print gmm
        # print gmm
        gmm_data = []
        for comp in gmm.comps:
            gmm_data.append([comp.mu[0], comp.mu[1]])
            # draw1dnormal(comp)

        gmm_data = sorted(gmm_data, key=lambda gmm_data: gmm_data[0])
        sky_peak = gmm_data[0][0]
        disk_peak = gmm_data[1][0]

        h_histogram = h_histogram[:-1]
        width = 0.7 * (bins[1] - bins[0])
        center = (bins[:-1] + bins[1:]) / 2

        #
        sky_peak = (dirty_map_max - dirty_map_min) * sky_peak / 2000.
        disk_peak = (dirty_map_max - dirty_map_min) * disk_peak / 2000.
        # logger.debug("Peak Value: sky_peak:%f  disk_peak:%f" % (sky_peak, disk_peak))
        print sky_peak,disk_peak

        return sky_peak, disk_peak

    def preclean(self):

        ## Create the PSF & dirty image
        #   dpsf - PSF, gpu_im ( dirty image)
        #   dpsf is computed by CPU, gpu_im is in the GPU
        # nx - 2 imsize, it means 2048 when imsize=1024
        nx = np.int32(2 * self.imsize)

        # create fft plan nx*nx
        # self.plan = fft.Plan((np.int(nx), np.int(nx)), np.complex64, np.complex64)

        d_dirty = np.zeros((np.int(self.imsize), np.int(self.imsize)), np.float32)

        dpsf, gpu_im,fdisk = self.gridvis(0,0)   ###706  (2,-168)  200(-11,167)
        gpu_disk = fdisk
        # , misc.minabs(gpu_im)

        gpu_dpsf = dpsf
        h_disk = gpu_disk
        # gpu_dpsf2 = gpu.to_gpu(dpsf2)

        # Clean the PSF
        if self.imsize >= 1024:
            cpsf = self.clean_beam(dpsf, 50)  # self.imsize / 32.)
        elif self.imsize >= 512:
            cpsf = self.clean_beam(dpsf, self.imsize / 24.)
        elif self.imsize >= 256:
            cpsf = self.clean_beam(dpsf, self.imsize / 16.)

        # Histogram
        sky_peak, disk_peak = self.cuda_histogram(gpu_im, 2000)
        gpu_im_sky,cleanmap_sky = self.hogbom_clean(gpu_im,dpsf,cpsf,sky_peak)

        dirty = gpu_im_sky

        ## Run CLEAN
        # Clean till >=Disk
        height, width = np.shape(gpu_im)
        gpu_pmodel = np.zeros([height, width], dtype=np.float32)
        gpu_clean = np.zeros([height, width], dtype=np.float32)
        gpu_dirty_shift = np.zeros([height, width], dtype=np.float32)




        # h_disk_im  = self.sub_sun_disk_offset(h_disk, dirty)

        gpu_disk_im = self.sub_sun_disk_offset(h_disk, dirty)
        h_disk_im = gpu_disk_im


        # sky_peak, disk_peak = self.cuda_histogram(gpu_im, 2000)
        #
        # print "Peak:", sky_peak, disk_peak
        print "x_offset=",-np.argmax(np.max(h_disk_im, axis=0)) + self.imsize / 2, "y_offset=",-self.imsize / 2 + np.argmax(np.max(h_disk_im, axis=1))
        return -np.argmax(np.max(h_disk_im, axis=0)) + self.imsize / 2, -self.imsize / 2 + np.argmax(np.max(h_disk_im, axis=1)),cpsf

    def MaxPosition(self,map):
        x = map
        raw, column = x.shape
        position = np.argmax(x)
        m, n = divmod(position, column)
        return m,n

    def hogbom_clean(self,dirtyMap,dirtyBeam,cleanbeam,thresh=0.2):
        gain = 0.1
        imsize = self.imsize
        dpsf = dirtyBeam
        dirtymap = dirtyMap
        cleanBeam = cleanbeam
        dpsf = 1.*dpsf/np.max(dpsf)
        imax = np.max(np.abs(dirtymap))
        scale = imax*gain
        thresh_val=thresh
        cleanMap = np.zeros((imsize,imsize),np.float32)
        i = 0
        residualmap = dirtymap
        t_start = time.time()
        print scale,thresh_val

        while (np.abs(imax)>thresh_val) and i<200:
            print "Hogbom iteration",i
            x,y = self.MaxPosition(residualmap)
            imax = np.abs(residualmap[x][y])
            print x,y,residualmap[x][y]
            dpsf_temp = dpsf[imsize-x:2*imsize-x,imsize-y:2*imsize-y]
	    dpsf_temp = dpsf_temp*1./np.max(dpsf_temp)
	    cpsf_temp = cleanBeam[imsize-x:2*imsize-x,imsize-y:2*imsize-y]
	    residualmap = residualmap-dpsf_temp*gain*imax
	    cleanMap = cleanMap+cpsf_temp*gain*imax
	    i += 1

	    #for idx in range(imsize):
            #    for idy in range(imsize):
            #        bidx = (idx-x)+imsize;
            #        bidy = (idy-y)+1024;
                # if bidx>=0 and bidx<1024 and bidy>0 and bidy<1024:
                    # print bidx,bidy
            #        residualmap[idx][idy] = residualmap[idx][idy]-dpsf[bidx][bidy]*gain*imax
            #        cleanMap[idx][idy] = cleanMap[idx][idy]+cleanBeam[bidx][bidy]*gain*imax
                # print residualmap[idx][idy]
            #i += 1
        cleanImage = cleanMap+residualmap
        t_end = time.time()
        print "clean time is ",t_end-t_start


        return residualmap,cleanImage

    # def serial_clean(self,infile,chosechannel):
    def serial_clean(self,inputfile, outdir, channel, weight, mode, automove, movera, movedec, plot, fits, correct, debug):
        # Load settings for each example
        self.infile = inputfile #'20151101-120849_354161240.uvfits'
        self.outdir= outdir
        self.briggs = np.float32(1e7)  # weight parameter
        self.light_speed = 299792458.  # Speed of light

        self.fitsfile = pyfits.open(self.infile,ignore_missing_end=True)  #open file

        self.telescope = self.fitsfile[0].header['INSTRUME'].strip()
        if self.telescope != 'MUSER':
            logger.error("Current program can only support MUSER.")
            return

        self.channel = self.fitsfile[0].data.data.shape[3]               #channel chose
        self.baseline_number = self.fitsfile[0].header['GCOUNT']
        self.obs_date = self.fitsfile[0].header['DATE-OBS']
        #self.muser_date = datetime.datetime.strptime(self.obs_date[:-3], "%Y-%m-%dT%H:%M:%S.%f")

        if self.infile.find('.fitsidi') != -1:
            self.freq = np.float32(self.fitsfile[7].header['CRVAL3'])  # 299792458vvvv
        elif self.infile.find('.uvfits') != -1:
            self.object = self.fitsfile[0].header['OBJECT']
            self.polarization = np.int32(self.fitsfile[0].header['CRVAL3'])
            self.basefreq = np.float32(self.fitsfile[0].header['CRVAL4'])
            self.bandwidth = np.float32(self.fitsfile[0].header['CDELT4'])
            self.ra = np.float32(self.fitsfile[0].header['OBSRA'])
            self.dec = np.float32(self.fitsfile[0].header['OBSDEC'])
            self.freq = self.basefreq + np.float32(self.fitsfile[1].data["IF FREQ"][0])

        self.h_uu = np.ndarray(shape=(self.baseline_number), dtype='float64')
        self.h_vv = np.ndarray(shape=(self.baseline_number), dtype='float64')
        self.h_rere = np.ndarray(shape=(self.baseline_number), dtype='float32')
        self.h_imim = np.ndarray(shape=(self.baseline_number), dtype='float32')

        for self.chan in range(channel, channel+1):

            self.current_freq = self.freq + self.chan * self.bandwidth + self.bandwidth // 2
            self.angular_resolution = self.light_speed / self.current_freq / 3000 * 180. * 3600 / np.pi #angular resolution

            if self.infile.find('.fitsidi') != -1:
                self.h_uu = np.float64((self.freq + self.chan * 25000000) * self.fitsfile[0].data[:].UU)
                self.h_vv = np.float64((self.freq + self.chan * 25000000) * self.fitsfile[0].data[:].VV)
                for bl in range(0, self.baseline_number):
                    self.h_rere[bl] = np.float32(self.fitsfile[0].data[:].data[bl][0][0][self.chan][0][0])
                    self.h_imim[bl] = np.float32(self.fitsfile[0].data[:].data[bl][0][0][self.chan][0][1])

                    self.h_uu = np.float32(self.h_uu.ravel())
                    self.h_vv = np.float32(self.h_vv.ravel())
                    gcount = np.int32(np.size(self.h_uu))
                    # gcount = len(gcount.ravel())
                    self.h_rere = np.float32(self.h_rere.ravel())
                    self.h_imim = np.float32(self.h_imim.ravel())

                    # print len(h_re),len(h_im)
            elif self.infile.find('.uvfits') != -1:
                good = np.where(self.fitsfile[0].data.data[:, 0, 0, self.chan, 0, 0] != 0)
                # the unit of uu and  vv is seconds
                self.h_uu = np.float64(self.fitsfile[0].data.par('uu')[good])  # * self.current_freq)
                self.h_vv = np.float64(self.fitsfile[0].data.par('vv')[good])  # * self.current_freq)
                gcount = np.int32(np.size(self.h_uu))
                # print self.h_uu
                ## assume data is unpolarized
                self.h_uu *= self.current_freq
                self.h_vv *= self.current_freq

                self.h_rere = np.float32(self.fitsfile[0].data.data[good, 0, 0, self.chan, 0, 0])
                self.h_imim = np.float32(self.fitsfile[0].data.data[good, 0, 0, self.chan, 0, 1])

            if self.freq == 400E6:
                self.imsize = 256
            elif self.freq == 800E6:
                self.imsize = 512
            elif self.freq in [1200E6, 1600E6]:
                self.imsize = 1024

            self.cell = self.angular_resolution / 3.                               # cell one resolution
            self.fov = self.cell * self.imsize                                     # Field of view
            self.number_of_wavelentgh = 1. / (self.cell / 3600. / 180. * np.pi)    #number of wavelentgh

            xoffset,yoffset,cpsf = self.preclean()
            if xoffset%2 ==1:
                xoffset -= 1
            if yoffset%2 ==1:
                yoffset -= 1
            dpsf,dirtymap,disk = self.gridvis(xoffset,yoffset)
            residualmap,cleanImage = self.hogbom_clean(dirtymap,dpsf,cpsf)
            axes = plt.subplot(111)
            axes.set_xticks([])
            axes.set_yticks([])
            plt.imshow(cleanImage,cmap = cm.gist_heat)
            # plt.colorbar()
            prefix = self.infile
            prefix, ext = os.path.splitext(os.path.basename(prefix))
            pathPrefix = self.outdir
            if pathPrefix == None:
                filename = prefix + '_clean_%d.png' % self.chan
            else:
                if pathPrefix[-1:] == '/':
                    pathPrefix = pathPrefix[:-1]
                filename = pathPrefix + '/' + prefix + '_clean_%d.png' % self.chan
            plt.savefig(filename)


