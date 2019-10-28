#!python
# !/usr/bin/env python -tt
# encoding: utf-8
#
# Created by Holger Rapp on 2009-03-11.
# HolgerRapp@gmx.net
#

clean_code = \
    """
    #define WIDTH 6
    #define NCGF 12
    #define HWIDTH 3
    #define STEP 4

    // *********************
    // MAP KERNELS
    // *********************

    __kernel void gridVis_wBM_kernel(__global float *cgf,__global float2 *Grd, __global float2 *bm,
                                     __global float2 *sf,__global int *cnt,__global float *d_u,
                                     __global float *d_v,__global float *d_re,__global float *d_im,
                                     int nu, float du,int gcount,int umax,int vmax,int pangle){

        int iu=get_global_id(0);
        int iv=get_global_id(1);
        int u0 = 0.5*nu;
        if(iu >= u0 && iu <= u0+umax && iv <= u0+vmax){
            for (int ivis = 0; ivis < gcount; ivis++){
                float mu = d_u[ivis];
                float mv = d_v[ivis];
                int hflag = 1;
                if (mu < 0){
                    hflag = -1;
                    mu = -1*mu;
                    mv = -1*mv;
                }
                float uu, vv;
                uu = mu/du + u0;
                vv = mv/du + u0;

                int iuuu=iu-uu;
                int ivvv=iv-vv;
                int cnu=abs(iuuu);
                int cnv=abs(ivvv);
                //int cnu=abs(iu-uu), cnv=abs(iv-vv);
                int ind = iv*nu+iu;
                if (cnu < HWIDTH && cnv < HWIDTH){
                    //float wgt = cgf[int(round(4.6*cnu+NCGF-0.5))]*cgf[int(round(4.6*cnv+NCGF-0.5))];
                    float roundcnu=4.6*cnu+NCGF-0.5;
                    float roundcnv=4.6*cnv+NCGF-0.5;
                    int round1=round(roundcnu);
                    int round2=round(roundcnv);
                    float wgt = cgf[round1]*cgf[round2];
                    Grd[ind].x +=       wgt*d_re[ivis];
                    Grd[ind].y += hflag*wgt*d_im[ivis];
                    cnt[ind]   += 1;
                    bm [ind].x += wgt;
                    sf[ind].x   = 1;
                    sf[ind].y   = 1;
                }

                if (iu-u0 < HWIDTH && mu/du < HWIDTH) {
                    mu = -1*mu;
                    mv = -1*mv;
                    uu = mu/du+u0;
                    vv = mv/du+u0;
                    int iuuu=iu-uu;
                    int ivvv=iv-vv;
                    int cnu=abs(iuuu);
                    int cnv=abs(ivvv);

                    if (cnu < HWIDTH && cnv < HWIDTH){
                        //float wgt = cgf[int(round(4.6*cnu+NCGF-0.5))]*cgf[int(round(4.6*cnv+NCGF-0.5))];
                        float roundcnu=4.6*cnu+NCGF-0.5;
                        float roundcnv=4.6*cnv+NCGF-0.5;
                        int round1=round(roundcnu);
                        int round2=round(roundcnv);
                        float wgt = cgf[round1]*cgf[round2];
                        Grd[ind].x +=          wgt*d_re[ivis];
                        Grd[ind].y += -1*hflag*wgt*d_im[ivis];
                        cnt[ind]   += 1;
                        bm[ind].x += wgt;
                        sf[ind].x   = 1;
                        sf[ind].y   = 1;
                    }
                }
            }
        }
    }

    __kernel void dblGrid_kernel(__global float2 *Grd, int nu, int hfac){

        int iu=get_global_id(0);
        int iv=get_global_id(1);
        int u0 = 0.5*nu;
        if (iu >= 0 && iu < u0 && iv < nu && iv >= 0){
            int niu = nu-iu;
            int niv = nu-iv;
            if(niu!=2048&&niv!=2048){
            Grd[iv*nu+iu].x =      Grd[niv*nu+niu].x;
            Grd[iv*nu+iu].y = hfac*Grd[niv*nu+niu].y;
            }
            if(niu==1024 && niv==1024){
            //printf("####grd.x: %.12f\\n",Grd[iv*nu+iu].x);
            //printf("####grd.y: %.12f\\n",Grd[iv*nu+iu].y);
            }
        }
    }

    __kernel void wgtGrid_kernel(__global float2 *Grd,__global int *cnt, float briggs, int nu){
        int iu=get_global_id(0);
        int iv=get_global_id(1);
        int u0 = 0.5*nu;
        if (iu >= u0 && iu < nu && iv < nu){
            if (cnt[iv*nu+iu]!= 0){
                int ind = iv*nu+iu;
                float foo = cnt[ind];
                float wgt = 1./sqrt(1 + foo*foo/(briggs*briggs));
                Grd[ind].x = Grd[ind].x*wgt;
                Grd[ind].y = Grd[ind].y*wgt;
            }
        }
    }

    __kernel void nrmGrid_kernel(__global float *Grd, float nrm, int nu){

        int iu=get_global_id(0);
        int iv=get_global_id(1);
        if (iu < nu &&  iv < nu){
            Grd[iv*nu + iu] = Grd[iv*nu+iu]*nrm;
        }
    }

    __kernel void corrGrid_kernel(__global float2 *Grd,__global float *corr, int nu){

        int iu=get_global_id(0);
        int iv=get_global_id(1);
        if (iu < nu && iv < nu ){
            Grd[iv*nu + iu].x = Grd[iv*nu+iu].x*corr[nu/2]*corr[nu/2]/(corr[iu]*corr[iv]);
            Grd[iv*nu + iu].y = Grd[iv*nu+iu].y*corr[nu/2]*corr[nu/2]/(corr[iu]*corr[iv]);
        }
    }

    // *********************
    // BEAM KERNELS
    // *********************
    __kernel void nrmBeam_kernel(__global float *bmR, float nrm, int nu){

        int iu=get_global_id(0);
        int iv=get_global_id(1);
        if (iu < nu && iv < nu){
            bmR[iv*nu+iu] = nrm*bmR[iv*nu+iu];
        }
    }

    // *********************
    // MORE semi-USEFUL KERNELS
    // *********************

    __kernel void shiftGrid_kernel(__global float2 *Grd,__global float2 *nGrd, int nu){

        int iu=get_global_id(0);
        int iv=get_global_id(1);
        if (iu < nu && iv < nu){
            int niu,niv,nud2 = 0.5*nu;
            if(iu < nud2) niu = nud2+iu;
            else niu = iu-nud2;
            if(iv < nud2) niv = nud2+iv;
            else niv = iv-nud2;
            nGrd[niv*nu + niu].x = Grd[iv*nu+iu].x;
            nGrd[niv*nu + niu].y = Grd[iv*nu+iu].y;
            //if(iu==0 && iv==0)
            //printf("*****niu niv nud2:%d,%d,%d\\n",niu,niv,nud2);
        }
    }

    __kernel void trimIm_kernel(__global float2 *im,__global float *nim, int nx, int nnx){

        int ix=get_global_id(0);
        int iy=get_global_id(1);
        if(ix==0 && iy==0){
        //printf("trimIm kernel nx,nnx:%d,%d",nx,nnx);
        //printf("%f",im[512*2048+512].x);
        }
        if (iy < nnx && ix < nnx){
            nim[iy*nnx + ix] = im[(nx/2 - nnx/2 + iy)*nx+(nx/2-nnx/2)+ix].x;
        }
    }

    __kernel void trim_float_image_kernel(__global float *im, __global float *nim, int nx, int nnx){

        int ix=get_global_id(0);
        int iy=get_global_id(1);
        if (iy < nnx && ix < nnx){
            nim[iy*nnx + ix] = im[(nx/2 - nnx/2 + iy)*nx+(nx/2 - nnx/2 + ix)];
        }
    }

    __kernel void copyIm_kernel(__global float2 *im,__global float *nim, int nx){

        int ix=get_global_id(0);
        int iy=get_global_id(1);
        if (iy < nx && ix < nx){
            nim[iy*nx + ix] = im[(iy)*nx+ix].x;
        }
    }

    __kernel void copyRIm_kernel(__global float *im, __global float2 *nim, int nx){

        int ix=get_global_id(0);
        int iy=get_global_id(1);
        if (iy < nx && ix < nx){
            nim[(iy)*nx+ix].x = im[iy*nx + ix];
            nim[(iy)*nx+ix].y = 0;
        }
    }

    __kernel void diskGrid_kernel( __global float2 *Grd, int nu, int radius, int light){

        int iu = get_global_id(0);
        int iv = get_global_id(1);
        int u0 = 0.5*nu;
        int niu, niv;
        if (iu >= 0 && iu <= u0 && iv <= nu && iv >= 0){
            float temp=1.0*(iu-u0)*(iu-u0)+1.0*(iv-u0)*(iv-u0);
            float sqrt1=sqrt(temp);
            float radius1=1.0*radius;
            if (sqrt1<=radius1){
                Grd[iv*nu+iu].x = light;
                Grd[iv*nu+iu].y = 0;
                niu = nu- iu;
                niv = iv ;
                Grd[niv*nu+niu].x = light;
                Grd[niv*nu+niu].y = 0;
                niu = iu;
                niv = nu- iv;
                Grd[niv*nu+niu].x = light;
                Grd[niv*nu+niu].y = 0;
                niu = nu- iu;
                niv = nu- iv;
                Grd[niv*nu+niu].x = light;
                Grd[niv*nu+niu].y = 0;
            }
        }
    }
    """
# -------------------
# CLEAN kernels
# -------------------

find_max_kernel_source = \
    """
    // Function to compute 1D array positioncuda_gri
    #define GRID(x,y,W) ((x)+((y)*W))

    __kernel void find_max_kernel(__global float* dimg,__global int* maxid,float maxval,
                                  int W, int H, __global float* model){
        // Identify place on grid
        int idx = get_global_id(0);
        int idy = get_global_id(1);
        int id  = GRID(idy,idx,H);

        // Ignore boundary pixels
        if (idx>-1 && idx<W && idy>-1 && idy<H) {
            // Is this greater than the current max?
            if (dimg[id]==maxval) {
                // Do an atomic replace
                // This might be #improvable#, but I think atomic operations are actually most efficient
                // in a situation like this where few (typically 1) threads will pass this conditional.
                // Note: this is a race condition!  If there are multiple instances of the max value,
                // this will end up returning one randomly
                // See atomic operation info here:
                //http://rpm.pbone.net/index.php3/stat/45/idpl/12463013/numer/3/nazwa/atomicExch
                // See also https://www.sharcnet.ca/help/index.php/CUDA_tips_and_tricks
                int dummy = atomic_xchg(maxid,id);
            }
        }
        // Update the model
        //barrier(CLK_LOCAL_MEM_FENCE);
        barrier(CLK_GLOBAL_MEM_FENCE);
        if (id==maxid[0]) {
            model[id]+=dimg[id];
        }
    }
    """

sub_beam_kernel_source = \
    """
    // Function to compute 1D array position
    #define GRID(x,y,W) ((x)+((y)*W))
    // Inverse
    #define IGRIDX(x,W) ((x)%(W))
    #define IGRIDY(x,W) ((x)/(W))

    __kernel void sub_beam_kernel(__global  float* dimg, __global  float* dpsf,__global  int* mid,
                                   __global  float* cimg,__global  float* cpsf,float scaler,
                                   int W, int H, int flag){

        int idx = get_global_id(0);
        int idy = get_global_id(1);
        int id  = GRID(idy,idx,H);
        // Identify position of maximum
        int midy = IGRIDX(mid[0],W);
        int midx = IGRIDY(mid[0],H);
        // Calculate position on the dirty beam
        int bidy = (idx-midx)+W;
        int bidx = (idy-midy)+H;
        int bid = GRID(bidx,bidy,2*W);

        // Stay within the bounds
        if (idx>-1 && idx<W && idy>-1 && idy<H && bidx>-1 && bidx<2*W && bidy>-1 && bidy<2*H) {
            //if (idx>-1 && idx<W && idy>-1 &&  idy<H) {
            // Subtract dirty beam from dirty map
            dimg[id]=dimg[id]-dpsf[bid]*scaler;
            // Add clean beam to clean map
        if (flag==1)
            cimg[id]=cimg[id]+cpsf[bid]*scaler;
        }
    }
    """

histogram_kernel_source = \
    """
    #define GRID(x,y,W) ((x)+((y)*W))
    __kernel void sub_histogram_kernel (__global float *dimg,int W, int H,__global int *histo,
                                       int max, int min,	int binsize){
        // Identify place on grid
        int idx = get_global_id(0);
        int idy = get_global_id(1);
        if (idy<W && idx< H){
            int id  = GRID(idy,idx,H);
            int offset = (dimg[id] - min)*(binsize-1.)/(max-min);
            if (offset<binsize)
                atomic_add(&histo[offset] , 1 );
        }
    }
    """

filter_kernel_source = \
    """
    __kernel void sub_mean_average_kernel(__global  int *in, __global  int *out, int height,
                                          int width, int radius){
        // Identify place on grid
        int idx = get_global_id(0);
        int idy = get_global_id(1);
	//printf("idx %d  idy  %d  ", idx, idy);
        int id  = idy+idx*width;
        int i = 0;
        float ss = 0;
        int s=0;
        out[id] = 0;
        if (idy < width - radius -1) {
            for (i=0;i<radius;i++)
                 ss += in[id+i];
            s=ss/radius;
            out[id] = s;

        }
    }
    """

sub_cuda_cyclic_shift_kernel_source = \
    """
    __kernel void sub_cuda_cyclic_shift_kernel(__global float2 *in,__global float2 *out,
                                               int N,	int x_offset, int y_offset){
        int tidx = get_global_id(0);
        int tidy = get_global_id(1);
        float cosv,sinv;
        if (tidx < N && tidy <N ){
            int index=tidx*N+tidy;
            float angle=2*3.1415926535*(x_offset*(tidx-N/2)+y_offset*(tidy-N/2))/N;
            //sincos(angle,&sinv,&cosv);
            sinv =  sin(angle);
            cosv =  cos(angle);
            out[index].x = in[index].x*cosv-in[index].y*sinv;
            out[index].y = in[index].x*sinv+in[index].y*cosv;
        }
    }
    """

cycle_shift_kernel_source = \
    """
    __kernel void sub_cycle_shift_kernel( __global float *im, __global float *nim,
                                         int nx, int x_offset, int y_offset){
        int ix = get_global_id(0);
        int iy = get_global_id(1);
        if (iy < nx && ix < nx){
            int x = (ix+x_offset);
            int y = (iy+y_offset);
            if (x>nx)
                x = x%nx;
            if (x<0)
                x = nx+x;
            if (y>nx)
                y = y%nx;
            if (y<0)
                y = nx+y;
            if (y<nx && x < nx)
                nim[y*nx + x] = im[(iy)*nx+ix];
        }
    }
    """

sub_rotation_kernel_source = \
    """
    __kernel void sub_rotate_image_kernel(__global float* src,__global float* trg,
                                          int imageWidth,int imageHeight, 	float angle,float scale){
        // compute thread dimension
        int x = get_global_id(0);
        int y = get_global_id(1);

        // compute target address
        int idx = x + y * imageWidth;

        int xA = (x - imageWidth/2 );
        int yA = (y - imageHeight/2 );

        int xR = (int)floor(1.0f/scale * (xA * cos(angle) - yA * sin(angle)));
        int yR = (int)floor(1.0f/scale * (xA * sin(angle) + yA * cos(angle)));

        float src_x = xR + imageWidth/2;
        float src_y = yR + imageHeight/2;

        if (src_x >= 0.0f && src_x < imageWidth && src_y >= 0.0f && src_y < imageHeight) {
            // BI - LINEAR INTERPOLATION
            float src_x0 = (float)(int)(src_x);
            float src_x1 = (src_x0+1);
            float src_y0 = (float)(int)(src_y);
            float src_y1 = (src_y0+1);

            float sx = (src_x-src_x0);
            float sy = (src_y-src_y0);


            int idx_src00 = min(max(0.0f,src_x0   + src_y0 * imageWidth),imageWidth*imageHeight-1.0f);
            int idx_src10 = min(max(0.0f,src_x1   + src_y0 * imageWidth),imageWidth*imageHeight-1.0f);
            int idx_src01 = min(max(0.0f,src_x0   + src_y1 * imageWidth),imageWidth*imageHeight-1.0f);
            int idx_src11 = min(max(0.0f,src_x1   + src_y1 * imageWidth),imageWidth*imageHeight-1.0f);

            trg[idx] = 0.0f;

            trg[idx]  = (1.0f-sx)*(1.0f-sy)*src[idx_src00];
            trg[idx] += (     sx)*(1.0f-sy)*src[idx_src10];
            trg[idx] += (1.0f-sx)*(     sy)*src[idx_src01];
            trg[idx] += (     sx)*(     sy)*src[idx_src11];
        }
        else {
            trg[idx] = 0.0f;
        }
    }
    """

dot_mul_kernel_source = \
    """
    __kernel void sub_dot_mul_kernel(__global const float2 *A, __global const float2 *B,
                                     __global const float2 *C, int width, int height){
        // Identify place on grid
        int idx = get_global_id(0);
        int idy = get_global_id(1);
        int id  = idy+idx*width;

        C[id].x = A[id].x*B[id].x - A[id].y*B[id].y ; //cuCaddf(Csub,cuCmulf(As[ty][k],Bs[k][tx]));
        C[id].y = A[id].y*B[id].x + A[id].x*B[id].y ;
    }
    """

matrix_mul_kernel_source = \
    """
    //#include <cuComplex.h>
    #define MATRIX_SIZE 1024
    #define BLOCK_SIZE 8

    __kernel void sub_matrix_mul_kernel(__global const float2 *A, __global const float2 *B,
                                        __global const float2 *C, int wA, int wB){
        //const int wA = MATRIX_SIZE;
        //const int wB = MATRIX_SIZE;

        // Block index
        int bx = get_local_size(0);
        int by = get_local_size(1);

        // Thread index
        int tx = get_local_id(0);
        int ty = get_local_id(1);

        // Index of the first sub-matrix of A processed by the block
        int aBegin = wA * BLOCK_SIZE * by;
        // Index of the last sub-matrix of A processed by the block
        int aEnd   = aBegin + wA - 1;
        // Step size used to iterate through the sub-matrices of A
        int aStep = BLOCK_SIZE;

        // Index of the first sub-matrix of B processed by the block
        int bBegin = BLOCK_SIZE * bx;
        // Step size used to iterate through the sub-matrcies of B
        int bStep = BLOCK_SIZE * wB;

        // The element of the block sub-matrix that is computed by the thread
        float2 Csub;
        Csub.x = 0; Csub.y =0; //= make_cuFloatComplex(0,0);
        // Loop over all the sub-matrices of A and B required to compute the block sub-matrix
        for (int a = aBegin, b = bBegin; a <= aEnd;    a += aStep, b += bStep){
            // Shared memory for the sub-matrix of A
            __local float2 As[BLOCK_SIZE][BLOCK_SIZE];
            // Shared memory for the sub-matrix of B
            __local float2 Bs[BLOCK_SIZE][BLOCK_SIZE];

            // Load the matrices from global memory to shared memory;
            // each thread loads one element of each matrix
            As[ty][tx].x = A[a + wA*ty + tx].x; As[ty][tx].y = A[a + wA*ty + tx].y;
            Bs[ty][tx].x = B[b + wB*ty + tx].x; Bs[ty][tx].y = B[b + wB*ty + tx].y;

            // Synchronize to make sure the matrices are loaded
            barrier(CLK_LOCAL_MEM_FENCE);

            // Multiply the two matrcies together
            // each thread computes one element of the block sub-matrix
            for (int k = 0; k < BLOCK_SIZE; ++k){
                //cuCaddf(Csub,cuCmulf(As[ty][k],Bs[k][tx]));
                Csub.x = Csub.x + (As[ty][k].x*Bs[k][tx].x - As[ty][k].y*Bs[k][tx].y );
                Csub.y = Csub.y + (As[ty][k].y*Bs[k][tx].x + As[ty][k].x*Bs[k][tx].y );
            }

            // Synchronize to make sure that the preceding computation
            // is done before loading two new sub-matrices of A and B in the next iteration
            barrier(CLK_LOCAL_MEM_FENCE);
        }
        // Write the block sub-matrix to global memory
        // each thread writes one element
        int cc = wB * BLOCK_SIZE * by + BLOCK_SIZE * bx;
        C[cc + wB*ty + tx].x = Csub.x;
        C[cc + wB*ty + tx].y = Csub.y;
    }
    """

rotation_kernel_source = """
    __kernel void rotateImage_Kernel(__global float2* trg, __global const float2* src,
                                     int imageWidth,int imageHeight, float angle, float scale){
        // compute thread dimension
        int x = get_global_id(0);
        int y = get_global_id(1);

        // compute target address
        int idx = x + y * imageWidth;

        int xA = (x - imageWidth/2 );
        int yA = (y - imageHeight/2 );

        int xR = (int)floor(1.0f/scale * (xA * cos(angle) - yA * sin(angle)));
        int yR = (int)floor(1.0f/scale * (xA * sin(angle) + yA * cos(angle)));

        float src_x = xR + imageWidth/2;
        float src_y = yR + imageHeight/2;

        if (src_x >= 0.0f && src_x < imageWidth && src_y >= 0.0f && src_y < imageHeight) {
            // BI - LINEAR INTERPOLATION
            float src_x0 = (float)(int)(src_x);
            float src_x1 = (src_x0+1);
            float src_y0 = (float)(int)(src_y);
            float src_y1 = (src_y0+1);

            float sx = (src_x-src_x0);
            float sy = (src_y-src_y0);

            int idx_src00 = min(max(0.0f,src_x0   + src_y0 * imageWidth),imageWidth*imageHeight-1.0f);
            int idx_src10 = min(max(0.0f,src_x1   + src_y0 * imageWidth),imageWidth*imageHeight-1.0f);
            int idx_src01 = min(max(0.0f,src_x0   + src_y1 * imageWidth),imageWidth*imageHeight-1.0f);
            int idx_src11 = min(max(0.0f,src_x1   + src_y1 * imageWidth),imageWidth*imageHeight-1.0f);

            trg[idx].y = 0.0f;

            trg[idx].x  = (1.0f-sx)*(1.0f-sy)*src[idx_src00].x;
            trg[idx].x += (     sx)*(1.0f-sy)*src[idx_src10].x;
            trg[idx].x += (1.0f-sx)*(     sy)*src[idx_src01].x;
            trg[idx].x += (     sx)*(     sy)*src[idx_src11].x;
        }
        else {
            trg[idx].x = 0.0f;
            trg[idx].y = 0.0f;
        }
        //DEVICE_METHODE_LAST_COMMAND;
    }


    __kernel void translateImage_Kernel(__global float2* trg, __global const float2* src,
                                        const unsigned int imageWidth, const unsigned int imageHeight,
                                        const float tX, const float tY){
        // compute thread dimension
        const unsigned int x = get_global_id(0);
        const unsigned int y = get_global_id(1);

        // compute target address
        const unsigned int idx = x + y * imageWidth;

        const int xB = ((int)x + (int)tX );
        const int yB = ((int)y + (int)tY );

        if (xB >= 0 && xB < imageWidth && yB >= 0 && yB < imageHeight) {
            trg[idx] = src[xB + yB * imageWidth];
        }
        else {
            trg[idx].x = 0.0f;
            trg[idx].y = 0.0f;
        }
    //DEVICE_METHODE_LAST_COMMAND;
   }
   """
import pyopencl as cl
from pyopencl.elementwise import ElementwiseKernel
import numpy as np

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

# add_noise_kernel
add_noise_kernel = ElementwiseKernel(ctx, \
                                     "float *a, float* b, int N", \
                                     "b[i] = a[i]+b[i]", \
                                     "gpunoise")
# build clean_code kernel
prg1 = cl.Program(ctx, clean_code).build()
gridVis_wBM_kernel = prg1.gridVis_wBM_kernel
shiftGrid_kernel = prg1.shiftGrid_kernel
nrmGrid_kernel = prg1.nrmGrid_kernel
wgtGrid_kernel = prg1.wgtGrid_kernel
dblGrid_kernel = prg1.dblGrid_kernel
corrGrid_kernel = prg1.corrGrid_kernel
nrmBeam_kernel = prg1.nrmBeam_kernel
trimIm_kernel = prg1.trimIm_kernel
copyIm_kernel = prg1.copyIm_kernel
copyRIm_kernel = prg1.copyRIm_kernel
diskGrid_kernel = prg1.diskGrid_kernel
trim_float_image_kernel = prg1.trim_float_image_kernel
# build find_max_kernel_source kernel
prg2 = cl.Program(ctx, find_max_kernel_source).build()
find_max_kernel = prg2.find_max_kernel
# build sub_beam_kernel_source kernel
prg3 = cl.Program(ctx, sub_beam_kernel_source).build()
sub_beam_kernel = prg3.sub_beam_kernel
# build histogram_kernel_source kernel
prg4 = cl.Program(ctx, histogram_kernel_source).build()
sub_histogram_kernel = prg4.sub_histogram_kernel
# build filter_kernel_source kernel
prg5 = cl.Program(ctx, filter_kernel_source).build()
sub_mean_average_kernel = prg5.sub_mean_average_kernel
# build sub_cuda_cyclic_shift_kernel_source kernel
prg6 = cl.Program(ctx, sub_cuda_cyclic_shift_kernel_source).build()
sub_cuda_cyclic_shift_kernel = prg6.sub_cuda_cyclic_shift_kernel
# build cycle_shift_kernel_source kernel
prg7 = cl.Program(ctx, cycle_shift_kernel_source).build()
sub_cycle_shift_kernel = prg7.sub_cycle_shift_kernel
# build sub_rotation_kernel_source kernel
prg8 = cl.Program(ctx, sub_rotation_kernel_source).build()
sub_rotate_image_kernel = prg8.sub_rotate_image_kernel
# build dot_mul_kernel_source kernel
prg9 = cl.Program(ctx, dot_mul_kernel_source).build()
sub_dot_mul_kernel = prg9.sub_dot_mul_kernel
# build matrix_mul_kernel_source kernel
prg10 = cl.Program(ctx, matrix_mul_kernel_source).build()
sub_matrix_mul_kernel = prg10.sub_matrix_mul_kernel
# build rotation_kernel_source kernel
prg11 = cl.Program(ctx, rotation_kernel_source).build()
rotateImage_Kernel = prg11.rotateImage_Kernel
translateImage_Kernel = prg11.translateImage_Kernel
