#include "project-conf.h"
#include "contiki.h"
#include "lib/random.h"
#include "sys/ctimer.h"
#include "sys/etimer.h"
#include "net/ipv6/uip.h"
#include "net/ipv6/uip-ds6.h"
#include "net/routing/routing.h"
#include "simple-udp.h"
#include "net/ipv6/uiplib.h"
#include "sys/log.h"
#include "net/routing/rpl-lite/rpl-neighbor.h"
#include "net/routing/rpl-lite/rpl-dag.h"

#include "lib/trickle-timer.h"
#include "net/ipv6/uip-icmp6.h"
#include<stdlib.h>

#include <stdio.h>
#include <string.h>
#undef UIP_CONF_TCP
#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_INFO

#define CTR_PORT 4569
#define WITH_SERVER_REPLY  1
#define DP_PORT	4567


#define SEND_INTERVAL CLOCK_SECOND
#define CTRL_INTERVAL (CLOCK_SECOND*0.2)


static struct simple_udp_connection broadcast_connection;

#define DATA_INTERVAL (1.0*CLOCK_SECOND)

static struct simple_udp_connection udp_conn;
static uip_ipaddr_t rcvd_ip;
static bool ctrl_wdw=true;
//static char seq_no[2];
//static char old_seq_no[2] = "\0\0";
const char *string = "Mobile Node Neighbor Table";



/*---------------------------------------------------------------------------*/
PROCESS(broadcast_example_process, "UDP broadcast example process");
PROCESS(udp_client_process, "UDP client");
AUTOSTART_PROCESSES(&broadcast_example_process,&udp_client_process);

/*---------------------------------------------------------------------------*/
/*---------------------------------------------------------------------------*/
char *replace_str(char *str, char *orig, char *rep)
{
  static char buffer[100];
  char *p;

 

  if(!(p = strstr(str, orig)))  // Is 'orig' even in 'str'?
    return str;

 

  strncpy(buffer, str, p-str); // Copy characters from 'str' start to 'orig' string
  buffer[p-str] = '\0';

 

  sprintf(buffer+(p-str), "%s%s", rep, p+strlen(orig));
  //printf("rep:%s\n",buffer);
  return buffer;
}

int random(int min, int max){
    int number = min + rand() % (max - min);
    return number; 
}

/*---------------------------------------------------------------------------*/
static void
receiver(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
  char buf[100];

	//seq_no[0] = *data; data += 1; seq_no[1] = *data; data += 1;

	// Ignore duplicate messages
	//if(!((old_seq_no[0] == seq_no[0]) && (old_seq_no[1] == seq_no[1]))) {
		// LOG_INFO("Received response");// %c%c       ", seq_no[0], seq_no[1]);
		strcpy(buf,replace_str((char *)data,"::",":0:0:0:"));
		if(!uiplib_ip6addrconv(buf, &rcvd_ip)) return;
		// Logging received IP address
		// LOG_INFO_6ADDR(&rcvd_ip);
    
		// printf(" from ");
		// LOG_INFO_6ADDR(sender_addr);
		
		//if(rpl_neighbor_get_from_ipaddr(&rcvd_ip)) {
			//if(!rpl_neighbor_is_parent(rpl_neighbor_get_from_ipaddr(&rcvd_ip))) {
				// before parent change
		// rpl_neighbor_print_list(string);
        

        // printf("trickel: %d\n",TRICKLE_TIMER_INTERVAL_END(tt));
				// after parent change
        // uip_ipaddr_t dest_ipaddr;
        // NETSTACK_ROUTING.get_root_ipaddr(&dest_ipaddr);
				//   uip_icmp6_send(&dest_ipaddr, ICMP6_RPL, RPL_CODE_DAO, 4);
			//} else {
				//printf("\nIgnoring request to change to existing parent\n");
			//}
		//} else {
			//printf("\nReceived parent is not neighbour list\n");
		//}
		//old_seq_no[0] = seq_no[0]; old_seq_no[1] = seq_no[1];
		//seq_no[0] = seq_no[1] = '\0';
	//} else {
		//printf("\nIgnoring repeated copies\n");
  //} 
}
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(broadcast_example_process, ev, data)
{
  static struct etimer periodic_timer;
  static struct etimer wdw_timer;
  uip_ipaddr_t addr;
  static char str[4 + UIPLIB_IPV6_MAX_STR_LEN];
  // static char buf[UIPLIB_IPV6_MAX_STR_LEN];
  static uint8_t time = 0;

  PROCESS_BEGIN();
  
  simple_udp_register(&broadcast_connection, CTR_PORT,
                      NULL, CTR_PORT,
                      receiver);

  etimer_set(&periodic_timer, SEND_INTERVAL);
  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));
    etimer_reset(&periodic_timer);
    // uiplib_ipaddr_snprint(buf, sizeof(buf), rpl_neighbor_get_ipaddr(curr_instance.dag.preferred_parent));
        // if ( buf[1] == 'N' ) {
        snprintf(str, sizeof(str), "%03d", (time >= 999)? time = 1 : time++);
        // } else {
        //     snprintf(str, sizeof(str), "%03d %s", (time >= 999)? time = 1 : time++, buf);
        // }
    printf("Sending control broadcast: %s\n", str);


    ctrl_wdw=true;
    uip_create_linklocal_allnodes_mcast(&addr);
    simple_udp_sendto(&broadcast_connection, str, sizeof(str), &addr);
    etimer_set(&wdw_timer,CTRL_INTERVAL);
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&wdw_timer));
    ctrl_wdw=false;
  }
  
  PROCESS_END();
}

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_client_process, ev, data)
{
  static struct etimer data_timer;
  static struct etimer polling_timer;
  static unsigned count;
  static char str[150];
  uip_ipaddr_t dest_ipaddr;
  
  PROCESS_BEGIN();

  /* Initialize UDP connection */
  simple_udp_register(&udp_conn, DP_PORT, NULL,
                      DP_PORT, NULL);

  etimer_set(&data_timer, DATA_INTERVAL);
  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&data_timer));
    // int reachable=NETSTACK_ROUTING.node_is_reachable();
    
    
    printf("start send %d\n",count+1);    
    while(ctrl_wdw==true)
    {
      // printf("control_window\n");
      etimer_set(&polling_timer, CLOCK_SECOND*0.02);
      PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&polling_timer));
    }
    
    // int root_ip=NETSTACK_ROUTING.get_root_ipaddr(&dest_ipaddr);
    // if(root_ip) {
      count++;
      snprintf(str, sizeof(str), "hello %d  ", count);
      printf("now sending %s\n",str);    
      uip_create_linklocal_allnodes_mcast(&dest_ipaddr);
      simple_udp_sendto(&udp_conn, str, sizeof(str), &dest_ipaddr);  
    // }
    // else {
    //   printf("%d %d\n", NETSTACK_ROUTING.node_is_reachable(), NETSTACK_ROUTING.get_root_ipaddr(&dest_ipaddr));
    //   printf("could not send %d\n",count);
    //   // rpl_neighbor_print_list("could not send");
    //   // if(curr_instance.dag.preferred_parent) {
    //   //   LOG_INFO_6ADDR( rpl_neighbor_get_ipaddr(curr_instance.dag.preferred_parent));
    //   // } else {
    //   //   printf("None\n");
    //   // }
    // }
    etimer_set(&data_timer, DATA_INTERVAL);
  }

  PROCESS_END();
}