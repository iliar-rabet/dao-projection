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
#define DAT_PORT 4568
#define DWN_PORT 5678
#define UP_SHM_KEY 123456
#define DN_SHM_KEY 123457

static int up_shm_id, dn_shm_id, time_rsscallback, iter_rss, old_time_rsscallback,
    sephamore_drop_rss, totalRx = 0;
static char addr_str[56], long_str[500],
    *shared_memory_up, *shared_memory_down, *shared_memory_rflx;

static struct ctimer read_timer;
static struct ctimer read_timer2;
static struct simple_udp_connection rssi_conn, data_conn, down_conn;

PROCESS(udp_server_process, "UDP server");

/*---------------------------------------------------------------------------*/
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
    printf("data:%s\n",data);

    strcat(long_str,data);   
    strcat(long_str," a ");
    strcat(long_str,addr_str);            
    strcat(long_str,"|");
    long_str[strlen(long_str)]='\0';
    printf("encoding %s\n",long_str);

}


// function to clean the buffer
void clean(char *var) {
    int i = 0;
    for(;i<500;i++){
        var[i] = '\0';
    }
}



// function to write into shared memory after 300 ms
static void ctimer_callback() {
    
    // Entering data into shared memory
    memcpy(shared_memory_up, long_str, strlen(long_str));
    printf("Sent buffer\n");
    sephamore_drop_rss = 1;
    
}


static void ctimer2_callback() {
    char set_unset_value[40], anchor_node[26], mobile_node[26];
    uip_ipaddr_t  anchor_node_address;
    int i;
    
    // Now reading the response
    char * curLine = shared_memory_down;
    printf("Full Line=[%s]\n", curLine);

    char * token = strtok(curLine, ";");
    // loop through the string to extract all other tokens
    while( token != NULL ) {

        printf("token=[%s]\n", token);
        
        memset(anchor_node, 0, 26*sizeof(char));
        sscanf(token, "%s %s for %s", set_unset_value, anchor_node, mobile_node);
        if(uiplib_ipaddrconv(anchor_node, &anchor_node_address) == 0) {
            LOG_INFO("ERR: IP ADDR converting\n");
            return;
        }
        else
        {
            LOG_INFO("set_unset_value = %s\tmobile_node = %s\t anchor_node = %s ->", set_unset_value, mobile_node, anchor_node);
            LOG_INFO_6ADDR(&anchor_node_address);
            LOG_INFO("\n");

            strcat(set_unset_value, " ");
            strcat(set_unset_value, mobile_node);
            simple_udp_sendto(&down_conn, set_unset_value, strlen(set_unset_value), &anchor_node_address);
        }

        token = strtok(NULL, ";");
    }

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

    // Delta time occurence
    temp_str = strstr((char *) data, "t");
    temp_str += 2;
    for (int i = 0; i < 3; i++) {
        num_str[i] = *temp_str++;
    }
    time_rsscallback = atoi(num_str);


        //     uip_ipaddr_t  anchor_node_address;
        // uiplib_ipaddrconv("fe80::c30c:0:0:3", &anchor_node_address);
        // simple_udp_sendto(&down_conn, "TEST_DOWN", strlen("TEST_DOWN"), &anchor_node_address);


    if((sephamore_drop_rss == 0) && (time_rsscallback == old_time_rsscallback)) {
        // Appending string list
        
        encoding(data, iter_rss++);
        //LOG_INFO("Encoded data: %s\n", long_str);
    } else if(time_rsscallback != old_time_rsscallback) {
        // Updating control variables
        old_time_rsscallback = time_rsscallback;
        clean(long_str);
        clean(shared_memory_up);
        printf("encoding CLEANED\n");
        
        iter_rss = 0;
        sephamore_drop_rss = 0;

        
        encoding(data, iter_rss++);
        // LOG_INFO("Encoded data: %s\n", long_str);
        // setting two different callback_timer, the difference would be the multipath time
        ctimer_set(&read_timer, 0.5*CLOCK_SECOND, ctimer_callback, NULL);
        ctimer_set(&read_timer2, 0.55*CLOCK_SECOND, ctimer2_callback, NULL);
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
    char str[26];
    int num=0;

    uiplib_ipaddr_snprint(str, sizeof(str), sender_addr);
    sscanf((char *) data, "hello %d", &num);
    LOG_INFO("Received data: \"hello %d\" from %s\n", num, str);
    LOG_INFO("num = %d\ttotalRx = %d\n", num, totalRx++);
}

/*---------------------------------------------------------------------------*/

static struct etimer periodic_timer;

PROCESS_THREAD(udp_server_process, ev, data)
{

    PROCESS_BEGIN();

    // Setup upward shared memory, 100 is the size
    if ((up_shm_id = shmget(UP_SHM_KEY, 600, IPC_CREAT | 0666)) < 0) {
        printf("Error getting shared memory id");
        exit(1);
    }
    // Attached shared memory
    if ((shared_memory_up = shmat(up_shm_id, NULL, 0)) == (char *) -1) {
        printf("Error attaching shared memory id");
        exit(1);
    }

    // Setup downward shared memory, 100 is the size
    if ((dn_shm_id = shmget(DN_SHM_KEY, 400, IPC_CREAT | 0666)) < 0) {
    printf("Error getting shared memory id");
    exit(1);
    }
    // Attached shared memory
    if ((shared_memory_down = shmat(dn_shm_id, NULL, 0)) == (char *) -1) {
    printf("Error attaching shared memory id");
    exit(1);
    }

    simple_udp_register(&rssi_conn, RSS_PORT, NULL, RSS_PORT, rss_rx_callback);
    simple_udp_register(&data_conn, DAT_PORT, NULL, DAT_PORT, dp_rx_callback);
    simple_udp_register(&down_conn, DWN_PORT, NULL, DWN_PORT, NULL);

    PROCESS_END();
}
