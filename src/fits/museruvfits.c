#include "uvfits.h"
#include "muserrawdata.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "eph_manager.h" /* remove this line for use with solsys version 2 */
#include "novas.h"

#define LONGITUDE 115.2505
//#define LONGITUDE 0.
#define LATITUDE 42.211833333333333
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

int debug=0;

const short int accuracy = 0;
short int error = 0;



int ephemOpen()
{
    double jd_beg, jd_end;
    short int de_num = 0;

    make_on_surface (LATITUDE,LONGITUDE,HEIGHT,0,0, &geo_loc);
    make_observer_on_surface (LATITUDE,LONGITUDE,HEIGHT,0,0,&obs_loc);
    make_cat_entry ("DUMMY","xxx",0,0.0,0.0,0.0,0.0,0.0,0.0,
                    &dummy_star);
    if ((error = make_object (0,10,"Sun",&dummy_star, &sun)) != 0)
    {
        printf ("Error %d from make_object (sun)\n", error);
        return (error);
    }
    if ((error = ephem_open (&jd_beg,&jd_end,&de_num)) != 0)
    {
        if (error == 1)
            printf ("JPL ephemeris file not found.\n");
        else
            printf ("Error reading JPL ephemeris file header.\n");
        return (error);
    }
    else
    {
        printf ("JPL ephemeris DE%d open. Start JD = %10.2f  End JD = %10.2f\n",
                de_num, jd_beg, jd_end);
        printf ("\n");
    }
    return 1;
}

void ephemClose()
{
    ephem_close();
}

int ephemPosition(double jd_utc, double *ra, double *dec, double *dis, double *rat, double *dect, double *dist,double *gast, double *last)
{
    double jd_tt, jd_ut1, jd_tdb, delta_t, zd, az, rar, decr,  theta,
    jd[2], pos[3], vel[3], pose[3], elon, elat, r, lon_rad, lat_rad,
    sin_lon, cos_lon, sin_lat, cos_lat, vter[3], vcel[3];

    int MJD= (int)(jd_utc - 2400000.5);
    printf("MJD:%d\n",MJD);
     if (get_leap_sec(MJD,0.,&leap_secs)==0)
     {
         printf ("Error in get data from Leap Second data.\n");
         return error ;
     }
    printf("Current leap second: %lf\n",leap_secs);


    if (get_iers_data(MJD, &ut1_utc, &x_pole, &y_pole)==0){
        printf ("Error in get data from IERS.\n");
        return error ;
    }
    printf("Current IERS ut1-utc, x, y: %lf %lf %lf\n",ut1_utc,x_pole,y_pole);

    jd_tt = jd_utc + ((double) leap_secs + 32.184) / 86400.0;
    jd_ut1 = jd_utc + ut1_utc / 86400.0;
    delta_t = 32.184 + leap_secs - ut1_utc;

    jd_tdb = jd_tt;          /* Approximation good to 0.0017 seconds. */

    if ((error = app_planet (jd_tt,&sun,accuracy, ra,dec,dis)) != 0)
    {
        printf ("Error %d from app_planet.", error);
        return error;
    }

    if ((error = topo_planet (jd_tt,&sun,delta_t,&geo_loc,accuracy,
                              rat,dect,dist)) != 0)
    {
        printf ("Error %d from topo_planet.", error);
        return error;
    }

    if ((error = sidereal_time (jd_ut1,0.0,delta_t,1,1,accuracy, gast)) != 0)
    {
        printf ("Error %d from sidereal_time.", error);
        return (error);
    }

    *last = *gast + geo_loc.longitude / 15.0;
    if ((*last) >= 24.0)
        (*last) -= 24.0;
    if ((*last) < 0.0)
        (*last) += 24.0;

    theta = era (jd_ut1,0.0);

}

void computeUVW(double h, double d)
{
    double H,DEC;
    H = h*PI/180.;
    DEC = d*PI/180.;
    int ANT1,ANT2,count;
    count=0;
    for(ANT1=0;ANT1<RealAntennasLow-1;ANT1++)
        for(ANT2=ANT1+1;ANT2<RealAntennasLow;ANT2++)
        {
            W[0][count]= (BSL[ANT1][ANT2][0]*cos(DEC)*cos(H)+ BSL[ANT1][ANT2][1]* (-cos(DEC)*sin(H))+ sin(DEC)*BSL[ANT1][ANT2][2])/light_speed;
            U[0][count]=(BSL[ANT1][ANT2][0]*sin(H)+BSL[ANT1][ANT2][1]*cos(H))/light_speed;
            V[0][count]=(-BSL[ANT1][ANT2][0]*sin(DEC)*cos(H)+BSL[ANT1][ANT2][1]*(sin(DEC)*sin(H))+cos(DEC)*BSL[ANT1][ANT2][2])/light_speed;
            /*if (count<=2){*/
             //printf("%lf,%lf\n",U[0][count]*light_speed,V[0][count]*light_speed);
             /*
             printf("UVW: %e %e %e\n",U[0][count],V[0][count],W[0][count]);
             }*/
            /*W[0][count]= (DXYZ[ANT1][ANT2][0]*cos(DEC)*cos(H)+ DXYZ[ANT1][ANT2][1]* (-cos(DEC)*sin(H))+ sin(DEC)*DXYZ[ANT1][ANT2][2])/light_speed;
             U[0][count]=(DXYZ[ANT1][ANT2][0]*sin(H)+DXYZ[ANT1][ANT2][1]*cos(H))/light_speed;
             V[0][count]=(-DXYZ[ANT1][ANT2][0]*sin(DEC)*cos(H)+DXYZ[ANT1][ANT2][1]*(sin(DEC)*sin(H))+cos(DEC)*DXYZ[ANT1][ANT2][2])/light_speed;*/
            count++;
        }

}


void createData(int npol, int pol_type, int nfreq, int nvis,float freq, float freqdelta)
{
    int i;
    Data.n_pol = npol;
    Data.pol_type = pol_type;
    Data.n_freq = nfreq;
    Data.n_vis = nvis;
    Data.cent_freq = freq;
    Data.freq_delta = freqdelta;
    Data.date = &date;
    Data.n_baselines = &n_baselines;
    Data.source = &Source;
    Data.antennas = Ant;
    Data.array = &Array;
    for (i=0;i<nvis;i++) /* Maybe use in the future */
    {
        pvisdata[i] = visdata[i];
        pweightdata[i] = weightdata[i];
        pbaseline[i] = baseline[i];
        pU[i]= U[i];
        pV[i] = V[i];
        pW[i] = W[i];
    }
    Data.visdata =  pvisdata;
    Data.weightdata =pweightdata;
    Data.baseline = pbaseline;
    Data.u = pU;
    Data.v = pV;
    Data.w = pW;
}

void createSource(double sra, double sdec, double rfreq)
{
    /*typedef struct _source_table {
     char name[SIZE_SOURCE_NAME+1];
     int  id;
     int  qual;
     char calcode[4];
     int  freq_id;
     double ra;     decimal hours
     double dec;    decimal degrees
     } source_table; */
    sprintf(Source.name,"%s","CSRHLOW");
    Source.id = 1;
    Source.qual = 0;
    sprintf(Source.calcode,"%s","NUL");
    Source.freq_id = 1;
    Source.ra = sra;
    Source.dec  = sdec;
    Source.restfreq=rfreq;
}

void createArray()
{
    /*typedef struct _array_table {
     int   n_ant;
     double xyz_pos[3];    the X,Y,Z coord of the array in conventional radio astronomy units
     char  name[16];
     } array_data;*/
    Array.n_ant = 40;
    sprintf(Array.name,"%s","CSRH");
    Array.xyz_pos[0] = Array.xyz_pos[1]= Array.xyz_pos[2] =0.;
    Locxyz2ITRF(LATITUDE, LONGITUDE, HEIGHT, Array.xyz_pos, Array.xyz_pos+1, Array.xyz_pos+2);
}

void createAnt()
{
    /*
     typedef struct  _ant_table {
     char name[SIZE_ANT_NAME+1];
     double xyz_pos[3];
     float  xyz_deriv[3];
     int  station_num;
     int  mount_type;
     double axis_offset[3];
     float pol_angleA;
     float pol_calA;
     float pol_angleB;
     float pol_calB;
     char pol_typeA[SIZE_POL_TYPE];
     char pol_typeB[SIZE_POL_TYPE];
     } ant_table;*/

    FILE *fp1;
    int i,j,k;
    double ANT_POS[AntennasLow][3];
    double X,Y,Z;
    char antname[200]={0};
    char *penv = getenv("MUSEROS_HOME");
    char antfile[]="/data/Ant_pos.txt";

    strncpy(antname,penv,strlen(penv));
    strncat(antname,antfile,strlen(antfile));

    if ((fp1=fopen(antname,"r"))==0){
        printf("Cannot open ant_pos.txt\n");
        exit(1);
        };
    //printf("the data of Ant_pos.txt:\n");
    for(i=0;i<40;i++)
    {
        fscanf(fp1,"%lf %lf %lf",&(ANT_POS[i][0]),&(ANT_POS[i][1]),&(ANT_POS[i][2]));
        //printf("%10.3f %10.3f %10.3f\n",ANT_POS[i][0],ANT_POS[i][1],ANT_POS[i][2]);

    }
    fclose(fp1);
    /* Init data */
    for (i=0;i<40;i++){
        /* Set antenna name */
        if (i<=13)
            sprintf(Ant[i].name,"I%c%d",'A',i);

        else if (i<=26)
            sprintf(Ant[i].name,"I%c%d",'B',i-13);
        else
            sprintf(Ant[i].name,"I%c%d",'C',i-26);




        /* Calculate ECEF XYZ */
        Ant[i].xyz_pos[0]=ANT_POS[i][0];
        Ant[i].xyz_pos[1]=ANT_POS[i][1];
        Ant[i].xyz_pos[2]=ANT_POS[i][2];
        Locxyz2ITRF(LATITUDE, LONGITUDE, HEIGHT, Ant[i].xyz_pos, Ant[i].xyz_pos+1, Ant[i].xyz_pos+2);
        //printf("%10.3f %10.3f %10.3f\n",Ant[i].xyz_pos[0],Ant[i].xyz_pos[1],Ant[i].xyz_pos[2]);

        Ant[i].xyz_deriv[0]=Ant[i].xyz_deriv[1]=Ant[i].xyz_deriv[2]=0.;
        Ant[i].station_num=1;
        Ant[i].mount_type=2;
        Ant[i].axis_offset[0]=Ant[i].axis_offset[1]=Ant[i].axis_offset[2]=0.;
        Ant[i].pol_angleA = Ant[i].pol_angleB =0;
        Ant[i].pol_calA = Ant[i].pol_calB =0;
        sprintf(Ant[i].pol_typeA,"%c",'R');
        sprintf(Ant[i].pol_typeB,"%c",'L');
    }

    X=Y=Z=0;
    Locxyz2ITRF(LATITUDE, LONGITUDE, HEIGHT, &X,&Y,&Z);

    for(i=0;i<40;i++)
    {
        Ant[i].xyz_pos[0] -= X;
        Ant[i].xyz_pos[1] -= Y;
        Ant[i].xyz_pos[2] -= Z;
    }
    for(i=0;i<39;i++)
    {
        for(j=i+1;j<40;j++)
        {

            for(k=0;k<3;k++)
            {
                BSL[i][j][k]=Ant[j].xyz_pos[k]-Ant[i].xyz_pos[k];

            }
            //printf("%f %f\n",BSL[i][j][0],BSL[i][j][1]);
            DXYZ[i][j][0]=-sin(PI*LATITUDE/180.0)*BSL[i][j][0]+cos(PI*LATITUDE/180.0)*BSL[i][j][2];
            DXYZ[i][j][1]=BSL[i][j][1];
            DXYZ[i][j][2]=cos(PI*LATITUDE/180.0)*BSL[i][j][0]+sin(PI*LATITUDE/180.0)*BSL[i][j][2];
        }
    }
    /* Locxyz2IRTF(double latitude, double longitude, double height, double *locx, double *locy, double *locz)  */

}



void main(int argc, char **argv)
{
    double obstime;
    int iLoop=1;
    char fitsfile[100];
    char fullfitsfile[200];
    int i,j,k,count;
    double jd_utc, jd_tt, jd_ut1, delta_t, hour;
    double ra,  dec, dis, rat, dect, dist,gast, last;

    char *penv = getenv("MUSEROS_WORK");

    if (argc<=1) {
        printf("Usage: csrhuvfits <filename>n");
        exit(0);
    }
    /*  Init Array and Antenna Table */
    createArray();
    printf("Create Array successfully\n");
    createAnt();
    printf("Create Antenna successfully\n");

    if (argc==3)
    {
        debug = 1;
        printf("DEBUG MODE\n");
    }
    /* Open raw data file */
    if (openCSRHFile(argv[1])==0) {
        printf("Cannot open file %s\n",argv[1]);
        exit(1);
    }
    printf("Open Raw Data File:%s successfully\n",argv[1]);


    ephemOpen();
    printf("Open Ephem File successfully\n");

    /* Search the beginning of the file */
    //while (searchFrameHeader())

    if (searchFrameHeader())
    {
        printf("Find a frame header\n");
        if (readOneFrame())
        {
            printf("Read a frame successfully\n");
            csrhPolarization = iLoop % 2 - 2;
            iLoop += 1;

            createData(1,csrhPolarization, 16, 1, csrhFrequency+20000000.,25000000);
            printf("Init UVFits data  successfully\n");

            /* Compute JD */


            hour = currentFrameTime.Hour -8 + (double)currentFrameTime.Minute/60.+ (currentFrameTime.Second+ (double)(currentFrameTime.miliSecond)/1000.+(double)(currentFrameTime.macroSecond)/1000000.+(double)(currentFrameTime.nanoSecond)/1000000000.)/3600.;

            jd_utc = julian_date (currentFrameTime.Year,currentFrameTime.Month,currentFrameTime.Day,hour);
            jd_tt = jd_utc + ((double) leap_secs + 32.184) / 86400.0;
            jd_ut1 = jd_utc + ut1_utc / 86400.0;
            delta_t = 32.184 + leap_secs - ut1_utc;


            ephemPosition(jd_utc, &ra, &dec, &dis, &rat, &dect, &dist,&gast, &last);
            printf("Compute target position successfully %lf %lf\n",rat,dect);
            sprintf(fitsfile,"%4d%02d%02d-%02d%02d%02d_%03d%03d%03d.uvfits",
                    currentFrameTime.Year, currentFrameTime.Month, currentFrameTime.Day,
                    currentFrameTime.Hour-8, currentFrameTime.Minute, currentFrameTime.Second, currentFrameTime.miliSecond,currentFrameTime.macroSecond, currentFrameTime.nanoSecond);
            printf("Filename: %s\n",fitsfile);
            createSource(ra*15-360, dec, csrhFrequency);
            printf("Create source successfully\n");
            date = jd_utc;
            n_baselines = 780;
            /* Gast - Greenwitch Apparent Sidereal time - apparent RA */
            printf("Hour and DEC: %lf %lf\n",last-ra, dec);
            //if (debug ==1)
            //    computeUVW(0,0);
            //else



                computeUVW((last - ra)*15., dec);

            /* Only need to write the data wit size of RealAntennasLow */
            count=0;
            for (i=0;i<RealAntennasLow-1; i++)
                for (j=i+1;j<RealAntennasLow;j++)
                    baseline[0][count++] = (i+1)*256+j+1;

            count=0;




            for (j=0;j<RealAntennasLow-1; j++)
                for (k= j+1;k<RealAntennasLow; k++)
                    for(i=0;i<16;i++)
                    {
                        visdata[0][count*2] =lowCSRHData[j][k][i].real;
                        visdata[0][count*2+1] =lowCSRHData[j][k][i].imaginary;
                        weightdata[0][count] = 1.;
                        count++;
                    }



            if (strlen(penv)!=0){
               strncpy(fullfitsfile,penv,strlen(penv));
               strncat(fullfitsfile,"/",1);
               strncat(fullfitsfile,fitsfile,strlen(fitsfile));
               writeUVFITS(fullfitsfile,&Data);
            }

            else
            {

                writeUVFITS(fitsfile,&Data);
            }

            printf("Write fille OK.\n");
        }
    }
    ephemClose();
    closeCSRHFile();
}
