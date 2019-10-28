#include "uvfits.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void main(int argc, char **argv)
{
    int ret=0,i=0,j=0,k=0,l=0;
    uvdata *x;
    uvdata **myuvdata=&x;


    if (argc<=1)
    {
        printf("Usage: muserreaduvfits <filename>\n");
        exit(0);
    }

    //uvfitsSetDebugLevel(1);
    ret=readUVFITS(argv[1],myuvdata);
    x=*myuvdata;

    printf("return %d .\n",ret);
    printf("int\tn_pol=%d\n",x->n_pol);
    printf("int\tpol_type=%d\n",x->pol_type);
    printf("int\tn_freq=%d\n",x->n_freq);
    printf("float\tn_vis=%d\n",x->n_vis);
    printf("float\tcent_freq=%f\n",x->cent_freq);
    printf("float\tfreq_delta=%f\n",x->freq_delta);

    printf("double\t*date=%p\n",x->date);
    printf("\tthe size of date is n_vis=%d\n",x->n_vis);
    for (i=0; i<x->n_vis; i++)
    {
        //printf("date[%d] addr=%p,value=%f\n",i,&((x->date)[i]),(x->date)[i]);
        printf("\tdouble date[%d] addr=%p,value=%f\n",i,&x->date[i],x->date[i]);
    }



    printf("int*\tn_baselines=%p\n",x->n_baselines);
    printf("\tthe size of n_baselines is n_vis=%d\n",x->n_vis);
    for (j=0; j<x->n_vis; j++)
    {
        printf("\tint n_baselines[%d] addr=%p,value=%d\n",j,&x->n_baselines[j],x->n_baselines[j]);
    }

    printf("source_table *source=%p\n",x->source);
    printf("\t char name[]=%s\n",x->source->name);
    printf("\t int id=%d\n",x->source->id);
    printf("\t int qual=%d\n",x->source->qual);
    printf("\t char calcode[]=%s\n",x->source->calcode);
    printf("\t int freq_id=%d\n",x->source->freq_id);
    printf("\t double ra=%f\n",x->source->ra);
    printf("\t double dec=%f\n",x->source->dec);


    printf("ant_bable*\tantennas=%p\n",x->antennas);
    printf("\tthe size of antennas is =%d\n",x->array->n_ant);
    for (i=0; i<x->array->n_ant; i++)
    {
        printf("\tantennas[%d]->name=%s\n",i,x->antennas[i].name);
        printf("\tantennas[%d]->xyz_pos={%f,%f,%f}\n",i,x->antennas[i].xyz_pos[0],x->antennas[i].xyz_pos[1],x->antennas[i].xyz_pos[2]);
        printf("\tantennas[%d]->xyz_deriv={%f,%f,%f}\n",i,x->antennas[i].xyz_deriv[0],x->antennas[i].xyz_deriv[1],x->antennas[i].xyz_deriv[2]);

        printf("\tantennas[%d]->station_num=%d\n",i,x->antennas[i].station_num);
        printf("\tantennas[%d]->mount_type=%d\n",i,x->antennas[i].mount_type);
        printf("\tantennas[%d]->axis_offset={%f,%f,%f}\n",i,x->antennas[i].axis_offset[0],x->antennas[i].axis_offset[1],x->antennas[i].axis_offset[2]);
        printf("\tantennas[%d]->pol_angleA=%f\n",i,x->antennas[i].pol_angleA);
        printf("\tantennas[%d]->pol_calA=%f\n",i,x->antennas[i].pol_calA);
        printf("\tantennas[%d]->pol_angleB=%f\n",i,x->antennas[i].pol_angleB);
        printf("\tantennas[%d]->pol_typeA=%s\n",i,x->antennas[i].pol_typeA);
        printf("\tantennas[%d]->pol_typeB=%s\n",i,x->antennas[i].pol_typeB);
    }

    printf("array_data*\tarray=%p\n",x->array);
    printf("\tthe size of array is 1\n");

    printf("\tint n_ant=%d\n",x->array->n_ant);
    printf("\tdouble xyz_pos[]={%f,%f,%f}\n",x->array->xyz_pos[0],x->array->xyz_pos[1],x->array->xyz_pos[2]);
    printf("\tchar name=%s\n",x->array->name);

    printf("float**\tvisdata=%p  weightdata=%p\n",x->visdata,x->weightdata);
    printf("\tthe size of visdata & weightdata is  %d\n",x->n_vis);
    for (i=0; i<x->n_vis; i++)
    {
        printf("\t\tthe size of visdata & weightdata[%d]  is %d\n",i,x->n_freq*x->n_pol*x->n_baselines[i]*2);
        for (j=0; j<x->n_baselines[i]; j++)
        {
            for (k=0; k<x->n_freq; k++)
            {
                for (l=0; l<x->n_pol; l++)
                {
                    printf("visdata[%d][%d][%d][%d]={%f,%f}  weightdata=%f\n",i,j,k,l,x->visdata[i][(j*x->n_freq*x->n_pol+k*x->n_pol+l)*2],x->visdata[i][(j*x->n_freq*x->n_pol+k*x->n_pol+l)*2+1],x->weightdata[i][j*x->n_freq*x->n_pol+k*x->n_pol+l]);
                }
            }
        }
    }


    printf("float**\tbaseline=%p  \n",x->baseline);
    printf("double**\tu=%p  \n",x->u);
    printf("double**\tv=%p  \n",x->v);
    printf("double**\tw=%p  \n",x->w);
    printf("\tthe size of baseline & u v w  is  %d\n",x->n_vis);
    for (i=0; i<x->n_vis; i++)
    {
        printf("\t\tthe size of baseline & u v w[%d]  is %d\n",i,x->n_baselines[i]);
        for (j=0; j<x->n_baselines[i]; j++)
        {
            printf("baseline u v w[%d][%d]={%f,%f,%f,%f}\n",i,j,x->baseline[i][j],x->u[i][j],x->v[i][j],x->w[i][j]);
        }
    }

}
