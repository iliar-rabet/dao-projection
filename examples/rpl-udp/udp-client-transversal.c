#include "contiki.h"
#include "net/routing/routing.h"
#include "random.h"
#include "net/netstack.h"
#include "net/ipv6/simple-udp.h"
#include "net/ipv6/uip.h"

#include "sys/log.h"
#include "sys/node-id.h"

#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_INFO

#define WITH_SERVER_REPLY  1
#define UDP_CLIENT_PORT	8765
#define FLOW_PORT	5678
// #define UDP_SERVER_PORT	5678

#define SEND_INTERVAL		  ( CLOCK_SECOND )

static struct simple_udp_connection udp_conn;
static struct simple_udp_connection flow_manager_conn;
int pdr_flag=0;


/*---------------------------------------------------------------------------*/
PROCESS(udp_client_process, "UDP client");
AUTOSTART_PROCESSES(&udp_client_process);
/*---------------------------------------------------------------------------*/
static void
udp_rx_callback(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
  LOG_INFO("Received '%.*s' from ", datalen, (char *) data);
  LOG_INFO_6ADDR(sender_addr);
  LOG_INFO(" in ");
  LOG_INFO_6ADDR(receiver_addr);
  LOG_INFO_("\n");
}

uip_ipaddr_t dest_ipaddr;
int flag=0;

static void
flow_manager_callback(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
  
  uint8_t lifetime;
  lifetime=0;

  LOG_INFO("Starting Flow '%.*s' from ", datalen, (char *) data);
  LOG_INFO_6ADDR(sender_addr);
  LOG_INFO_("\n");


  uiplib_ip6addrconv((char *) data,&dest_ipaddr);
  rpl_icmp6_pdr_output(lifetime, &dest_ipaddr);
  flag=1;
}

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_client_process, ev, data)
{
  static struct etimer periodic_timer;
  static unsigned count;
  static char str[32];
  uip_ipaddr_t root_ipaddr;
  
  PROCESS_BEGIN();

  /* Initialize UDP connection */
  simple_udp_register(&udp_conn, UDP_CLIENT_PORT, NULL  ,
                      UDP_CLIENT_PORT, udp_rx_callback);

  simple_udp_register(&flow_manager_conn, FLOW_PORT, NULL,
                      FLOW_PORT, flow_manager_callback);

  etimer_set(&periodic_timer, random_rand() % SEND_INTERVAL);
  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));

    if(NETSTACK_ROUTING.node_is_reachable() && NETSTACK_ROUTING.get_root_ipaddr(&root_ipaddr) && flag==1) {
       
      /* Send to DAG root */
      
      LOG_INFO("Sending %u to ", count);
      LOG_INFO_6ADDR(&dest_ipaddr);
      LOG_INFO_("\n");
      snprintf(str, sizeof(str), "hello %d", count);
      simple_udp_sendto(&udp_conn, str, strlen(str), &dest_ipaddr);
      count++;
    } 
    etimer_set(&periodic_timer, SEND_INTERVAL);
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
