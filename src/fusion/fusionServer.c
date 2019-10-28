/*
 # The fusion status query server based on ZeroMQ platform
 # CSRHOS - Chinese Solar Radio HelioGraph Operation System
 #
 # Created: Since 2014-8-1
 #     CSRHOS Team, Feng Wang， Jiaojiao Gao
 #
 # This file is part of CSRH project
 #
 # This program is free software: you can redistribute it and/or modify
 # it under the terms of the GNU General Public License as published by
 # the Free Software Foundation, either version 3 of the License, or
 # (at your option) any later version.
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License
 # along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <math.h>
#include <time.h>
#include <string.h>
#include <czmq.h>
#include <my_global.h>
#include <mysql.h>

int year,month,day;
double tt;


int main(int argc, char **argv)
{
    
    char result[1500];
    char sql[300];
    zctx_t *context= zctx_new ();
    void *server;
    char *ymdt;
    
    time_t seconds;
    
    struct tm time_fields;
    
    MYSQL *conn;
    MYSQL_RES *sqlresult;
    MYSQL_ROW row;
    unsigned long numRows;
    
    int num_fields;
    int i;
    
    printf("Connecting to database...\n");
    conn = mysql_init(NULL);
    mysql_real_connect(conn, "localhost", "csrh", "csrhos", "csrh", 0, NULL, 0);
    printf("Connected.\n"); 
    
    printf ("Chinese Spectral RadioHeliograph Status Query Services \n");
    printf ("Current supported: Transfer delay compensation, Antenna flag status and weather information\n");
    printf( "Server is starting...\n");
    
    server = zsocket_new(context, ZMQ_REP);
    assert(server);
    zsocket_bind(server, "tcp://*:6666");
    printf ("Server started...");
    
    //load array
    while (!zctx_interrupted) {
        char *request = zstr_recv (server);
        printf("R:%s\n",request);
    	ymdt=strtok(request,"-");
        year=atof(ymdt);
        
        ymdt = strtok(NULL,"-");
        month=atof(ymdt);
        
    	ymdt =strtok(NULL,"-");
        day=atof(ymdt);
        
    	ymdt=strtok(NULL,"-");
        tt=atof(ymdt);
        
        time_fields.tm_mday = day;
        time_fields.tm_mon = month;
        time_fields.tm_year = year-1900;
        time_fields.tm_hour = (int)tt;
        time_fields.tm_min = (tt - time_fields.tm_hour )*60;
        time_fields.tm_sec = (int) ((tt - time_fields.tm_hour - time_fields.tm_min/60.)*3600+0.5);
        
        seconds = mktime(&time_fields);
	printf("%lu\n",seconds);        
       /* Query t_delay */
        sprintf(sql,"SELECT item_value FROM t_delay where start_sec <= %ld and end_sec>= %ld ", seconds,seconds);
        printf("SQL:%s\n",sql);
	mysql_query(conn, sql);
        sqlresult = mysql_store_result(conn);
        num_fields = mysql_num_fields(sqlresult);
        numRows = (unsigned long) mysql_num_rows(sqlresult);
        if (numRows>1)
            strcpy(result,"ERROR;");
        else if (numRows==0)
            strcpy(result,"NULL;");
        else
        {
            row = mysql_fetch_row(sqlresult);
            for(i = 0; i < num_fields; i++)
            {
                strcpy(result, row[i] ? row[i] : "NULL");
            }
            strcat(result,";");
        }
        mysql_free_result(sqlresult);
        
        /* Query t_antenna */
        sprintf(sql,"SELECT item_value FROM t_antenna where start_sec <= %ld and end_sec>= %ld ", seconds, seconds);
        mysql_query(conn, sql);
        sqlresult = mysql_store_result(conn);
        num_fields = mysql_num_fields(sqlresult);
        numRows = (unsigned long) mysql_num_rows(sqlresult);
        if (numRows>1)
            strcat(result,"ERROR;");
        else if (numRows==0)
            strcat(result,"NULL;");
        else
        {
            row = mysql_fetch_row(sqlresult);
            for(i = 0; i < num_fields; i++)
            {
                strcat(result, row[i] ? row[i] : "NULL");
            }
            strcat(result,";");
        }
        mysql_free_result(sqlresult);
        
        /* Query t_weather */
        /* Query t_antenna */
        sprintf(sql,"SELECT item_value FROM t_weather where start_sec <= %ld and end_sec>= %ld ", seconds,seconds);
        mysql_query(conn, sql);
        sqlresult = mysql_store_result(conn);
        num_fields = mysql_num_fields(sqlresult);
        numRows = (unsigned long) mysql_num_rows(sqlresult);
        if (numRows>1)
            strcat(result,"ERROR");
        else if (numRows==0)
            strcat(result,"NULL");
        else
        {
            row = mysql_fetch_row(sqlresult);
            for(i = 0; i < num_fields; i++)
            {
                strcat(result, row[i] ? row[i] : "NULL");
            }
        }
        mysql_free_result(sqlresult);
        
        printf("%s\n",result);
        zstr_send(server,result);
    }
    
    
    zctx_destroy (&context);
    mysql_close(conn);
    
    return 0;
}
