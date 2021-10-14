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

#include<stdlib.h>

#include <stdio.h>
#include <string.h>
#undef UIP_CONF_TCP
#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_INFO

#define START 300
#define CTR_PORT 4569
#define WITH_SERVER_REPLY  1
#define DP_PORT	5678


#define SEND_INTERVAL CLOCK_SECOND
#define CTRL_INTERVAL (CLOCK_SECOND*0.5)


static struct simple_udp_connection broadcast_connection;

#define DATA_INTERVAL (CLOCK_SECOND)

static struct simple_udp_connection udp_conn;
static uip_ipaddr_t rcvd_ip;
static bool ctrl_wdw=false;
//static char seq_no[2];
//static char old_seq_no[2] = "\0\0";
const char *string = "Mobile Node Neighbor Table";



/*---------------------------------------------------------------------------*/
PROCESS(udp_client_process, "UDP client");
AUTOSTART_PROCESSES(&udp_client_process);


/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_client_process, ev, data)
{
  static struct etimer data_timer;
  static struct etimer polling_timer;
  static struct etimer init_timer2;

  static unsigned count;
  static char str[150];
  uip_ipaddr_t dest_ipaddr;
  
  PROCESS_BEGIN();

  /* Initialize UDP connection */
  simple_udp_register(&udp_conn, DP_PORT, NULL,
                      DP_PORT, NULL);

  etimer_set(&init_timer2, START* CLOCK_SECOND);
  PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&init_timer2));

  etimer_set(&data_timer, DATA_INTERVAL);


  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&data_timer));
    // int reachable=NETSTACK_ROUTING.node_is_reachable();
    
    uip_ds6_addr_t *my_addr;
    char src[100];
    my_addr = uip_ds6_get_link_local(ADDR_PREFERRED);
    LOG_INFO_6ADDR(my_addr);
    uiplib_ipaddr_snprint(src, sizeof(src), my_addr);
    
    printf("start send %d\n",count+1);    
   
    int root_ip=NETSTACK_ROUTING.get_root_ipaddr(&dest_ipaddr);
    if(root_ip) {
      count++;
      snprintf(str, sizeof(str), "hello %d from %s", count,src);
      printf("now sending %s\n",str);    
      // uip_create_linklocal_allnodes_mcast(&dest_ipaddr);
      simple_udp_sendto(&udp_conn, str, sizeof(str), &dest_ipaddr);  
   
    }
      
    etimer_set(&data_timer, DATA_INTERVAL);
  }

  PROCESS_END();
}