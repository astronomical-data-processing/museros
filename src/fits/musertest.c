#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <capi.h>
#if defined(LINUX)
#include <error.h>
#endif
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "muserrawdata.h"

typedef struct
{
    char header[32];
    long long time;
    char stuff[148];
    char polarization[2];
    unsigned short  subband;
    char stuff1[99264-192];
    unsigned short  subband2;
}  Frame;


void usage(const char *name)
{
    fprintf(stdout, "my tester for the C API of %s\n"
            "Insert Example:\n"
            "%s -d dir -i\n\n"
            "Query Example:\n"
            "%s -d dir -q 'time>=1 and time<=2'\n\n",
            fastbit_get_version_string(), name,name);
} /* usage */


int scanframebyfread(char* filename)
{
    if (openCSRHFile(filename)==0)
    {
        printf("Cannot open file %s\n",filename);
        exit(1);
    }

    int i=0;
    /* Search the beginning of the file */
    while (searchFrameHeader() && i<19200)
    {
        //showoffset include in csrhrawdata.c
        readOneFrame();
        i++;
    }

    closeCSRHFile();
    printf("i frames founded %d\n",i);


}

char * csrh_memmem (const char *s1, size_t l1, const char *s2,size_t l2, size_t start)
{
    const char *p = s1+start;
    const size_t len = l2;
    for (; (p = memchr (p, 0x55,l1-start)) != 0; p++)
    {

        if (strncmp (p, s2, len) == 0)
            return (char *)p;
    }
    return (0);
}

int searchFrameHeaderbymmap(char * buffer,size_t len,size_t start)
{
    char* pos;
    char pattern[28];
    int i;
    for(i=0; i<28; i++)  pattern[i]=0x55;
    pos=csrh_memmem(buffer,len,pattern,28,start);
    if (pos==0)
    {
        return -1;
    }
    else
        return pos-buffer;

}


int scanOneFrameBymmap(char * buffer)
{
    Frame *fr;
    fr=(Frame *)buffer;
    currentFrameTime = convertTime(fr->time);

    char freq;
    // Determine the subband
    switch (fr->subband)
    {
        case 0x3333:
            freq = 1;
            break;
        case 0x7777:
            freq = 2;
            break;
        case 0xbbbb:
            freq = 3;
            break;
        case 0xcccc:
            freq = 4;
            break;
        default:
            switch (fr->subband2)
            {
                case 0x0000:
                    freq = 1;
                    break;
                case 0x5555:
                    freq = 2;
                    break;
                case 0xaaaa:
                    freq = 3;
                    break;
                case 0xffff:
                    freq = 4;
                    break;
                default:
                    break;
            }
            break;
    }
	int time=0;
        time = currentFrameTime.Hour*10000+currentFrameTime.Minute*100+currentFrameTime.Second;
        printf(",time=%d",time);
        printf(",freq=%d\n",freq);

    return 1;
}


int scanframebymmap(char* filename)
{
    int fd_r,fd_w;
    struct stat file_stat;
    int file_len_r;
    char *file_buf_r,*file_buf_w;

//�򿪽�Ҫ�������ļ�

    fd_r = open(filename,O_RDONLY);

    if(fd_r == -1)
    {
        perror("open file fail:");
        exit(1);
    }

//��ȡҪ�����ļ�������

    if(fstat(fd_r,&file_stat)==-1)
    {
        perror("get file stat fail:");
        close(fd_r);
        exit(1);
    }

//�������л�ȡ�ļ��ĳ���
    file_len_r = file_stat.st_size;


//�����ļ�������ӳ�䵽�ڴ档

    file_buf_r =(char *)mmap(NULL,file_len_r,PROT_READ,MAP_SHARED,fd_r,SEEK_SET);
    if(file_buf_r == MAP_FAILED)
    {
        perror("map file_read fail:");
        close(fd_r);
        exit(1);
    }

//ӳ�佨����ر��ļ���ֻҪӳ�佨�����ر��ļ�ӳ���ϵ��Ȼ���ڡ�
    close(fd_r);
    size_t offset=0;
    while(1)
    {
        offset=searchFrameHeaderbymmap(file_buf_r,file_len_r,offset);
        if (offset==-1) break;
        printf("offset=%d,",offset);
        scanOneFrameBymmap(file_buf_r+offset);
        offset+=100000;

    }





}





int main(int argc, char **argv)
{
    if (3!=argc)
    {
        usage(*argv);
        exit(0);
    }

    if (argv[1][0]=='1')
    {
        printf("mmap\n");
        scanframebymmap(argv[2]);
    }
    else

    {
        printf("fread\n");
        scanframebyfread(argv[2]);
    }


} /* main */


