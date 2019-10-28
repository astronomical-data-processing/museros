#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <capi.h>
#include "fastbit.h"

int	appendrows(char **filename,int *time,char  *pc,unsigned long *offset, int count)
{
    fastbit_add_values("filename", "text", filename, count, 0);
    fastbit_add_values("time", "int", time, count, 0);
    fastbit_add_values("pc", "byte", pc, count, 0);
    fastbit_add_values("offset", "ulong", offset, count, 0);
}


int	selectrows(const char *dir,const char *conditions,ResultSet* rsh)
{
    int ret,i;
    int nhits ;
    FastBitQueryHandle  qh;
    FastBitResultSetHandle rh;
    qh = fastbit_build_query("offset,filename,time,pc", dir, conditions);
    nhits = fastbit_get_result_rows(qh);
    if (nhits<=0)
        return nhits;
    rsh->rowcount=nhits;
    rh = fastbit_build_result_set(qh);
    if (rh != 0)
    {
        rsh->filename=malloc(sizeof(char*)*nhits);
        rsh->time=malloc(sizeof(int)*nhits);
        rsh->pc=malloc(sizeof(char)*nhits);
        rsh->offset=malloc(sizeof(unsigned long)*nhits);
        i=0;
        while (fastbit_result_set_next(rh) == 0)
        {
            //printf("%s,%s,%s,%s\n", fastbit_result_set_getString(rh, 0), fastbit_result_set_getString(rh, 1), fastbit_result_set_getString(rh, 2), fastbit_result_set_getString(rh, 3));
            rsh->offset[i]=fastbit_result_set_getLong(rh,0);
            //      rsh->filename[i]=malloc(strlen( fastbit_result_set_getString(rh,1)));
            rsh->filename[i]=malloc(100);
            strcpy(rsh->filename[i], fastbit_result_set_getString(rh,1));
            rsh->time[i]=fastbit_result_set_getInt(rh,2);
            rsh->pc[i]=fastbit_result_set_getInt(rh,3);
            i++;

        }

        fastbit_destroy_result_set(rh);
    }

    fastbit_destroy_query(qh);
    return nhits;
}


int	freerows(ResultSet* rsh)
{
    int i;
    if (rsh->time) free(rsh->time);
    if (rsh->pc) free(rsh->pc);
    if (rsh->offset) free(rsh->offset);
    for (i=0; i<rsh->rowcount; i++)
    {
        if (rsh->filename)  free(rsh->filename[i]);
    }
    if (rsh->filename) free(rsh->filename);

}


