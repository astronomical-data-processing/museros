#include "muserrawdata.h"
#include "fastbit.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#define  LINE 19200

FILE *input,*output,*fpCSRH;
char *filename[LINE];			// ���ڴ洢�ļ���
int HMS[LINE];  //���ڴ洢ʱ��
char stripSwitchBand[LINE];  	//���弫����Ƶ�ʣ����ּ���������Ƶ�ʣ�
unsigned long offset[LINE];			//������ļ���ʼλ�õ�ƫת
CSRHSystemTime OneFrameTime;  //����ʱ��ṹ�����洢ʱ��
unsigned char block[100000];  //�ļ����ƻ�����
int simtime = 0;  //ģ��һ�죨600����ݣ����ļ�����
char dir[9],dir_user[100];		//���屣���ļ���������,���ڴ������洢·��

//��ʾ������Ϣ
int datasim = 0;  //�������ģ�⣬0��ʾ��ģ����ݣ�1��ʾģ��һ������
int showprintf = 2;   //������ʾprintf��Ϣ��0����ʾ��1��ʾ,2��ʾ��ȡ�����Ϣ

void JudgeArgc(int argc, char **argv);
void CpFilename(int argc,char **argv) ;
void DataSim(int argc, char **argv);
int ScanInfo(int argc,char **argv);
int ScanOneFrame(int i);
int Cp_SearchHeader();
int Cp_ScanOneFrame(int i);
int ShowOffset(int argc,char **argv);
int ShowTime(int i);
int ShowDayTime(int i);
void ManageInfo(int argc,char **argv);
int CheckScanData();
void strncpyTwo(char *dest, const char *source, unsigned count);

void main(int argc, char **argv)
{
    printf("The program is runing ....\n");
    if (argc<=1) {
        printf("Argc Wrong! Run Example:\n");
        printf("./csrhscanrawdata filename \n");
        printf("./csrhscanrawdata -d dir(storage way)filename \n");
        printf("./csrhscanrawdata filename CpFilename(dir)\n");
        printf("./csrhscanrawdata -d dir(storage way)filename CpFilename(dir) \n");
        exit(0);
    }
    JudgeArgc(argc,argv); //�ж�-d�ļ�··��������ļ����и���
    DataSim(argc,argv);
    if(argc == 2 || argc == 4)  //�������ļ�
        fclose(fpCSRH);
    else {
        fclose(input);
        fclose(output);
    }
}

//��һ�����ݣ�600�Σ�ģ��
void DataSim(int argc, char **argv)
{
		//��ģ�����
    if(datasim == 0) {
        ScanInfo(argc,argv);
        ManageInfo(argc,argv);
        printf("The data has been done!\n");
    }
    //ģ�����
    else if(datasim == 1){
        while(simtime<600) {
            ScanInfo(argc,argv);
            ManageInfo(argc,argv);
            printf("\nthe data :%d has been done!\n\n",simtime);
            simtime++;
        }
    }
    else{
    	printf("The fpCSRH donot been dispose! Please check datasim value!\n");
    	exit(1);
    }    	
}

//�ж�-d�ļ�··��������ļ����и���
void JudgeArgc(int argc, char **argv) {
    char *cpfilename,*cptmpname;

    //argc = 2��argc = 3�����������·����Ĭ�ϵ�ǰ·�� 
    if(argc == 2 || argc == 3) {
        if(argc == 2) { // �������ļ�
            if(openCSRHFile(argv[1]) == 0 ) {
                printf("Cannot open file %s\n", argv[1]);
                perror( "Warm message" );
                exit(1);
            }
        }
        else { //argc = 3 �����ļ�
            input = fopen( argv[1], "rb" );
            if (input == 0) {
                printf("Cannot open file %s\n",argv[1]);
                perror( "Warm message" );
                exit(1);
            }
            CpFilename(argc,argv);
        }
    }
    //argc = 4��argc = 5���������·��
    else {
        if ((argc == 4 || argc == 5 ) && (argv[1][0]) == '-' && (argv[1][1] == 'd')) {
            if(argc == 4) { //�������ļ�
                if(openCSRHFile(argv[3]) == 0 ) {
                    printf("Cannot open file %s\n", argv[3]);
                    perror( "Warm message" );
                    exit(1);
                }
            }
            else { //argc = 5 //�����ļ�
                input = fopen( argv[3], "rb" );
                if (input == 0) {
                    printf("Cannot open file %s\n",argv[3]);
                    perror( "Warm message" );
                    exit(1);
                }
                CpFilename(argc,argv);
            }
            strcpy(dir_user, argv[2]);
            /*��·�������"/",ʹ��ȡ����λ��Ϊ·��*/
            strcat(dir_user,"/");
        }
    }
}

//��ʾ����Ҫ��ȡ����Ϣ�ļ���֡ʱ�䡢������Ƶ�ʡ�ƫ��
int ScanInfo(int argc,char **argv) {
    int i=0;

    //�������ļ�
    if(argc == 2 || argc == 4 ) {
        while (searchFrameHeader()&& i < LINE) {  //Ѱ���ļ�ͷ
            offset[i] = ShowOffset(argc,argv);    //ƫ�� �ڽ��ж�֮֡ǰ�ͽ����жϣ������践�ض�ȡ��֡������
            if (ScanOneFrame(i)) { //��ȡһ��֡
                //��ݲ������ָ���ļ����λ�ã�argc=4Ϊ������ļ�·��
                if(argc == 2)
              		filename[i] = argv[1];
              	else
              		filename[i] = argv[3];
                if(datasim == 0)
                    ShowTime(i);  //һ���ӵ����ʱ��
                else
                    ShowDayTime(i);  //ģ��һ������ʱ��
                i++;
            }
        }
    }
    //�����ļ�
    else {
        while (Cp_SearchHeader()&& i < LINE) {  //Ѱ���ļ�ͷ
            offset[i] = ShowOffset(argc,argv) - 99968;    //ƫ�� �ڽ��ж�֮֡ǰ�ͽ����жϣ������践�ض�ȡ��֡������
            if (Cp_ScanOneFrame(i)) { //��ȡһ��֡
                /*��ݲ������ָ���ļ����λ�ã�argc=4Ϊ������ļ�·��*/
                if(argc == 3)
              		filename[i] = argv[1];
              	else
              		filename[i] = argv[3];                
                if(datasim == 0)
                    ShowTime(i);  //һ���ӵ����ʱ��
                else
                    ShowDayTime(i);  //ģ��һ������ʱ��
                i++;
            }
        }
    }
}

//����Ŀ���ļ��ļ���
void CpFilename(int argc,char **argv) {
    char *cpfilename,*cptmpname;
    char *filedir;

    if(argc == 3) {
        cptmpname = strrchr(argv[2],'/');
        if(*(++cptmpname) == '\0') {
            cptmpname = strrchr(argv[1],'/');
            cpfilename = strcat(argv[2],++cptmpname);
            output = fopen(cpfilename, "wb" );
            if (output == 0) {
                printf("Cannot open file %s\n",cpfilename);
                perror( "Warm message" );
                exit(1);
            }
        }
        else {
            output = fopen(argv[2] , "wb" );
            if (output == 0) {
                printf("Cannot open file %s\n",argv[2]);
                perror( "Warm message" );
                exit(1);
            }
        }
    }
    else { //argc ==5
        cptmpname = strrchr(argv[4],'/');
        cptmpname++;
        if(*cptmpname == '\0') {
            cptmpname = strrchr(argv[3],'/');
            cpfilename = strcat(argv[4],++cptmpname);
            output = fopen(cpfilename, "wb" );
            if (output == 0) {
                printf("Cannot open file %s\n",cpfilename);
                perror( "perror says open failed" );
                exit(1);
            }
        }
        else {
            output = fopen(argv[4], "wb" );
            if (output == 0) {
                printf("Cannot open file %s\n",argv[4]);
                perror( "perror says open failed" );
                exit(1);
            }
        }
    }
}


//���ɨ��Ľ��д���������
void ManageInfo(int argc,char **argv) {
    const char *conffile=NULL;

    /*show all message*/
    if(showprintf == 2)
        CheckScanData();
    fastbit_init((const char*)conffile);
    fastbit_set_verbose_level(1);
    appendrows(&filename[0],&HMS[0],&stripSwitchBand[0],&offset[0],LINE) ;
    if(argc == 2 || argc == 3)  //û��-d������ڵ�ǰ·����
        fastbit_flush_buffer(dir);
    else {  //����-d������Ҫ�Ա����ļ�·���������¸�ֵ
        strcat(dir_user,dir);
        fastbit_flush_buffer(dir_user);
        strcpy(dir_user, argv[2]);//��dir_user���¸�ֵ
        strcat(dir_user,"/");
    }
}

//ɨ��֡����е�ʱ�䣬������Ƶ��
int ScanOneFrame(int i) {
    char *base;
    int PolsubBand=0;
    int Frequency;

    //readout system time csrhrawdata.h�Ľṹ��CSRHSystemTime����
    base = ((char *) &(currentFrameHeader.systemtime));
    if ((fread(base,8,1,fpCSRH))==0)
        return 0;
    if (showprintf == 1)
        printf("base: %x \n",base);
    OneFrameTime = convertTime(currentFrameHeader.systemtime);

    /*frequency switch 4�� read spare 64��bandWidth 4��quantizationLevel 4��delaySwitch 4��strip switch 4
    �����,���,������ƽȨֵ����ֵ���ӳٵ���أ�������ת���� ����148bit*/
    fseek(fpCSRH, 148, 1);
    // read subBand		�Ӵ�����ʽ 32bit
    if ((fread((char *) (&currentFrameHeader.subBand), 4, 1, fpCSRH))==0)
        return 0;

    // Determine the subband
    int subBand = (currentFrameHeader.subBand >> 16);  //�ж���ƵƵ�ʣ���16bits��
    if (showprintf == 1)
        printf("subBand: %x \n",subBand);
    switch (subBand) {
    case 0x3333:
        Frequency = 4;
        break;
    case 0x7777:
        Frequency = 8;
        break;
    case 0xbbbb:
        Frequency = 12;
        break;
    case 0xcccc:
        Frequency = 16;
        break;
    default:
        fseek(fpCSRH, 99264 - 192, 1);
        unsigned short subBandTmp;
        if ((fread(&subBandTmp,2,1,fpCSRH))==0)
            return 0;
        if (showprintf == 1)
            printf("subBandTmp: %x \n",subBandTmp);
        switch(subBandTmp) {
        case 0x0000:
            Frequency = 4;
            break;
        case 0x5555:
            Frequency = 8;
            break;
        case 0xaaaa:
            Frequency = 12;
            break;
        case 0xffff:
            Frequency = 16;
            break;
        }
        break;
    }
    //���?����ʽ
    PolsubBand=(i%2)*4+Frequency/4;
    stripSwitchBand[i] = PolsubBand;
    return 1;
}

//��ģ�����ʱ����д���
int ShowDayTime(int i) {
    int Time,Date,Minute;
    Minute=OneFrameTime.Hour*60+OneFrameTime.Minute+simtime;
    OneFrameTime.Hour=Minute/60;
    OneFrameTime.Minute=Minute%60;
    Time = OneFrameTime.Hour*10000+OneFrameTime.Minute*100+OneFrameTime.Second;
    if (showprintf == 1)
        printf("Time:%d\n",Time);
    HMS[i] = Time;
    if(i == 0) {
        Date = OneFrameTime.Year*10000+OneFrameTime.Month*100+OneFrameTime.Day;
        sprintf(dir,"%d",Date);
        if (showprintf == 1)
            printf("dir: %s\n",dir);
    }
    return 0;
}

//������ݵ�ʱ�䲢��ȡ������λ��
int ShowTime(int i) {
    int Time,Date;
    /*csrhrawdata.h�ڵ�ʱ��ṹ��ֻ����ʱ���룬ֻ�豣��ʱ����*/
    Time = OneFrameTime.Hour*10000+OneFrameTime.Minute*100+OneFrameTime.Second;
    if (showprintf == 1)
        printf("Time:%d\n",Time);
    HMS[i] = Time;

    //get the date as the dir name
    if(i == 0) {
        Date = OneFrameTime.Year*10000+OneFrameTime.Month*100+OneFrameTime.Day;
        sprintf(dir,"%d",Date);
        if (showprintf == 1)
            printf("dir: %s\n",dir);
    }
    return 0;
}

//��ʾ�ļ�ƫ��
int ShowOffset(int argc,char **argv) {
    fpos_t Offset;
    if(argc == 2 || argc == 4)
        fgetpos(fpCSRH, &Offset);
    else
        fgetpos(input, &Offset);
    if(showprintf == 1)
    {
	#if defined(LINUX)
        printf("Offset:%d\n",Offset.__pos-32);
        #endif
	#if defined(DARWIN)
	printf("offset:%d\n",Offset-32);
	#endif
    }
    #if defined(LINUX)
    return Offset.__pos-32;
    #endif
    #if defined(DARWIN)
    return Offset-32;
    #endif
}

//���ɨ�����
int CheckScanData() {
    int k=0;
    printf("all frame is :\n");
    while(k < LINE) {
        printf("%s\t %d\t %d\t %d \n",filename[k],HMS[k],stripSwitchBand[k],offset[k]);
        k++;
    }
}

//�������
int Cp_SearchHeader() {
    int value,j ;

    if((value = fread( block, sizeof( char ), 100000, input )) > 0) {
        fwrite( block, sizeof( char ), 100000, output );
    }
    //���ļ�ͷ������֤
    for (j = 0; j < 28; j++) {
        if (block[j] != 0x55) {
            printf("The frame head error!\n");
            exit(1);
        }
        break;
    }
}

//��дstrncpy�������������
void strncpyTwo(char *dest, const char *source, unsigned count)
{
    while(count) {
        *dest++=*source++;
        count--;
    }
}

//�ӻ������ɨ��֡��ݣ�ʱ�䣬������Ƶ�ʣ�
int Cp_ScanOneFrame(int i) {
    char *base;
    unsigned char *tmp;
    int PolsubBand=0;
    int Frequency;
    unsigned short subBandTmp;

    //readout system time csrhrawdata.h�Ľṹ��CSRHSystemTime����
    base = ((char *) &(currentFrameHeader.systemtime));
    tmp = &block[32];
    strncpyTwo(base, tmp, 8);
    if (showprintf == 1)
        printf("base: %x \n",base);
    OneFrameTime = convertTime(currentFrameHeader.systemtime);
    /*frequency switch 4�� read spare 64��bandWidth 4��quantizationLevel 4��delaySwitch 4��strip switch 4
    �����,���,������ƽȨֵ����ֵ���ӳٵ���أ�������ת���� ����148bit
    ����ļ�ͷ32bit ʱ��8bit ����188*/
    tmp = &block[188];
    strncpyTwo((char *)(&currentFrameHeader.subBand), tmp, 4);
    // Determine the subband
    int subBand = (currentFrameHeader.subBand >> 16);  //�ж���ƵƵ�ʣ���16bits��
    if (showprintf == 1)
        printf("subBand: %x \n",subBand);
    switch (subBand) {
    case 0x3333:
        Frequency = 4;
        break;
    case 0x7777:
        Frequency = 8;
        break;
    case 0xbbbb:
        Frequency = 12;
        break;
    case 0xcccc:
        Frequency = 16;
        break;
    default:
        tmp = &block[32+8+148+4+99264-192];
        strncpyTwo((char *)(&subBandTmp), tmp, 2);
        if (showprintf == 1)
            printf("subBandTmp: %x \n",subBandTmp);
        switch(subBandTmp) {
        case 0x0000:
            Frequency = 4;
            break;
        case 0x5555:
            Frequency = 8;
            break;
        case 0xaaaa:
            Frequency = 12;
            break;
        case 0xffff:
            Frequency = 16;
            break;
        }
        break;
    }
    /*���?����ʽ*/
    PolsubBand=(i%2)*4+Frequency/4;
    stripSwitchBand[i] = PolsubBand;
    return 1;
}

