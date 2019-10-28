#ifndef CSRH_FASTBIT_H
#define  CSRH_FASTBIT_H

typedef struct {
    char** filename;
    int *time;
    char  *pc;
    unsigned long *offset;
    int rowcount;
}  ResultSet;

int	appendrows(char **filename,int *time,char  *pc,unsigned long *offset, int count);
int	selectrows(const char *dir,const char *conditions,ResultSet* rsh);


#endif