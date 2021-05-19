#define _GNU_SOURCE

#include <math.h>
#include "contiki.h"
#include "contiki-net.h"

#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/ctimer.h>
#include <string.h>

#include "net/ipv6/uiplib.h"
#include "net/routing/routing.h"
#include "net/netstack.h"
#include "net/ipv6/simple-udp.h"

#include "sys/log.h"
#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_DBG

#define WITH_SERVER_REPLY  1
#define RSS_PORT 8765
#define DP_PORT	4568
#define DOWNWARD_PORT 5678
//#define FIFO_FILE "MYFIFO"

static int shmid;
static int down_shmid;
const key_t key = 123456;
const key_t down_key = 123457;

static int time_rsscallback, iter_rss, old_time_rsscallback,
    sephamore_drop_rss, plist[500],totalRx = 0; //, fd, sock, reply_control, first_run_only_if_65;
static char addr_str[56], long_str[100], *shared_memory,*down_memory; //, buff[100], curr_parent[100], msg_cntr[2] = {0};
//const char wait[4] = "WAIT";

static struct ctimer read_timer;
static uip_ipaddr_t new_parent;
//static struct sockaddr_in serv_addr;
static struct simple_udp_connection rssi_conn, data_conn,downward_conn;

PROCESS(udp_server_process, "UDP server");

/*---------------------------------------------------------------------------*/

/*
void read_pipe(){
    // Reading from named pipe for communication with python script
    fd = open(FIFO_FILE_DOWN, O_RDONLY);
    // Erasing buff everytime before reading
    memset(buff, 0, 100 * (sizeof buff[0]))
    if(read(fd, buff, sizeof(buff)))
        //LOG_INFO("buff: %s\n", buff);
        ;
        printf("downward buf: %s\n",buff);
        if(wait[0]==buff[0]&&wait[1]==buff[1]&&wait[2]==buff[2]&&wait[3]==buff[3]) {
        printf("waiting\n");
    } else{
        printf("trying to SEND BEST\n");
        uip_create_linklocal_allnodes_mcast(&new_parent);//broadcast
        simple_udp_sendto(&downward_conn, buff, sizeof(buff), &new_parent);  
    }
    close(fd);
}
*/


// function to encode incoming control string to condensed form
void encoding(const uint8_t *data, const uint8_t i)
{
    // Example
        // Input: r -76 f fe80::212:7401:1:101 t 164 p 
        // Output: 05-761164;
            // 05 -- from 5th anchor node
            // 76 -- RSSI value
            // 1 -- mobile node
            // 164 -- sequence number

    for (int iter_enc = 10*i; iter_enc < ( 10*i + 10 ) ; iter_enc++) {
        // printf("LS:%s\n",long_str);
        if ( iter_enc - 10*i < 2 ) {
            // Adding only the node ID to str
            long_str[iter_enc] = addr_str[ 18 + iter_enc - 10*i ];
        } else if ( iter_enc - 10*i < 5 ) {
            if ( iter_enc - 10*i == 2 )
                // Removing 'R '
                data += 2;
            // Adding RSSI to str
            long_str[iter_enc] = (char) *data++;
        } else if ( iter_enc - 10*i == 5 ) {
            // Removing ' F fe80::212:7402:2:20'
            data += 18;
            // Adding mobile ID to str
            long_str[iter_enc] = (char) *data++;
            // Removing ' T ' 
            data += 3; 
        } else if ( iter_enc - 10*i < 9 ) {
            // Adding time to str
            long_str[iter_enc] = (char) *data++;
        } else {
            long_str[iter_enc] = ';';
        }
    }
    long_str[39] = '\0';

    /*
    // Removing ' P '
    data += 3; 
    if (((char) *data) == 'f') {
        memset(curr_parent, 0, 25 * (sizeof curr_parent[0]));
        for (iter = 0; iter < 20; iter++) 
            curr_parent[iter] = (char) *data++;
        curr_parent[20] = '\0';
    }
    */
}

// function to clean the buffer
void clean(char *var) {
    int i = 0;
    while(var[i] != '\0') {
        var[i] = '\0';
        i++;
    }
}

// function to write into shared memory after 100 ms
static void ctimer_callback() {
    char AP_str[30];
    char MN[30];
    char set[40];
    uip_ipaddr_t  AP_addr;
    // Entering data into shared memory
    memcpy(shared_memory, long_str, strlen(long_str));
    LOG_INFO("Sent buffer\n");
    sephamore_drop_rss = 1;
    //Now reading the response
    printf("down_memory: %s\n", down_memory); 
    // char * token=strtok(down_memory,"\n");
    // while (token != NULL) { 
    //     printf("token: %s\n", token); 
    //     sscanf(token,"%s %s for %s",set,AP_str,MN);
    //     uiplib_ipaddrconv(AP_str,&AP_addr);
    //     LOG_INFO("ADDRESS:");
    //     LOG_INFO_6ADDR(&AP_addr);
    //     LOG_INFO("\n");
    //     printf("set:%s MN:%s\n",set,MN);
    //     if(strcmp(set,"UNSET")!=0 && strcmp(set,"SET")!=0 ){
    //         token = strtok(NULL, "\n"); 
    //         continue;
    //     }
    //     strcat(set,MN);
    //     simple_udp_sendto(&downward_conn, set, sizeof(set), &AP_addr); 
    //     token = strtok(NULL, "\n"); 
    // } 

    char * token=strtok(down_memory,"\n");
    
    printf("trying to SEND BEST %s %d\n",token, sizeof(token));
    uip_create_linklocal_allnodes_mcast(&new_parent);//broadcast
    simple_udp_sendto(&downward_conn, token, strlen(token), &new_parent);  

}

static void
rss_rx_callback(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
    char num_str[3] = "\0";
    char *temp_str;
    
    LOG_INFO("Received request '%.*s' from ", datalen, (char *) data);
    LOG_INFO_6ADDR(sender_addr);
    LOG_INFO_("\n");
    //static struct timer downward_resend_timer;
    memset(addr_str, 0, 56 * (sizeof addr_str[0]));
    uiplib_ipaddr_snprint(addr_str, sizeof(addr_str), sender_addr);

	// Data extraction
    //printf("[INFO: App       ] data: %s\n",data);

    // Delta time occurence
    temp_str = strstr((char *) data, "t");
    temp_str += 2;
    for (int i = 0; i < 3; i++) {
        num_str[i] = *temp_str++;
    }
    time_rsscallback = atoi(num_str);

    if((sephamore_drop_rss == 0) && (time_rsscallback == old_time_rsscallback)) {
        // Appending string list
        encoding(data, iter_rss++);
        LOG_INFO("Encoded data: %s\n", long_str);
    } else if(time_rsscallback != old_time_rsscallback) {
        // Updating control variables
        old_time_rsscallback = time_rsscallback;
        clean(long_str);
        iter_rss = 0;
        sephamore_drop_rss = 0;

        encoding(data, iter_rss++);
        LOG_INFO("Encoded data: %s\n", long_str);
        // setting callback_timer for 200 ms
        ctimer_set(&read_timer, 0.3*CLOCK_SECOND, ctimer_callback, NULL);

    }
	// fd = open(FIFO_FILE, O_WRONLY);
	// int bs=write(fd, str, sizeof(str));
	// if(bs);
	// close(fd);
}

static void sum_list(){
    totalRx=0;
    for (int i=0;i<500;i++){
        if(plist[i]==1)
        totalRx=totalRx+1;
    }
}

static void
dp_rx_callback(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
    char str[280];

    uiplib_ipaddr_snprint(str, sizeof(str), sender_addr);  
    strcat(str,",");
    strcat(str,(char *) data);
    strcat(str,";");
    //send(sock , str , strlen(str) , 0 ); 
    LOG_INFO("Received HELLO '%.*s' from ", datalen, (char *) data);
    int num=0;
    sscanf((char *)data,"hello %d",&num);
    printf("num: %d",num);
    plist[num]=1;
    //LOG_INFO_6ADDR(sender_addr);
    LOG_INFO_("\n");
    //totalRx++;
    sum_list();
    printf("totalRx=%d\n",totalRx);
    //printf("sender_addr: %s\n",(char *)sender_addr);
}

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_server_process, ev, data)
{

	PROCESS_BEGIN();

    /*
	// Create the FIFO if it does not exist
	mkfifo(FIFO_FILE, 0666);
    mkfifo(FIFO_FILE_DOWN, 0666);
    old_parent=NULL;
    */

    // Setup shared memory, 43 is the size
    if ((shmid = shmget(key, 100, IPC_CREAT | 0666)) < 0)
   {
      printf("Error getting shared memory id");
      exit(1);
   }
    // Attached shared memory
    if ((shared_memory = shmat(shmid, NULL, 0)) == (char *) -1) {
        printf("Error attaching shared memory id");
        exit(1);
    }


    if ((down_shmid = shmget(down_key, 200, IPC_CREAT | 0666)) < 0)
   {
      printf("Error getting shared memory id");
      exit(1);
   }
    // Attached shared memory
    if ((down_memory = shmat(down_shmid, NULL, 0)) == (char *) -1) {
        printf("Error attaching shared memory id");
        exit(1);
    }


	simple_udp_register(&rssi_conn, RSS_PORT, NULL, RSS_PORT, rss_rx_callback);
	simple_udp_register(&data_conn, DP_PORT, NULL, DP_PORT, dp_rx_callback);
    simple_udp_register(&downward_conn, DOWNWARD_PORT, NULL, DOWNWARD_PORT, NULL);

    /*
    ctimer_set(&read_timer, 10, read_func, NULL);
    while (1) {
        PROCESS_WAIT_EVENT_UNTIL(ctimer_expired(&read_timer)); //Real Time Event 
        LOG_INFO("ctimer set\n");
        ctimer_set(&read_timer, CLOCK_SECOND, read_func, NULL);
    }
    */
  
    PROCESS_END();
}
