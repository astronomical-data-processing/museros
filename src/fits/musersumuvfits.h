#ifndef CSRHSUMUVFITS_H
#define CSRHSUMUVFITS_H

#define LONGITUDE 115.2505
#define LATITUDE 42.2118333333
#define HEIGHT 1365.
#define PI 3.14159265358979
#define light_speed 299792458.

/* Define Antenna Structure Variable */
ant_table Ant[AntennasLow];
source_table Source;
array_data Array;
uvdata Data;

double BSL [AntennasLow][AntennasLow][3];
double DXYZ [AntennasLow][AntennasLow][3];

double date;         /* Julian date. array the size of n_vis */
int  n_baselines;    /* array the size of n_vis. number of baselines for each scan. */
float *pvisdata[4];
float visdata[4][24960];      /* array the size of n_vis whose elements point to arrays of visibiliites the size of n_freq*n_pol*n_baselines complex floats 12480*2 */
float *pweightdata[4];
float weightdata[4][12480];   /* weight data for visibiliites. Same data ordering as above, just float, not complex */
float *pbaseline[4];
float baseline[4][780];     /* same ordering again. encoded baseline using Miriad encoding convention */
double *pU[4];
double U[4][780];           /* arry the size of n_vis whose elements point to arrays of uvw data the size of n_baselines */
double *pV[4];
double V[4][780];
double *pW[4];
double W[4][780];

/* JPL DE405 Ephemsis */
double ut1_utc; /* -0.387845;*/
double x_pole;
double y_pole;
double leap_secs;
on_surface geo_loc;
observer obs_loc;
cat_entry dummy_star;
object sun;

const short int accuracy = 0;
short int error = 0;

/*求平均时用来保存临时文件的数据结构*/
typedef struct 
     {
				CSRHSystemTime currentFrameTime;
    		int csrhPolarization;
    		unsigned long csrhFrequency;
    		float visdata[4][24960];
   	 } averageValue;

#endif
