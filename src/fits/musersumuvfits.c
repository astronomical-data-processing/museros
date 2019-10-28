#include "uvfits.h"
#include "muserrawdata.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "eph_manager.h"	/* remove this line for use with solsys version 2 */
#include "novas.h"
#include "musersumuvfits.h"
#include "fastbit.h"

int debug=0;
int delayFlag=1;
char logName[4096]="csrhsumuvfits.log";
int logFlag=0;
char condition[] = "time>=       and time<=      ";
char dir[4096]="\0"; 
int frameLength = 0;
FILE *fpLog=NULL;
time_t runTime;
struct tm *localTime;
char logRecord[4096], tmp[1024];

int ephemOpen()
{
	double jd_beg, jd_end;
	short int de_num=0;

	make_on_surface(LATITUDE, LONGITUDE, HEIGHT, 0, 0, &geo_loc);
	make_observer_on_surface(LATITUDE, LONGITUDE, HEIGHT, 0, 0, &obs_loc);
	make_cat_entry("DUMMY", "xxx", 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
		       &dummy_star);
	if ((error = make_object(0, 10, "Sun", &dummy_star, &sun)) != 0) {
		printf("Error %d from make_object (sun)\n", error);
		if (logFlag){
			fprintf(fpLog, "Error %d from make_object (sun)\nRun program error\n", error);
		}
		return (error);
	}
	if ((error = ephem_open(&jd_beg, &jd_end, &de_num)) != 0) {
		if (error == 1){
			printf("JPL ephemeris file not found.\n");
			if (logFlag)
				fprintf(fpLog, "JPL ephemeris file not found.\n");
		}
		else{
			printf("Error reading JPL ephemeris file header.\n");
			if (logFlag)
				fprintf(fpLog, "Error reading JPL ephemeris file header.\n");
		}
		return (error);
	} else {
		if (debug)
			printf("JPL ephemeris DE%d open. Start JD = %10.2f  End JD = %10.2f\n\n",de_num, jd_beg, jd_end);
		if (logFlag)
			fprintf(fpLog, "JPL ephemeris DE%d open. Start JD = %10.2f  End JD = %10.2f\n\n",de_num, jd_beg, jd_end);
	}
	return 1;
}

void ephemClose()
{
	ephem_close();
}

void destroy()
{
	int i;
	if (debug == 3)
		printf("destroy function is running\n");
	if (logFlag){
		runTime = time(NULL);
		localTime = localtime(&runTime);
		fprintf(fpLog, "Program finish information:\n\tDate: %d/%02d/%02d\n\tTime: %02d:%02d:%02d\n", (1900+localTime->tm_year), localTime->tm_mon, localTime->tm_mday, localTime->tm_hour, localTime->tm_min, localTime->tm_sec);
		for (i=0; i<80; i++)
			fputc('_', fpLog);
		fputc('\n', fpLog);
	}
	if (fpLog != NULL || logFlag)
		fclose(fpLog);
	if (debug == 3)
		printf("destroy function was finished\n");
}

int ephemPosition(double jd_utc, double *ra, double *dec, double *dis,
	      double *rat, double *dect, double *dist, double *gast,
	      double *last)
{
	double jd_tt, jd_ut1, jd_tdb, delta_t, zd, az, rar, decr, theta,
	    jd[2], pos[3], vel[3], pose[3], elon, elat, r, lon_rad, lat_rad,
	    sin_lon, cos_lon, sin_lat, cos_lat, vter[3], vcel[3];

	int MJD = (int)(jd_utc - 2400000.5);
	if (debug == 2 || debug == 3)
		printf("MJD:%d\n", MJD);
	if (get_leap_sec(MJD, 0., &leap_secs) == 0) {
		printf("Error in get data from Leap Second data.\n");
		return error;
	}
	if (debug == 2 || debug == 3)
		printf("Current leap second: %lf\n", leap_secs);

	if (get_iers_data(MJD, &ut1_utc, &x_pole, &y_pole) == 0) {
		printf("Error in get data from IERS.\n");
		return error;
	}
	if (debug == 2 || debug == 3)
		printf("Current IERS ut1-utc, x, y: %lf %lf %lf\n", ut1_utc, x_pole,
	       y_pole);

	jd_tt = jd_utc + ((double)leap_secs + 32.184) / 86400.0;
	jd_ut1 = jd_utc + ut1_utc / 86400.0;
	delta_t = 32.184 + leap_secs - ut1_utc;

	jd_tdb = jd_tt;		/* Approximation good to 0.0017 seconds. */

	if ((error = app_planet(jd_tt, &sun, accuracy, ra, dec, dis)) != 0) {
		printf("Error %d from app_planet.", error);
		return error;
	}

	if ((error = topo_planet(jd_tt, &sun, delta_t, &geo_loc, accuracy,
				 rat, dect, dist)) != 0) {
		printf("Error %d from topo_planet.", error);
		return error;
	}

	if ((error =
	     sidereal_time(jd_ut1, 0.0, delta_t, 1, 1, accuracy, gast)) != 0) {
		printf("Error %d from sidereal_time.", error);
		return (error);
	}

	*last = *gast + geo_loc.longitude / 15.0;
	if ((*last) >= 24.0)
		(*last) -= 24.0;
	if ((*last) < 0.0)
		(*last) += 24.0;

	theta = era(jd_ut1, 0.0);

}

void computeUVW(double h, double d)
{
	double H, DEC;
	H = h * PI / 180.;
	DEC = d * PI / 180.;
	int ANT1, ANT2, count;
	count = 0;
	for (ANT1 = 0; ANT1 < AntennasLow - 1; ANT1++)
		for (ANT2 = ANT1 + 1; ANT2 < AntennasLow; ANT2++) {
			W[0][count] =
			    (BSL[ANT1][ANT2][0] * cos(DEC) * cos(H) +
			     BSL[ANT1][ANT2][1] * (-cos(DEC) * sin(H)) +
			     sin(DEC) * BSL[ANT1][ANT2][2]) / light_speed;
			U[0][count] =
			    (BSL[ANT1][ANT2][0] * sin(H) +
			     BSL[ANT1][ANT2][1] * cos(H)) / light_speed;
			V[0][count] =
			    (-BSL[ANT1][ANT2][0] * sin(DEC) * cos(H) +
			     BSL[ANT1][ANT2][1] * (sin(DEC) * sin(H)) +
			     cos(DEC) * BSL[ANT1][ANT2][2]) / light_speed;
			/*if (count<=2){
			   printf("%lf %lf %lf\n",BSL[ANT1][ANT2][0],BSL[ANT1][ANT2][1],BSL[ANT1][ANT2][2]);

			   printf("UVW: %e %e %e\n",U[0][count],V[0][count],W[0][count]);
			   } */
			/*W[0][count]= (DXYZ[ANT1][ANT2][0]*cos(DEC)*cos(H)+ DXYZ[ANT1][ANT2][1]* (-cos(DEC)*sin(H))+ sin(DEC)*DXYZ[ANT1][ANT2][2])/light_speed;
			   U[0][count]=(DXYZ[ANT1][ANT2][0]*sin(H)+DXYZ[ANT1][ANT2][1]*cos(H))/light_speed;
			   V[0][count]=(-DXYZ[ANT1][ANT2][0]*sin(DEC)*cos(H)+DXYZ[ANT1][ANT2][1]*(sin(DEC)*sin(H))+cos(DEC)*DXYZ[ANT1][ANT2][2])/light_speed; */
			count++;
		}

}

void createData(int npol, int pol_type, int nfreq, int nvis, float freq,
	   float freqdelta)
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
	for (i = 0; i < nvis; i++) {	/* Maybe use in the future */
		pvisdata[i] = visdata[i];
		pweightdata[i] = weightdata[i];
		pbaseline[i] = baseline[i];
		pU[i] = U[i];
		pV[i] = V[i];
		pW[i] = W[i];
	}
	Data.visdata = pvisdata;
	Data.weightdata = pweightdata;
	Data.baseline = pbaseline;
	Data.u = pU;
	Data.v = pV;
	Data.w = pW;
}

void createSource(double sra, double sdec)
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
	sprintf(Source.name, "%s", "CSRHLOW");
	Source.id = 1;
	Source.qual = 0;
	sprintf(Source.calcode, "%s", "NUL");
	Source.freq_id = 1;
	Source.ra = sra;
	Source.dec = sdec;
}

void createArray()
{
	/*typedef struct _array_table {
	   int   n_ant;
	   double xyz_pos[3];    the X,Y,Z coord of the array in conventional radio astronomy units
	   char  name[16];
	   } array_data; */
	if (debug == 3)
		printf("createArray function is running\n");
	Array.n_ant = 40;
	sprintf(Array.name, "%s", "CSRH");
	Array.xyz_pos[0] = Array.xyz_pos[1] = Array.xyz_pos[2] = 0.;
	Locxyz2ITRF(LATITUDE, LONGITUDE, HEIGHT, Array.xyz_pos,
		    Array.xyz_pos + 1, Array.xyz_pos + 2);
			
	if (debug == 3)
		printf("createArray function was finished\n");
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
	   } ant_table; */

	FILE *fp1;
	int i, j, k;
	double ANT_POS[AntennasLow][3];
	double X, Y, Z;
	char antPos[4096];
	char *tmp;
	
	if (debug == 3)
		printf("createAnt function is running\n");
	
	if ( (tmp = getenv("MUSEROS_HOME")) == NULL ){
		printf("Cannot find \"MUSEROS_HOME\"");
	}
	strcpy(antPos, tmp);
	strcat(antPos, "/data/Ant_pos.txt");
	if (debug)
		printf("Ant_pos file is:\n%s\n", antPos);
	if (logFlag){
		fprintf(fpLog, "Ant_pos file is:\n%s\n", antPos);
	}
	if ((fp1 = fopen(antPos, "r")) == NULL) {
		printf("Open Ant_pos.txt file error\nfilename is:%s\n", antPos);
		if (logFlag){
			fprintf(fpLog, "Open Ant_pos.txt file error\nfilename is:%s\nRun Program error!\n", antPos);
		}
		destroy();
		exit(0);
	}
	if (debug == 2 || debug == 3)
		printf("the data of Ant_pos.txt:\n%10s %10s %10s\n","x", "y", "z");
	if (logFlag)
		fprintf(fpLog, "The data of Ant_pos.txt:\n%10s %10s %10s\n","x", "y", "z");
	for (i = 0; i < 40; i++) {
		fscanf(fp1, "%lf %lf %lf", &(ANT_POS[i][1]), &(ANT_POS[i][0]), &(ANT_POS[i][2]));
		if (debug == 2 || debug == 3)
			printf("%10.3f %10.3f %10.3f\n",ANT_POS[i][0],ANT_POS[i][1],ANT_POS[i][2]);
		if (logFlag)
			fprintf(fpLog, "%10.3f %10.3f %10.3f\n",ANT_POS[i][0],ANT_POS[i][1],ANT_POS[i][2]);
	}
	fclose(fp1);
	/* Init data */
	if (debug == 2 || debug == 3){
		printf("Init data is:\n");
		printf("Name    x_pos       y_pos       z_pos     pol_typeA pol_typeB\n");
	}
	if (logFlag)
			fprintf(fpLog, "\nInit data is:\nName    x_pos       y_pos       z_pos     pol_typeA pol_typeB\n");
	for (i = 0; i < 40; i++) {
		/* Set antenna name */
		if (i <= 13)
			sprintf(Ant[i].name, "I%c%d", 'A', i);
		else if (i <= 26)
			sprintf(Ant[i].name, "I%c%d", 'B', i - 13);
		else
			sprintf(Ant[i].name, "I%c%d", 'C', i - 26);

		if (debug == 2 || debug == 3)
			printf("%-4s ", Ant[i].name);
		if (logFlag)
			fprintf(fpLog, "%-4s ", Ant[i].name);
		/* Calculate ECEF XYZ */
		Ant[i].xyz_pos[0] = ANT_POS[i][0];
		Ant[i].xyz_pos[1] = ANT_POS[i][1];
		Ant[i].xyz_pos[2] = ANT_POS[i][2];
		Locxyz2ITRF(LATITUDE, LONGITUDE, HEIGHT, Ant[i].xyz_pos,
			    Ant[i].xyz_pos + 1, Ant[i].xyz_pos + 2);
		if (debug == 2 || debug == 3)
			printf("%10.3f %10.3f %10.3f ",Ant[i].xyz_pos[0],Ant[i].xyz_pos[1],Ant[i].xyz_pos[2]);
		if (logFlag)
			fprintf(fpLog, "%10.3f %10.3f %10.3f ",Ant[i].xyz_pos[0],Ant[i].xyz_pos[1],Ant[i].xyz_pos[2]);

		Ant[i].xyz_deriv[0] = Ant[i].xyz_deriv[1] =
		    Ant[i].xyz_deriv[2] = 0.;
		Ant[i].station_num = 1;
		Ant[i].mount_type = 2;
		Ant[i].axis_offset[0] = Ant[i].axis_offset[1] =
		    Ant[i].axis_offset[2] = 0.;
		Ant[i].pol_angleA = Ant[i].pol_angleB = 0;
		Ant[i].pol_calA = Ant[i].pol_calB = 0;
		sprintf(Ant[i].pol_typeA, "%c", 'R');
		sprintf(Ant[i].pol_typeB, "%c", 'L');
		if (debug == 2 || debug == 3)
			printf("%9s %9s\n\n", Ant[i].pol_typeA, Ant[i].pol_typeB);
		if (logFlag)
			fprintf(fpLog, "%9s %9s\n\n", Ant[i].pol_typeA, Ant[i].pol_typeB);
	}
	X = Y = Z = 0;
	Locxyz2ITRF(LATITUDE, LONGITUDE, HEIGHT, &X, &Y, &Z);
	for (i = 0; i < 40; i++) {
		Ant[i].xyz_pos[0] -= X;
		Ant[i].xyz_pos[1] -= Y;
		Ant[i].xyz_pos[2] -= Z;
	}
	for (i = 0; i < 39; i++) {
		for (j = i + 1; j < 40; j++) {

			for (k = 0; k < 3; k++) {
				BSL[i][j][k] =
				    Ant[j].xyz_pos[k] - Ant[i].xyz_pos[k];
			}

			DXYZ[i][j][0] =
			    -sin(PI * LATITUDE / 180.0) * BSL[i][j][0] +
			    cos(PI * LATITUDE / 180.0) * BSL[i][j][2];
			DXYZ[i][j][1] = BSL[i][j][1];
			DXYZ[i][j][2] =
			    cos(PI * LATITUDE / 180.0) * BSL[i][j][0] +
			    sin(PI * LATITUDE / 180.0) * BSL[i][j][2];
		}
	}
	if (debug == 3)
		printf("createAnt function was finished\n");
	if (logFlag)
		fprintf(fpLog, "createAnt function was successed\n");
	/* Locxyz2IRTF(double latitude, double longitude, double height, double *locx, double *locy, double *locz)  */
}

void helpMenu()
{
	printf("\nNAME\n\tcsrhsumuvfits - by index to creat fits file\n"
		   "\nDESCRIPTION\n\t./csrhsumuvfits --help\n\t\tdisplay help and exit\n"
		   "\n\t./csrhsumuvfits startdate enddate framelength\n\t\tIndex in current directory,create fits file in current directory\n"
		   "\n\t./csrhsumuvfits -d querypath startdate enddate framelength\n\t\tIndex in querypath directory, create fits file in current directory\n"
		   "\n\t./csrhsumuvfits startdate enddate framelength [option]\n\t\tIndex in current directory,create fits file in current directory\n"
		   "\n\t./csrhsumuvfits -d querypath startdate enddate framelength [option]\n\t\tIndex in querypath directory, create fits file in current directory\n"
		   "\toption:\n"
		   "\t-debug=level\n\t\tShow informations by level.The value of levels is 1,2,3\n\n"
		   "\t-log filepath\n\t\tCreate log's file in filepath\n");
}

/*�ֽ����ϳɲ�ѯ��Ŀ¼dir
 *
 *����˵����
 *dir[]���ϳɲ�ѯ��Ŀ¼��
 *argc������ĸ�������ϳɲ�ѯĿ¼�ķ�ʽ��
 *argv���������ֹʱ�����Ϣ
 *
 *����ֵ��
 *1���ϳɲ�ѯ����ʧ�ܣ�
 *0���ϳɲ�ѯ�����ɹ���
 *
 */
void getDir(const int argvFlag, char **argv, int choose)
{
	if (debug == 3)
		printf("getDir function is running\n");
	switch (choose){
	case 1:
		strncpy(dir, argv[argvFlag], 8);
		break;
	case 2:
		strcpy(dir, argv[argvFlag -1]);
		strcat(dir, "/");
		strncat(dir, argv[argvFlag], 8);
		break;
	}
	if (debug == 3)
		printf("getDir function was finished\n");
}

/*�ֽ����ϳɲ�ѯ������condition
 *
 *����˵����
 *condition[]:�ϳɵĲ�ѯ������
 *argc������ĸ������ںϳɲ�ѯ����ʱ��ֹʱ���λ��
 *argv���������ֹʱ�䣻
 *
 */
void getCondition(int argvFlag, char **argv)
{
	int i;
	if (debug == 3)
		printf("getCondition function is running\n");
	for (i = 8; i < 14; i++) {
		condition[i - 2] = argv[argvFlag][i];
		condition[i + 15] = argv[argvFlag + 1][i];
	}
	
	if (debug == 3)
		printf("getCondition function was finished\n");
	
}

void usage(char **argv)
{
	printf("\nUsage example:\n"
		   "\t%s yyyymmddhhnnss yyyymmddhhnnss framelength\n"
		   "or"
		   "\n\t%s -d querypath yyyymmddhhnnss yyyymmddhhnnss framelength\n", argv[0], argv[0]);
	printf("\n\tMore help, Please input:\n\t\t%s --help\n", argv[0]);
}

int checkTime(const int argvFlag, char **argv)
{
	int i_min_sec[2], i, j;
	char c_min_sec[5] = "\0";
	
	if (debug == 3)
		printf("checkTime function is running\n");
	
	/*��鿪ʼʱ��λ���Ƿ���ȷ */
	if (strlen(argv[argvFlag]) != 14) {
		printf("\n%s argument's length error!\n", argv[argvFlag]);
		sprintf(tmp, "\n%s argument's length error!\n", argv[argvFlag]);
		strcat(logRecord, tmp);
		return -1;
	}
	
	/*����ֹʱ��λ���Ƿ���ȷ */
	if (strlen(argv[argvFlag + 1]) != 14) {
		printf("\n%s argument's length error!\n", argv[argvFlag+1]);
		sprintf(tmp, "\n%s argument's length error!\n", argv[argvFlag+1]);
		strcat(logRecord, tmp);
		return -1;
	}
	
	/*��鿪ʼʱ�����ֹʱ����ꡢ�¡��ա�ʱ�����Ƿ���ͬ����ͬ���������ʾ */
	if (strncmp(argv[argvFlag], argv[argvFlag+1], 10) != 0) {
		printf("\nTime is error!\n%s\n%s\n", argv[argvFlag], argv[argvFlag+1]);
		sprintf(tmp, "\nTime is error!\n%s\n%s\n", argv[argvFlag], argv[argvFlag+1]);
		strcat(logRecord, tmp);
		return -1;
	}
	
	/*���ʱ�����Ƿ�С��һ����*/
	for (i = 0; i < 2; i++) {
		for (j = 0; j < 4; j++) {
			c_min_sec[j] = argv[i + argvFlag][j + 10];
		}
		i_min_sec[i] = atoi(c_min_sec);
	}
	if ((i_min_sec[1] - i_min_sec[0]) > 100) {
		printf("Time is error:\n%s\n%s\n", argv[argvFlag],
		       argv[argvFlag + 1]);
		sprintf(tmp, "Time is error:\n%s\n%s\n", argv[argvFlag], argv[argvFlag + 1]);
		strcat(logRecord, tmp);
		return -1;
	}
	if (debug == 3)
		printf("checkTime function was finished\n");
	sprintf(tmp, "checkTime function was successed\n");
	strcat(logRecord, tmp);
	
	return 0;
}

/*�������Ƿ���Ҫ��
 *
 *����˵����
 *argc���������
 *argv���������ݡ�
 *
 *����ֵ��
 *1��������Ҫ�󲢸����ʾ��
 *0��������Ҫ��
 *
 */
int initialization(const int argc, char **argv)
{
	/*���������������ǣ���ʼʱ�䣬��ֹʱ�䣬�����ۼӵ�֡�ĸ��� */
	int i_min_sec[2], i, j;
	char c_min_sec[5] = "\0";
	char *tmpDebug;
	switch (argc)
	{
	case 1:
		usage(argv);
		return 1;
		break;
	case 2:
		if (strcmp(argv[1], "--help") == 0){
			helpMenu();
			return 1;
		}
		else{
			usage(argv);
			return 1;
		}
		break;
	case 3:
		if (checkTime(1, argv) == -1)
			return 1;
		getDir(1, argv, 1);
		getCondition(1, argv);
		frameLength = 1;
		break;
	case 4:
		if (strcmp(argv[3], "-log") == 0){
			if ((fpLog = fopen(logName, "a+")) == NULL){
				printf("Cannot open log file\n");
					return 1;
			}
			logFlag = 1;
		}
		else {
			if (checkTime(1, argv) == -1)
				return 1;
			getDir(1, argv, 1);
			getCondition(1, argv);
			frameLength = atoi(argv[3]);
		}
		break;
	case 5:
		if (strcmp(argv[4], "-delay") == 0)
			delayFlag = 0;
		else if (strncmp(argv[4], "-debug", 6) == 0){
			if (strlen(argv[4]) == 6)
				debug = 1;
			else{
				if ((tmpDebug = strchr(argv[4], '=') ) == NULL){
					printf("Set debug level error:\n%s\n%*s%c\n", argv[4], 6, "", '^');
					return 1;
				}
				tmpDebug++;
				if (((debug = atoi(tmpDebug) ) > 3) || *tmpDebug < '0' || *tmpDebug > '9'){
					printf("Set debug level error:\n%s\n%*s%c\n", argv[4], 7, "", '^');
					return 1;
				}
			}
		}
		else if(strcmp(argv[4], "-log") == 0){
			if ((fpLog = fopen(logName, "a+")) == NULL){
				printf("Cannot open log file\n");
				return 1;
			}
			logFlag = 1;
		}
		else{
			printf("\"%s\" arguments unknown\n", argv[4]);
			printf("\nMore help, Please input:\n\t%s --help\n", argv[0]);
			return 1;
		}
		if (checkTime(1, argv) == -1)
			return 1;
		getDir(1, argv, 1);
		getCondition(1, argv);
		frameLength = atoi(argv[3]);
		break;
	case 6:
		if (strcmp(argv[4], "-log") == 0){
			getDir(1, argv, 1);
			getCondition(1, argv);
			frameLength = atoi(argv[3]);
			strcpy(logName, argv[5]);
			strcat(logName, "/csrhsumuvfits.log");
			if ( (fpLog = fopen(logName, "a+")) == NULL){
				printf("Cannot open file %s\n", logName);
				return 1;
			}
			logFlag = 1;
			if (checkTime(1, argv) == -1)
				return 1;
			if (debug)
				printf("Log file is:%s\n", logName);
		}
		else{
			if (checkTime(3, argv) == -1)
				return 1;
			getDir(3, argv, 2);
			getCondition(3, argv);
			frameLength = atoi(argv[5]);
		}
		break;
	case 7:
		getDir(3, argv, 2);
		getCondition(3, argv);
		frameLength = atoi(argv[5]);
		if (strcmp(argv[6], "-delay") == 0)
			delayFlag = 0;
		else if((strncmp(argv[6], "-debug", 6) == 0)){
			if (strlen(argv[6]) == 6)
				debug = 1;
			else{
				if ((tmpDebug = strchr(argv[6], '=') ) == NULL){
					printf("Set debug level error:\n%s\n%*s%c\n", argv[6], 6, "", '^');
					return 1;
				}
				tmpDebug++;
				if (((debug = atoi(tmpDebug) ) > 3) || *tmpDebug < '0' || *tmpDebug > '9'){
					printf("Set debug level error:\n%s\n%*s%c\n", argv[6], 7, "", '^');
					return 1;
				}
			}
		}
		else if(strcmp(argv[6], "-log") == 0){
			if ((fpLog = fopen(logName, "a+")) == NULL){
				printf("Cannot open log file\n");
				return 1;
			}
			/*
			else if (argc == 8){
				strcpy(logName, argv[5]);
				strcat(logName, "/csrhsumuvfits.log");
				if ( (fpLog = fopen(logName, "a+")) == NULL){
					printf("Cannot open file %s\n", logName);
					return 1;
				}
				if (debug)
					printf("Log file is:%s\n", logName);
			}*/
			logFlag = 1;
		}
		else{
			printf("\"%s\" arguments unknown\n", argv[6]);
			printf("\nMore help, Please input:\n\t%s --help\n", argv[0]);
			return 1;
		}
		if (checkTime(3, argv) == -1)
			return 1;
		break;
	case 8:
		getDir(3, argv, 2);
		getCondition(3, argv);
		frameLength = atoi(argv[5]);
		if (strcmp(argv[6], "-delay") == 0){
			delayFlag = 0;
			if (strncmp(argv[7], "-debug", 6) == 0){
				if (strlen(argv[7]) == 6)
					debug = 1;
				else{
					if ((tmpDebug = strchr(argv[7], '=') ) == NULL){
						printf("Set debug level error:\n%s\n%*s%c\n", argv[6], 6, "", '^');
						return 1;
					}
					tmpDebug++;
					if (((debug = atoi(tmpDebug) ) > 3) || *tmpDebug < '0' || *tmpDebug > '9'){
						printf("Set debug level error:\n%s\n%*s%c\n", argv[6], 7, "", '^');
						return 1;
					}
				}
			}
			else if(strcmp(argv[7], "-log") == 0){
				if ((fpLog = fopen(logName, "a+")) == NULL){
					printf("Cannot open log file\n");
					return 1;
				}
				/*else if (argc == 8){
				strcpy(logName, argv[5]);
				strcat(logName, "/csrhsumuvfits.log");
				if ( (fpLog = fopen(logName, "a+")) == NULL){
					printf("Cannot open file %s\n", logName);
					return 1;
				}
				if (debug)
					printf("Log file is:%s\n", logName);
			}*/
				logFlag = 1;
			}
			else{
				printf("\"%s\" arguments unknown\n", argv[7]);
				printf("\nMore help, Please input:\n\t%s --help\n", argv[0]);
				return 1;
			}
		//else if((strncmp(argv[6], "-debug", 6) == 0)){
		}
		else{
			printf("\"%s\" arguments unknown\n", argv[6]);
			printf("\nMore help, Please input:\n\t%s --help\n", argv[0]);
			return 1;
		}
		if (checkTime(3, argv) == -1)
			return 1;
		break;
	case 9:
		getDir(3, argv, 2);
		getCondition(3, argv);
		frameLength = atoi(argv[5]);
		if (strcmp(argv[6], "-delay") == 0){
			delayFlag = 0;
			if (strcmp(argv[7], "-log") != 0){
				printf("\"%s\" arguments unknown\n", argv[7]);
				printf("\nMore help, Please input:\n\t%s --help\n", argv[0]);
				return 1;
			}
			strcpy(logName, argv[8]);
			strcat(logName, "/csrhsumuvfits.log");
			if ( (fpLog = fopen(logName, "a+")) == NULL){
				printf("Cannot open file %s\n", logName);
				return 1;
			}
			logFlag = 1;
		}
		else{
			printf("\"%s\" arguments unknown\n", argv[6]);
			printf("\nMore help, Please input:\n\t%s --help\n", argv[0]);
			return 1;
		}
		if (checkTime(3, argv) == -1)
			return 1;
		break;
	case 10:
		getDir(3, argv, 2);
		getCondition(3, argv);
		frameLength = atoi(argv[5]);
		if (strcmp(argv[6], "-delay") == 0){
			delayFlag = 0;
			if (strncmp(argv[7], "-debug", 6) != 0){
				printf("\"%s\" arguments unknown\n", argv[7]);
				printf("\nMore help, Please input:\n\t%s --help\n", argv[0]);
				return 1;
			}
			if (strlen(argv[7]) == 6)
				debug = 1;
			else{
				if ((tmpDebug = strchr(argv[7], '=') ) == NULL){
					printf("Set debug level error:\n%s\n%*s%c\n", argv[6], 6, "", '^');
					return 1;
				}
				tmpDebug++;
				if (((debug = atoi(tmpDebug) ) > 3) || *tmpDebug < '0' || *tmpDebug > '9'){
					printf("Set debug level error:\n%s\n%*s%c\n", argv[6], 7, "", '^');
					return 1;
				}
			}
			if (strcmp(argv[8], "-log") != 0){
				printf("\"%s\" arguments unknown\n", argv[8]);
				printf("\nMore help, Please input:\n\t%s --help\n", argv[0]);
				return 1;
			}
			strcpy(logName, argv[9]);
			strcat(logName, "/csrhsumuvfits.log");
			if ( (fpLog = fopen(logName, "a+")) == NULL){
				printf("Cannot open file %s\n", logName);
				return 1;
			}
			logFlag = 1;
		}
		else{
			printf("\"%s\" arguments unknown\n", argv[6]);
			printf("\nMore help, Please input:\n\t%s --help\n", argv[0]);
			return 1;
		}
		if (checkTime(3, argv) == -1)
			return 1;
		break;
	default:
		usage(argv);
		return 1;
	}
	if (debug == 3)
		printf("Initialization function is running\n");
	if (debug){
		if (logFlag)
			printf("Log file is:%s\n", logName);
		printf("Query path is:%s\n", dir);
		printf("Condition is:%s\n", condition);
		printf("FrameLength is :%d\n", frameLength);
	}
	if (debug == 3)
		printf("Initialization function was finished\n");
	return 0;
}

/*�����������
 *
 *����
 *rowcount����ѯ���Ľ������
 *frameLength������������ֵ��
 *
 *����ֵ��
 *0��������Ҫ��
 *1��������Ҫ��
 *
 *�ж�������
 *���������Ǹ���
 *���������Ӧ�ÿ��Ա���ѯ�������������֤�ۼ�ʱ�����?
 */
int checkFrameLength(int rowcount)
{
	if (debug == 3)
		printf("checkFrameLength function is running\n");
	if (frameLength <= 0 || rowcount % frameLength != 0) {
		printf
		    ("Length is error:\nThe result of query is:%d\nThe length is:%d\n",
		     rowcount, frameLength);
		if (logFlag){
			fprintf(fpLog, "Length is error:\nThe result of query is:%d\nThe length is:%d\nRun program error\n", rowcount, frameLength);
		}
		return 0;
	}
	if (debug == 3)
		printf("checkFrameLength function was finished\n\n");
	return 1;
}

/*��ʱ�Ӳ�����д���
 *
 *������
 *
 *����ֵ����
 */
void delayProcess()
{
	int delayNs[44] = {-56, 0, 48, 921, 13, 59, -3, 460, 49, 69, -675,
				-157, 363, -65, 30, 42, 51, 121, -2, 73, 35, 26,
				74, 35, -3, 47, -71, 75,343, 56, 32,313, 678,
				12, -30, 48, -18, 20, 10, -1666,0,  0,  0,  0}; 
              
	int delayNsAdd[44] = {0, 0, -30, -20, 10, 9, -15, -1, -48, -33, 0,
				186, 0, 0, 0, -26, 0, 0, 0, 0, -24, -1,
				-57, 0, 0, 3, 66, -12, 0, -20, -1, 0, -22,
				0, 7, 10, 2, 1, 0, 0, 0,  0,  0,  0};
	float delay[44];
	float Frf,Fif,tg,tg0,phai,phai1,phai2;
	int i;
	int antenna1,antenna2,channel;
	double module;
	
	if (debug == 3)
		printf("delayProcess function is running\n");
	
	for (i=0; i<AntennasLow; i++){
		delayNs[i] += delayNsAdd[i];
	}
	for (i=0; i<AntennasLow; i++){
		delay[i] = delayCSRHData[i]-(float)delayNs[i];
	}
	
	for (antenna1=0; antenna1<AntennasLow-1; antenna1++){
		for (antenna2=antenna1+1; antenna2<AntennasLow; antenna2++){
			for (channel=0; channel<SubChannelsLow; channel++){
				module = sqrt(pow(lowCSRHData[antenna1][antenna2][channel].real, 2) + pow(lowCSRHData[antenna1][antenna2][channel].imaginary, 2));
				phai1 = (float)atan2(lowCSRHData[antenna1][antenna2][channel].real , lowCSRHData[antenna1][antenna2][channel].imaginary);
				Frf = (1600+channel*25+2.5)/1000.0;
				Fif = (channel*25+2.5+50.0)/1000.0;
				tg  =  delay[antenna2] - delay[antenna1];
				tg0  =  (float)(floor((double)delay[antenna2]) - floor((double)delay[antenna1]));
				phai2 = PI*2*(Frf*tg-Fif*tg0);
				phai = phai1 - phai2;
				
				lowCSRHData[antenna1][antenna2][channel].real = module * cos(phai);
				lowCSRHData[antenna1][antenna2][channel].imaginary = module * sin(phai);
				
			}
		}
	}
	
	if (debug == 3)
		printf("delayProcess function was finished\n");
}

/*��ݲ�ѯ������ݽ����ۼӣ���ƽ���ϳ�fits�ļ�
 *
 *����˵����
 *frameLength���ۼӵĴ�֡�ĳ��ȣ�
 *ret����ѯ��������
 *rs����ѯ�Ľ��
 *
 */
void handleData(int ret, ResultSet rs)
{
	averageValue tmpData[8];	//������ƽ�����ʱ��ݣ�ÿһ����Ԫ����ÿһ��С֡�����
	double obstime;
	char filename[4096] = "\0";
	char fitsfile[100];
	char *tmp;
	int i, j, k, l, count;
	short int openFileFlag = 1;
	double jd_utc, jd_tt, jd_ut1, delta_t, hour;
	double ra, dec, dis, rat, dect, dist, gast, last;
	int countFits=0;

	/*frameCount:����ÿ�κϳɽ��е�С֡�ţ�ÿ���һ�ξ���0��
	 *rowCount:���浱ǰ�ϳɵ��кţ�
	 *frameLengthCount:���浱ǰ�����˶��ٴε��ۼӣ�
	 */
	int frameCount = 0, rowCount = 0, frameLengthCount = 0;
	/*�ϳ���Ҫ�򿪵��ļ��� */
	if (debug == 3)
		printf("handleData function is running\n");
	
	strcpy(filename, rs.filename[0]);
	for (i = 0; filename[i + 1] != '\"'; i++) {
		filename[i] = filename[i + 1];
	}
	filename[i] = '\0';
	if (debug)
		printf("filename and path:\n%s\n", filename);
	if (logFlag)
		fprintf(fpLog, "filename and path:\n\t%s\n\nCreate fits file list:\n", filename);

	while (rowCount < rs.rowcount)	//�ϳ�δ��ɽ�����ݺϳ�
	{
		while (frameLengthCount < frameLength)	//���ﵽ�ۼƵ�֡��ϳ�һ����ݣ���д��fits�ļ�
		{
			if (openFileFlag) {
				if (openCSRHFile(filename) == 0) {
					printf("Cannot open file %s\n", filename);
					if (logFlag){
						fprintf(fpLog, "Cannot open file %s\nRun program error\n", filename);
					}
					destroy();
					exit(1);
				}
				if (debug){
					if ( (tmp = strrchr(filename, '/')) == NULL)
						tmp = filename;
					else
						tmp++;
					printf("Open Raw Data File:%s successfully\n", tmp);
				}
				openFileFlag = 0;
			}
			if (!setOffset(rs.offset[rowCount]))	//�趨�ļ���ָ���ƫ��
				return;
			readOneFrame();	//��ȡ�ļ��е����
			if (delayFlag)
				delayProcess(); //����λ���в���
			if (frameCount < 8)	//��1~8֡����ݽ��г�ʼ��������ʱ��������
			{
				if (rs.pc[rowCount] <= 4)
					tmpData[frameCount].csrhPolarization =
					    0;
				else
					tmpData[frameCount].csrhPolarization =
					    1;
				tmpData[frameCount].currentFrameTime =
				    currentFrameTime;
					if (debug == 3)
						printf("currentFrameTime.nanoSecond is:%d\n", tmpData[frameCount].currentFrameTime.nanoSecond);
				tmpData[frameCount].csrhFrequency =
				    csrhFrequency;
				count = 0;
				for (i = 0; i < 16; i++)
					for (j = 0; j < RealAntennasLow - 1;
					     j++)
						for (k = j + 1;
						     k < RealAntennasLow; k++) {
							tmpData
							    [frameCount].visdata
							    [0][count * 2] =
							    lowCSRHData[j][k]
							    [i].real;
							tmpData
							    [frameCount].visdata
							    [0][count * 2 + 1] =
							    lowCSRHData[j][k]
							    [i].imaginary;
							weightdata[0][count] =
							    1.;
							count++;
						}
			} else	//���һ����֡����ݺ���������������ԭ���Ļ��Ͻ����ۼ�
			{	//���ﵽ�ϳɵ�Ҫ��ʱ����ʱ������ۼӣ�Ϊ��ƽ��ֵ��׼��
				if (frameLengthCount == frameLength - 1) {
					tmpData[frameCount %
						8].currentFrameTime.Year +=
					    currentFrameTime.Year;
					tmpData[frameCount %
						8].currentFrameTime.Month +=
					    currentFrameTime.Month;
					tmpData[frameCount %
						8].currentFrameTime.Day +=
					    currentFrameTime.Day;
					tmpData[frameCount %
						8].currentFrameTime.Hour +=
					    currentFrameTime.Hour;
					tmpData[frameCount %
						8].currentFrameTime.Minute +=
					    currentFrameTime.Minute;
					tmpData[frameCount %
						8].currentFrameTime.Second +=
					    currentFrameTime.Second;
					tmpData[frameCount %
						8].
					    currentFrameTime.miliSecond +=
					    currentFrameTime.miliSecond;
					tmpData[frameCount %
						8].
					    currentFrameTime.macroSecond +=
					    currentFrameTime.macroSecond;
					tmpData[frameCount %
						8].
					    currentFrameTime.nanoSecond +=
					    currentFrameTime.nanoSecond;
				}

				count = 0;
				for (i = 0; i < 16; i++)
					for (j = 0; j < RealAntennasLow - 1;
					     j++)
						for (k = j + 1;
						     k < RealAntennasLow; k++) {
							tmpData[frameCount %
								8].visdata[0]
							    [count * 2] +=
							    lowCSRHData[j][k]
							    [i].real;
							tmpData[frameCount %
								8].visdata[0]
							    [count * 2 + 1] +=
							    lowCSRHData[j][k]
							    [i].imaginary;
							count++;
						}
			}
			frameCount++;
			rowCount++;
			if (frameCount % 8 == 0)	//��ȡ��һ�δ�֡���֡�Ž���������ֱ���ϳ������ɡ�
				frameLengthCount++;
			if ((rowCount + 1) < rs.rowcount) {
				if (strcmp
				    (rs.filename[rowCount],
				     rs.filename[rowCount + 1]) != 0) {
					closeCSRHFile();
					strcpy(filename,
					       rs.filename[rowCount + 1]);
					for (i = 0; filename[i + 1] != '\"';
					     i++)
						filename[i] = filename[i + 1];
					filename[i] = '\0';
					openFileFlag = 1;
					if (debug)
						printf("filename:%s\n", filename);
				}
			}
		}

		for (l = 0; l < 8; l++)	//��8��С֡������ƽ��ͬʱ�ϳ�fits�ļ���
		{
			if (frameLength > 1)	//���ۼӵĴ�֡����1ʱ�Ŷ���ݽ�����ƽ�����������
			{
				/*��ʱ�������ƽ�� */
				tmpData[l].currentFrameTime.Year /= 2;
				tmpData[l].currentFrameTime.Month /= 2;
				tmpData[l].currentFrameTime.Day /= 2;
				tmpData[l].currentFrameTime.Hour /= 2;
				tmpData[l].currentFrameTime.Minute /= 2;
				tmpData[l].currentFrameTime.Second /= 2;
				tmpData[l].currentFrameTime.miliSecond /= 2;
				tmpData[l].currentFrameTime.macroSecond /= 2;
				tmpData[l].currentFrameTime.nanoSecond /= 2;

				/*����ݵ�ʵ�����鲿������ƽ�� */
				count = 0;
				for (i = 0; i < 16; i++)
					for (j = 0; j < RealAntennasLow - 1;
					     j++)
						for (k = j + 1;
						     k < RealAntennasLow; k++) {
							tmpData[l].visdata[0]
							    [count *
							     2] /= (float)
							    frameLength;
							tmpData[l].visdata[0]
							    [count * 2 +
							     1] /= (float)
							    frameLength;
							/*if((l == 3) && (count == 780))
						  {
						  	printf("real is:%f\n",tmpData[l].visdata[0][count*2]);
						  	printf("imaginary is:%f\n",tmpData[l].visdata[0][count*2+1]);
						  }
						  if((l == 3) && (count == 0))
						  {
						  	printf("real is:%f\n",tmpData[l].visdata[0][count*2]);
						  	printf("imaginary is:%f\n",tmpData[l].visdata[0][count*2+1]);
						  }*/
							count++;
						}
			}
			createData(1, tmpData[l].csrhPolarization, 16, 1,
				   tmpData[l].csrhFrequency + 200000000.,
				   25000000);
			if (debug)
				printf("\nInit UVFits data [%d] successfully\n", l + 1);

			hour =
			    tmpData[l].currentFrameTime.Hour - 8 +
			    (double)tmpData[l].currentFrameTime.Minute / 60. +
			    (tmpData[l].currentFrameTime.Second +
			     (double)(tmpData[l].currentFrameTime.miliSecond) /
			     1000. +
			     (double)(tmpData[l].currentFrameTime.macroSecond) /
			     1000000. +
			     (double)(tmpData[l].currentFrameTime.nanoSecond) /
			     1000000000.) / 3600.;
			jd_utc =
			    julian_date(tmpData[l].currentFrameTime.Year,
					tmpData[l].currentFrameTime.Month,
					tmpData[l].currentFrameTime.Day, hour);
			jd_tt = jd_utc + ((double)leap_secs + 32.184) / 86400.0;
			jd_ut1 = jd_utc + ut1_utc / 86400.0;
			delta_t = 32.184 + leap_secs - ut1_utc;
			ephemPosition(jd_utc, &ra, &dec, &dis, &rat, &dect,
				      &dist, &gast, &last);
			if (debug == 2 || debug == 3)
				printf("Compute target position successfully %lf %lf\n",
			       rat, dect);
			sprintf(fitsfile,
				"%4d%02d%02d-%02d%02d%02d_%03d%03d%03d.fits",
				tmpData[l].currentFrameTime.Year,
				tmpData[l].currentFrameTime.Month,
				tmpData[l].currentFrameTime.Day,
				tmpData[l].currentFrameTime.Hour,
				tmpData[l].currentFrameTime.Minute,
				tmpData[l].currentFrameTime.Second,
				tmpData[l].currentFrameTime.miliSecond,
				tmpData[l].currentFrameTime.macroSecond,
				tmpData[l].currentFrameTime.nanoSecond);
			if (debug == 2 || debug == 3)
				printf("Filename: %s\n", fitsfile);
			if (logFlag)
				fprintf(fpLog, "%s\n", fitsfile);
			date = jd_utc;
			n_baselines = 780;
			if (debug == 2 || debug == 3)
				printf("Hour and DEC: %lf %lf\n", last - rat, dect);
			computeUVW((last - rat) * 15., dect);

			// Only need to write the data wit size of RealAntennasLow 
			count = 0;
			for (i = 0; i < RealAntennasLow - 1; i++)
				for (j = i + 1; j < RealAntennasLow; j++)
					baseline[0][count++] =
					    (i + 1) * 256 + j + 1;

			count = 0;
			for (i = 0; i < 16; i++)
				for (j = 0; j < RealAntennasLow - 1; j++)
					for (k = j + 1; k < RealAntennasLow;
					     k++) {
						visdata[0][count * 2] =
						    tmpData[l].visdata[0][count
									  * 2];
						visdata[0][count * 2 + 1] =
						    tmpData[l].visdata[0][count
									  * 2 +
									  1];
						weightdata[0][count] = 1.;
						count++;
					}
			countFits++;
			writeUVFITS(fitsfile, &Data);
			if (debug)
				printf("Write file ok!\n");
		}
		frameCount = frameLengthCount = 0;
		if (debug)
			printf("rowCount:%d\n", rowCount);
	}
	closeCSRHFile();
	if (debug == 3)
		printf("handle function was finished\n");
	
	if (logFlag)
		fprintf(fpLog, "The count is: %d\nWrite fits file OK!\n", countFits);
}

void main(int argc, char **argv)
{
	int ret = 0, i, startTime, endTime,countTime[2];
	ResultSet rs;
	
	runTime = time(NULL);
	localTime = localtime(&runTime);
	//strcpy(logRecord, "Time is:");
	sprintf(tmp, "program name:\n\t%s\nDate: %d/%02d/%02d\nTime: %02d:%02d:%02d\n", argv[0], (1900+localTime->tm_year), (localTime->tm_mon+1), localTime->tm_mday, localTime->tm_hour, localTime->tm_min, localTime->tm_sec);
	strcpy(logRecord, tmp);
	for (i=0; i<80; i++)
		strcat(logRecord, "_");
	strcat(logRecord, "\n");
	
	printf("The program is running...\n");
	
	if (initialization(argc, argv)){
		if (logFlag){
			fputc('\n', fpLog);
			for (i=0; i<80; i++)
				fputc('-', fpLog);
			fputc('\n', fpLog);
			for (i=0; i<31; i++)
				fputc(' ', fpLog);
			fputs("csrhsumuvfits  Log\n", fpLog);
			for (i=0; i<80; i++)
				fputc('-', fpLog);
			fputc('\n', fpLog);
			fputs(logRecord, fpLog);
			fprintf(fpLog, "Run program error!\n");
		}
		destroy();
		exit(0);
	}
	if (logFlag){
		fputc('\n', fpLog);
		for (i=0; i<80; i++)
			fputc('-', fpLog);
		fputc('\n', fpLog);
		for (i=0; i<31; i++)
			fputc(' ', fpLog);
		fputs("csrhsumuvfits  Log\n", fpLog);
		for (i=0; i<80; i++)
			fputc('-', fpLog);
		fputc('\n', fpLog);
		fputs(logRecord, fpLog);
		fprintf(fpLog, "Query path is:%s\nCondition is:%s\nFrameLength is :%d\nInitialization function was successed\n", dir, condition, frameLength);
	}
	/*  Init Array and Antenna Table */
	createArray();
	if (debug)
		printf("Create Array successfully\n");
	if (logFlag){
		fputs("Create Array successfully\n", fpLog);
		for (i=0; i<80; i++)
			fputc('_', fpLog);
		fputc('\n', fpLog);
	}
	createAnt();
	if (debug)
		printf("Create Antenna successfully\n");
	if (logFlag){
		fputs("Create Antenna successfully\n", fpLog);
		for (i=0; i<80; i++)
			fputc('_', fpLog);
		fputc('\n', fpLog);
	}

	/*����fastbit���в�ѯ */
	startTime = clock();
	ret = selectrows(dir, condition, &rs);
	endTime = clock();
	if (debug)
		printf("rowcount is:%d\n\n", ret);
	countTime[0] = (endTime - startTime)/1000;

	if (ret == 0 || ret == -1) {
		printf("find file failure\n");
		destroy();
		exit(0);
	}
	/*check input data */
	if (!checkFrameLength(ret)) {
		printf("You should input a integer\n");
		destroy();
		exit(0);
	}

	if (ephemOpen() != 1){
		if (logFlag)
			fprintf(fpLog, "The program error\n");
		destroy();
		exit(0);
	}
	if (debug)
		printf("Open Ephem File successfully\n");
	if (logFlag)
		fprintf(fpLog, "Open Ephem File successfully\n");

	startTime = clock();
	handleData(ret, rs);
	endTime = clock();
	countTime[1] = (endTime - startTime)/1000;

	if (debug == 2){
		printf("Query time is:%d s\nDispos time is:%d ms\n", countTime[0], countTime[1]);
	}
	if (logFlag){
		fprintf(fpLog, "Run program successfully.\n");
	}
	destroy();
	ephemClose();
	printf("Program was finished.\n");
}
