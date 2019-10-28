#include "muserrawdata.h"
#include <stdio.h>
#include <math.h>

FILE *fpCSRH;
double currentCSRHTime;
int delayNN[44]={-56,0,18,901,23,68,-18,459,1,36,-675,29,363,-65,30,16,51,121,-2,73,11,
	25,17,35,-3,50,-5,63,343,36,31,313,656,12,-23,58,-16,21,10,-1666,0,0,0,0};

void ResetlowCSRHDataFlag()
{
    int i, j, k, m;
    
    for (j = 0; j < AntennasLow - 1; j++)
        for (k = 0; k < AntennasLow; k++)
            for (m = 0; m < SubChannelsLow; m++) {
                lowCSRHDataFlag[j][k][m] =0;
            }
}

int openCSRHFile(char *filename) {
    if ((fpCSRH = fopen(filename, "rb"))==0)
        return 0;
    // Reset FLag data while opening the file
    ResetlowCSRHDataFlag();
    return 1;
}

void closeCSRHFile() {
    fclose(fpCSRH);
}

// ResetlowCSRHDataFlag - Initialize the Flag information when opening the file
// Flag - 1: the data is valid , 0 : invalid


// Convert a long long  value to a self-defined System Date/Time Format
CSRHSystemTime convertTime(long long stime) {
    CSRHSystemTime tmp;
    // Read nanosecond, 0-5 bits
    tmp.nanoSecond = (stime & 0x3f);
    if (tmp.nanoSecond>=50)
        tmp.nanoSecond=0;
    tmp.nanoSecond *= 20;
    stime >>= 6;
    // Read macrosecond, 6-15
    tmp.macroSecond = (stime & 0x3ff);
    stime >>= 10;
    // Read milisecond 16-25
    tmp.miliSecond = (stime & 0x3ff);
    stime >>= 10;
    // Read second, 26-31
    tmp.Second = (stime & 0x3f);
    stime >>= 6;
    // Read Minute, 32-37
    tmp.Minute = (stime & 0x3f);
    stime >>= 6;
    // Read Hour, 38-42
    tmp.Hour = (stime & 0x1f);
    stime >>= 5;
    // Read Day
    tmp.Day = (stime & 0x1f);
    stime >>= 5;
    // Read Month, 48-51
    tmp.Month = (stime & 0x0f);
    stime >>= 4;
    // Read Year
    tmp.Year = (stime & 0xfff) + 2000;
    return tmp;
}

int changesigned(a)
{
    if (a >= 128l * 256l * 256l)
    {
        a = a - 256l * 256l * 256L;
    }
    return a;
}

void ConvertCrossCorrelationData(unsigned char *buff, CSRHComplex *c1,
                                 CSRHComplex *c2) {
    int r;
    // read imaginary part of second channel
    r = buff[8];
    r <<= 8;
    r |= buff[4];
    r <<= 8;
    r |= buff[0];
    r =  changesigned(r);
    (*c2).imaginary = r;
    // read real part of second channel
    r = buff[9];
    r <<= 8;
    r |= buff[5];
    r <<= 8;
    r |= buff[1];
    r =  changesigned(r);
    (*c2).real = r;
    // read imaginary part of second channel
    r = buff[10];
    r <<= 8;
    r |= buff[6];
    r <<= 8;
    r |= buff[2];
    r =  changesigned(r);
    (*c1).imaginary = r;
    // read real part of second channel
    r = buff[11];
    r <<= 8;
    r |= buff[7];
    r <<= 8;
    r |= buff[3];
    r =  changesigned(r);
    (*c1).real = r;
}

void SelfCorrelationData(unsigned char *buff,int  *r1, int *r2)
{
    *r1=buff[3];
    *r1<<=8;
    *r1|=buff[2];
    *r1<<=8;
    *r1|=buff[1];
    *r1<<=8;
    *r1|=buff[0];
    
    *r2=buff[7];
    *r2<<=8;
    *r2|=buff[6];
    *r2<<=8;
    *r2|=buff[5];
    *r2<<=8;
    *r2|=buff[4];
    
}

void countDelay(unsigned char *buff, float *delay, int number) {
		int r1,r2;
		r1 = buff[number*2+1];
		r1 <<= 8;
		r1 |= buff[number*2];
		r1 = changesigned(r1);
		
		r2 = buff[number*2+1+8];
		r2 <<= 8;
		r2 |= buff[number*2+8];
		r2 = changesigned(r2);
		
		*delay=(((float)r2+(float)r1*0.0001));
		//modified by daiwei 2014-05-16,remove *1e-09
	//	*delay=(((float)r2+(float)r1*0.0001)*1e-09);
	  //*delay=(double)buff[number+4]+(double)buff[number]*0.1/1000.;
	  //printf("Integer is:%d\tDecimal is:%d\n", buff[number+4], buff[number]);
	  //printf("Integer is:%x\tDecimal is:%x\n", buff[number+4], buff[number]);
	  
}

int readOneFrame() {
    unsigned char buff[13];
    int antenna, antenna1,antenna2,antenna3, channel;  
    unsigned char buff2[8];
    int r1,r2;
    int i;
    unsigned char buff3[16];
    int delayInteger,delayDecimal;
    char *base;
	
    /* 28 bytes should be checked*/
    /*if (!searchFrameHeader()) {
	return 0;
}*/
    
    // readout system time ϵͳʱ��Ϊ64bit
    base = ((char *) &(currentFrameHeader.systemtime));  
    if ((fread(base,8,1,fpCSRH))==0)   
        return 0;
    currentFrameTime = convertTime(currentFrameHeader.systemtime);
    // read frequency switch �ź�������תƵ�ʣ�32bit
    if ((fread((char *) &currentFrameHeader.frequencySwitch, 4,1, fpCSRH))==0)
        return 0;
    // read spare 64 x 16bits ����õ�64bit
    fseek(fpCSRH, 128, 1);
    // read bandWidth;   ���32bit
    if ((fread((char *) &currentFrameHeader.bandWidth, 4,1, fpCSRH))==0)
        return 0;
    // read quantizationLevel ������ƽȨֵ����ֵ32 Ȩֵ ��16λ ��ֵ ��16λ
    if ((fread((char *) &currentFrameHeader.quantizationLevel, 4,1, fpCSRH))==0)
        return 0;
    // read delaySwitch  �ӳٵ���� 32bit
    if ((fread((char *) &currentFrameHeader.delaySwitch, 4, 1, fpCSRH))==0)
        return 0;
    // read strip switch  ������ת����	32bits
    if ((fread((char *) &currentFrameHeader.stripSwitch, 4, 1, fpCSRH)) ==0)
        return 0;
    // read subBand		�Ӵ�����ʽ 32bit
    if ((fread((char *) &currentFrameHeader.subBand, 4, 1, fpCSRH))==0)
        return 0;
    
    // Determine the polarization
    if (currentFrameHeader.subBand && 0xffff == 0x3333)
		csrhPolarization = 0;
    else
        csrhPolarization = 1;
    
    // Determine the subband
    int subBand = (currentFrameHeader.subBand >> 16);  //�ж���ƵƵ�ʣ���16bits��
    switch (subBand) {
	case 0x3333:
		csrhChannelGroup = 0;
		csrhFrequency = 400000000;
		break;
	case 0x7777:
		csrhChannelGroup = 16;
		csrhFrequency = 800000000;
		break;
	case 0xbbbb:
		csrhChannelGroup = 32;
		csrhFrequency = 1200000000;
		break;
	case 0xcccc:
		csrhChannelGroup = 48;
		csrhFrequency = 1600000000;
		break;
	default:
		fseek(fpCSRH, 99264 - 192, 1);  //���ѭ������ֵ
		unsigned short subBandTmp;
		if ((fread(&subBandTmp,2,1,fpCSRH))==0)
			return 0;
		switch(subBandTmp) {
		case 0x0000:
			csrhChannelGroup = 0;
			csrhFrequency = 400000000;
			break;
		case 0x5555:
			csrhChannelGroup = 16;
			csrhFrequency = 800000000;
			break;
		case 0xaaaa:
			csrhChannelGroup = 32;
			csrhFrequency = 1200000000;
			break;
		case 0xffff:
			csrhChannelGroup = 48;
			csrhFrequency = 1600000000;
			break;
		}
		fseek(fpCSRH,-(99264 - 192 + 2), 1);  //��������ѭ������ֵ ѭ��ֵ+��ȡ������ֵ
		break;
    }
	
//    printf("Channelgroup %d Frequency %ld \n",csrhChannelGroup,csrhFrequency);
    // read Spare  ��ȡ����
    fseek(fpCSRH, 2752, 1);
	
    // read cross correlation data
    // Notice: Data with the size of AntennasLow (44) should be read
    antenna3=0;
    for (channel = 0; channel <= SubChannelsLow - 1; channel += 2) {
        for (antenna1 = 0; antenna1 < AntennasLow - 1; antenna1++) {
            for (antenna2 = antenna1 + 1; antenna2 < AntennasLow; antenna2++) {
                fread(buff, 12,1,fpCSRH);
                CSRHComplex c1, c2;
                ConvertCrossCorrelationData(buff, &c1, &c2);
                
                lowCSRHData[antenna1][antenna2][channel+1].real = c2.real;
                lowCSRHData[antenna1][antenna2][channel+1].imaginary = c2.imaginary;
                lowCSRHData[antenna1][antenna2][channel].real = c1.real;
                lowCSRHData[antenna1][antenna2][channel].imaginary = c1.imaginary;
                /*    printf("VIS: %f %f\n",lowCSRHData[antenna1][antenna2][channel].real,lowCSRHData[antenna1][antenna2][channel].imaginary);
				printf("VIS: %f %f\n",lowCSRHData[antenna1][antenna2][channel+1].real,lowCSRHData[antenna1][antenna2][channel+1].imaginary);*/
            }
        }
        // Read spare data between each cross correlation data, I don't know how to use the parameters
        // So, I have to directly skip the file pointer
        // TODO: maybe we should read out the parameters and to *DO* some processings
        /*inFile.seekg(744, std::ios_base::cur);
			unsigned short FHCode;
			inFile.read((char *) &FHCode, 2);
			inFile.seekg(30, std::ios_base::cur);*/
        
        fseek(fpCSRH,40, 1);
        for(antenna=0;antenna<AntennasLow;antenna++){
            fread(buff2,8, 1, fpCSRH);
            SelfCorrelationData(buff2,&r1,&r2);
            
            selfCorrelationValue[antenna][channel]=r1;
            selfCorrelationValue[antenna][channel+1]=r2;
            
            //���Ӷ�ʱ�Ӳ���Ĵ���
            if((antenna+1)%4==0){
                //fseek(fpCSRH,32,1);
                if (channel == 14){
                	//showoffset();
                	fseek(fpCSRH,8,1);
                	//printf("Integer is:\n");
                	for(i=0; i<16; i++){
                		fread(&buff3[i], 1, 1, fpCSRH);
                		//printf("%.2X ",buff3[i]);
                	}
                	//printf("\n");
                	for(i=0; i<4; i++,antenna3++){
                		//fseek(fpCSRH, 7,1);
                		//fread(&delayInteger, 2, 1, fpCSRH);
                		countDelay(buff3, &delayCSRHData[antenna3], i);
                	//	printf("Antenna's delay is[%d]:%E\n", antenna3+1, delayCSRHData[antenna3]);
              		}
              		fseek(fpCSRH,8,1);
              	}
              	else
              		fseek(fpCSRH,32,1);
            }
        }
        fseek(fpCSRH, 32,1);
    }
    
    return 1;
}

int searchFrameHeader() {
    int i;
    char beginner;
    if (feof(fpCSRH)) {		//����ļ��Ƿ����
        // if Eof then exit current frame reading
        return 0;
    }
    while (!feof(fpCSRH)) {  		
        if ((fread(&beginner,1, 1, fpCSRH))==0)
            break;
        if (beginner == 0x55) {
            for (i = 0; i < 27; i++) {
                if ((fread(&beginner, 1,1, fpCSRH))== 1 ){
                    if (beginner != 0x55)
						break;
                }
                else break;
            }
            if (i == 27) {
                /* Skip 4 bytes */
                fseek(fpCSRH,4,1);
				
                return 1;
            }
        }
    }
    return 0;
}

/*��ݸ��ƫ�������ļ�ָ���λ�ã�ͬʱ�������֡ͷ������ֱ�Ӷ�ȡ���
*����ֵ��
*0�������ļ�ָ��ʧ��
*1�����óɹ���
*/
int setOffset(unsigned long offset)
{
	fpos_t pos;
        #if defined(LINUX)
	pos.__pos = offset;
        #endif
        #if defined(DARWIN)
        pos=offset;
        #endif
	if (fsetpos(fpCSRH, &pos))
	{
		printf("Set position error!\n");
		return 0;
	}
	fseek(fpCSRH, 32, SEEK_CUR);		//���֡ͷ��λ�ã�����ֱ�Ӷ�ȡ���
	return 1;
}

void showoffset()
{
	fpos_t pos;
	if (!fgetpos(fpCSRH, &pos)){
		#if defined(LINUX)
	 	 printf("position is:%x\n",pos.__pos);
		#endif
		#if defined(DARWIN)
		 printf("position is:%x\n",pos);
		#endif
	}
}
