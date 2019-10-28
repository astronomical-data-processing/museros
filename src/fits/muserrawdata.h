#ifndef CSRHRAWDATA_H
#define CSRHRAWDATA_H

#define AntennasLow  44
#define RealAntennasLow  40
#define ChannelsLow  64
#define RealChannelsLow  64
#define SubChannelsLow  16
#define RealSubChannelsLow  12
#define PolarizationLow  2

typedef struct {
    float real;
    float imaginary;
} CSRHComplex;

// According to the manual, the system time can be divided into 9 parts
typedef struct {
    unsigned int Year;
    unsigned int Month;
    unsigned int Day;
    unsigned int Hour;
    unsigned int Minute;
    unsigned int Second;
    unsigned int miliSecond;
    unsigned int macroSecond;
    unsigned int nanoSecond;
} CSRHSystemTime;

typedef struct {
    long long systemtime;
    unsigned int frequencySwitch;   // Frequency Switch
    unsigned int bandWidth;  // Bandwidth of each channel
    unsigned int quantizationLevel;
    unsigned int delaySwitch;
    unsigned int stripSwitch;
    unsigned int subBand;  // **IMPORTANT** Parameter, Low 16bits: frequency hopping
} CSRHLowFrameHeader;

int csrhPolarization;  // Polarization mode
int csrhChannelGroup;  // Frequency hopping flag, values from 0 to 48 step 16

unsigned long csrhFrequency;

const static unsigned int frequency=400000000;

CSRHLowFrameHeader currentFrameHeader;
CSRHSystemTime currentFrameTime;

CSRHComplex lowCSRHData[AntennasLow][AntennasLow][SubChannelsLow];

float correlationValue[SubChannelsLow][AntennasLow][AntennasLow];
int selfCorrelationValue[AntennasLow][SubChannelsLow];

CSRHSystemTime convertTime(long long stime);

int lowCSRHDataFlag[AntennasLow][AntennasLow][SubChannelsLow];

float delayCSRHData[AntennasLow];

int openCSRHFile(char *file);
void closeCSRHFile();

int searchFrameHeader();
int readOneFrame();
int readOneData();

CSRHSystemTime getFrameTime();
int getCorrelationValue(int channel,int antenna1,int antenna2);
CSRHComplex getCrossCorrelationLow(int Polarization, int Antenna1,
                                   int Antenna2, int Channel);

void ConvertCrossCorrelationData(unsigned char *buff, CSRHComplex *c2,CSRHComplex *c1);
void AutoCorrelationData(unsigned char *buff,long long *r1,long long *r2);

// Reset the information of FLag for LowData
void ResetLowDataFlag();

int setOffset(unsigned long offset);
void showoffset();

#endif // CSRHRAWDATA_H
