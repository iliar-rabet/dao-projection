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


#include "net/ipv6/uiplib.h"
#include "net/routing/routing.h"
#include "net/netstack.h"
#include "net/ipv6/simple-udp.h"

#include "sys/log.h"
#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_DBG

#define WITH_SERVER_REPLY  1
#define RSS_PORT	8765
#define SOCKPORT 1234
#define DP_PORT	4568
#define DOWNWARD_PORT	5678
#define FIFO_FILE "MYFIFO"

int shmid;
// give your shared memory an id, anything will do
key_t key = 123456;
char *shared_memory;

// static uip_ipaddr_t old_parent;
static uip_ipaddr_t new_parent;

static struct simple_udp_connection rssi_conn;	
static struct simple_udp_connection data_conn;


static int fd, iter = 0;
static char str[100], buff[100], curr_parent[100];
// const char wait[4] = "WAIT";

//, reply_control, first_run_only_if_65 = 0;
//static char msg_cntr[2] = {0};
//   static int sock = 0; 
//   static struct sockaddr_in serv_addr; 
  static int totalRx=0;
  static int plist[500];
static void sum_list(){
    totalRx=0;
    for (int i=0;i<500;i++){
        if(plist[i]==1)
        totalRx=totalRx+1;
    }
}

void encoding(const uint8_t *data)
{
    //    Example data :
    //    R -59 F fe80::212:7402:2:202 T 41 P fe80::212:7403:3:303
    for (iter = 0; iter < 56; iter++) {
        if ( iter < 2 )
            str[iter] = str[18+iter]; //    Adding only the node ID to str
        else if ( iter < 5 ) {
            if ( iter == 2 )
                data += 2; // Removing 'R '
            str[iter] = (char) *data++; //    Adding RSSI to str
        }    else if ( iter == 5 ) {
            data += 22; // Removing ' F fe80::212:7402:2:20'
            str[iter] = (char) *data++; // Adding mobile ID to str
            data += 3; // Removing ' T '
        } else if ( iter < 9 )
                str[iter] = (char) *data++; // Adding time to str
        else if ( iter < 10 )
            str[iter] = ';';
        else
            str[iter] = '\0';
    }

    data += 3; // Removing ' P '

    if (((char) *data) == 'f') {
        memset(curr_parent, 0, 25 * (sizeof curr_parent[0]));
        for (iter = 0; iter < 20; iter++) 
            curr_parent[iter] = (char) *data++;
        curr_parent[20] = '\0';
    }
}

static struct ctimer read_timer;


PROCESS(udp_server_process, "UDP server");

/*---------------------------------------------------------------------------*/
// void read_pipe(){
// // Reading from named pipe for communication with python script
//     fd = open(FIFO_FILE_DOWN, O_RDONLY);
//     // Erasing buff everytime before reading
//     memset(buff, 0, 100 * (sizeof buff[0]));

//     if(read(fd, buff, sizeof(buff)))
//         // LOG_INFO("buff: %s\n", buff);
//         ;
		
//     printf("downward buf: %s\n",buff);
//     if(wait[0]==buff[0]&&wait[1]==buff[1]&&wait[2]==buff[2]&&wait[3]==buff[3]) {
//         printf("waiting\n");
//     }
//     else{
//         printf("trying to SEND BEST\n");
//         uip_create_linklocal_allnodes_mcast(&new_parent);//broadcast
//         simple_udp_sendto(&downward_conn, buff, sizeof(buff), &new_parent);  
//     }

//     close(fd);
// }


static void
rss_rx_callback(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
    LOG_INFO("Received request '%.*s' from ", datalen, (char *) data);
    LOG_INFO_6ADDR(sender_addr);
    LOG_INFO_("\n");
   
	
	// Erasing str everytime before reading
    memset(str, 0, 100 * (sizeof str[0]));

    uiplib_ipaddr_snprint(str, sizeof(str), sender_addr);
	// Data extraction
    printf("data:%s\n",data);
    encoding(data);
    printf("encoded data:%s\n",data);
    printf("str:%s\n",str);
    memcpy(shared_memory, str, strlen(str));
	// fd = open(FIFO_FILE, O_WRONLY);
	// int bullshit=write(fd, str, sizeof(str));
	// if(bullshit);
	// close(fd);
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
  // send(sock , str , strlen(str) , 0 ); 
  LOG_INFO("Received HELLO '%.*s' from ", datalen, (char *) data);
  int num=0;
  sscanf((char *)data,"hello %d",&num);
  printf("num: %d",num);
  plist[num]=1;
  // LOG_INFO_6ADDR(sender_addr);
  LOG_INFO_("\n");
//   totalRx++;
  sum_list();
  printf("totalRx=%d\n",totalRx);

//   printf("sender_addr: %s\n",(char *)sender_addr);

}


/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_server_process, ev, data)
{

	PROCESS_BEGIN();

	/* Create the FIFO if it does not exist */
	mkfifo(FIFO_FILE, 0666);
    // old_parent=NULL;

   // Setup shared memory, 400 is the size
   if ((shmid = shmget(key, 400, IPC_CREAT | 0666)) < 0)
   {
      printf("Error getting shared memory id");
      exit(1);
   }
   // Attached shared memory
   if ((shared_memory = shmat(shmid, NULL, 0)) == (char *) -1)
   {
      printf("Error attaching shared memory id");
      exit(1);
   }


	simple_udp_register(&rssi_conn, RSS_PORT, NULL,
						RSS_PORT, rss_rx_callback);
	simple_udp_register(&data_conn, DP_PORT, NULL,
						DP_PORT, dp_rx_callback);  

  PROCESS_END();
}
