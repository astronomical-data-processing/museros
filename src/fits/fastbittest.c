#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <capi.h>
#include "fastbit.h"
void usage(const char *name)
{
    fprintf(stdout, "my tester for the C API of %s\n"
            "Insert Example:\n"
            "%s -d dir -i\n\n"
            "Query Example:\n"
            "%s -d dir -q 'time>=1 and time<=2'\n\n",
            fastbit_get_version_string(), name,name);
} /* usage */

int  addrows(const char *dir)
{
    const char *conffile=NULL;
    int i;
    char **filename;
    filename=malloc(100*sizeof(char*));
    int *time;
    time=malloc(100*sizeof(double));
    char *pc;
    pc=malloc(100*sizeof(char));
    unsigned long *offset;
    offset=malloc(100*sizeof(unsigned long ));



    for(i=0; i<100; i++)
    {
        filename[i]=malloc(sizeof(char)*20);
        sprintf(filename[i],"filename%d",i);
        time[i]=i;
        pc[i]=i;
        offset[i]=i;
    }
    fastbit_init((const char*)conffile);
    fastbit_set_verbose_level(1);

    appendrows(filename,time,pc,offset,100);
    fastbit_flush_buffer(dir);

}

int queryrows(const char *dir,const char *conditions)
{
    ResultSet  rs;
    int i;
    int ret=selectrows(dir, conditions,&rs);
    for (i=0; i<ret; i++)
    {
        printf("here %s,%d,%d,%d\n",rs.filename[i],rs.time[i],rs.pc[i],rs.offset[i]);
    }
    freerows(&rs);
    
}


int main(int argc, char **argv)
{
    if (1==argc)
    {
        usage(*argv);
        exit(0);
    }

    if (argv[1][0]=='-' && argv[1][1]=='d')
    {
        if (argv[3][0]=='-' && argv[3][1]=='i')
        {

            addrows(argv[2]);
        }
        else
        {
            if (argv[3][0]=='-' && argv[3][1]=='q')
            {
                queryrows(argv[2],argv[4]);
            }
        }
    }
    else
    {
        usage(*argv);
        exit(0);
    }

} /* main */

