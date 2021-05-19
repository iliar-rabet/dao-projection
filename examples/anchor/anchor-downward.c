#include "project-conf.h"
#include "contiki.h"
#include "lib/random.h"
#include "sys/ctimer.h"
#include "sys/etimer.h"
#include "net/ipv6/uip.h"
#include "net/ipv6/uip-ds6.h"
#include "net/ipv6/sicslowpan.h"
#include "simple-udp.h"
#include "net/ipv6/uiplib.h"
#include "net/routing/routing.h"
#include "sys/log.h"

#include "net/ipv6/uip.h"
#include "net/routing/rpl-lite/rpl-timers.h"
#include "net/ipv6/uiplib.h"

#include <stdio.h>
#include <string.h>
#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_INFO
#undef UIP_CONF_TCP
#define UDP_PORT 1234

#define WITH_SERVER_REPLY  1
#define RSSI_RELAY	8765
#define DOWNWARD_PORT	5678
#define DATA_PORT 4567
#define DATA_RELAY_PORT 4568
#define RSSI_PORT 4569


#define SEND_INTERVAL		(20 * CLOCK_SECOND)
#define SEND_TIME		(random_rand() % (SEND_INTERVAL))
static struct simple_udp_connection downward_connection;
static struct simple_udp_connection rssi_MN_conn;
static struct simple_udp_connection rssi_anchor_conn;
static struct simple_udp_connection data_conn;
static struct simple_udp_connection data_relay_conn;
uip_ipaddr_t mobile_ip_addr;
static bool best=false;
static int handoff_flag=0;
/*---------------------------------------------------------------------------*/
PROCESS(broadcast_example_process, "UDP broadcast example process");
AUTOSTART_PROCESSES(&broadcast_example_process);
/*---------------------------------------------------------------------------*/
static void
rss_callback(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{

  static char src[21];
    uip_ipaddr_t dest_ipaddr;
    static char str[100];
      static char time[4];
      static char p_parent[21];
  
  if(best==true)
    return;    

    mobile_ip_addr = *sender_addr;

    int i;
    for(i = 0; i < 3; i++) {
        time[i] = *data;
        data++;
    }

    time[3]='\0';

    data++;
    for(i = 0; i < UIPLIB_IPV6_MAX_STR_LEN; i++) {
        p_parent[i] = *data;
        data++;
    }

    uiplib_ipaddr_snprint(src, sizeof(src), sender_addr);
    // printf("last_rssi %d from %s at %s\n",sicslowpan_get_last_rssi(),src,time);
      //if(sicslowpan_get_last_rssi() < -60) {
      //    printf("Mobile node leaving coverage at %s\n", time);
      //}

  
    snprintf(str, sizeof(str), "r %d f %s t %s p %s", sicslowpan_get_last_rssi(), src, time, p_parent);
    // printf("str: %s\n", str);
    if(NETSTACK_ROUTING.node_is_reachable() && NETSTACK_ROUTING.get_root_ipaddr(&dest_ipaddr)) {
          // Flags in message sent: R = RSSI F = From or source T = Time P = current parent of the mobile node
          simple_udp_sendto(&rssi_anchor_conn, str, strlen(str), &dest_ipaddr);
    }
  }
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

bool compare(const uip_ipaddr_t * first,uip_ipaddr_t * sec){
  bool ret = true;
  int i;
  for(i=0;i<8;i++){
    if(first->u16[i]!=sec->u16[i])
      ret=false;
  }
  return ret;
}
static void
downward_callback(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
    //printf("\n\n%s\n\n", data);
    // rpl_neighbor_print_list("Anchor's table when relaying downward");
    char buff[100];
    uip_ipaddr_t addr;
    printf("Received response: %s\n",data);// %c%c       ", seq_no[0], seq_no[1]);
    // strcpy(buf,replace_str((char *)data,"::",":0:0:0:"));
    sprintf(buff,"%s",data);
    uip_ipaddr_t rcvd_ip;
    // if(strcmp(buf,"STOP")){
    //   printf("STOOOOOOOOOOOOOOOOOOOOOOOOOOP\n");
    //   best=false; 
    // }
    char * buf=strtok(buff," ");
    char * time=strtok(NULL," ");
    // printf("time : %s\n",time);
    if(strstr(buf, "+") == NULL) {
        if(!uiplib_ip6addrconv(buf, &rcvd_ip)) return;
        // Logging received IP address
        // LOG_INFO_6ADDR(&rcvd_ip);
        // LOG_INFO_6ADDR(rpl_get_global_address());
        if (compare(rpl_get_global_address(),&rcvd_ip)){      
            best=true;
            printf("NOW BEING BEST time: %s\n",time);
            handoff_flag=0;
        }
        else{
            best=false; 
            // printf("Not Best anymore\n");
        }
    }
    else {
        char * token = strtok(buf, "+");
        // loop through the string to extract all other tokens
        // printf( "first part is: %s\n", token ); //printing each token
        if(!uiplib_ip6addrconv(token, &rcvd_ip)) return;
        // Logging received IP address
        // LOG_INFO_6ADDR(&rcvd_ip);
        // LOG_INFO_6ADDR(rpl_get_global_address());
        if (compare(rpl_get_global_address(),&rcvd_ip)){      
            token=strtok(NULL,"+");
            char tmp[90];
            sprintf(tmp,"%s %s",token,time);
            // printf( "second part is: %s\n", token); //printing each token
            uip_create_linklocal_allnodes_mcast(&addr);//broadcast
            simple_udp_sendto(&downward_connection, tmp, strlen(tmp), &addr);  
        }
    }
}


static void
dataRelay(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
  if(best==0){
    //  printf("not best\n");
     return; //anchor only relays the packet to root if it is assigned best
  }
  printf("relaying %s\n",(char *)data);
  uip_ipaddr_t dest_ipaddr;
  NETSTACK_ROUTING.get_root_ipaddr(&dest_ipaddr);
  if(sicslowpan_get_last_rssi()<-85 && handoff_flag==0){
    printf("HANDOFF STARTED\n");
    handoff_flag=1;
  }
  // uiplib_ipaddrconv("fd00::212:740c:c:c0c",&dest_ipaddr);
  // LOG_INFO("RELAYING TO:");
  // LOG_INFO_6ADDR(&dest_ipaddr);
  // LOG_INFO("\n");
  simple_udp_sendto(&data_relay_conn, data, datalen, &dest_ipaddr);
}

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(broadcast_example_process, ev, data)
{
  static struct etimer periodic_timer;
  static struct etimer send_timer;
//  uip_ipaddr_t addr;

  PROCESS_BEGIN();

  simple_udp_register(&rssi_anchor_conn, RSSI_RELAY,
                      NULL, RSSI_RELAY,
                      NULL);

  simple_udp_register(&rssi_MN_conn, RSSI_PORT, NULL,
                      RSSI_PORT, rss_callback);                      
  
  simple_udp_register(&downward_connection, DOWNWARD_PORT, NULL,
                      DOWNWARD_PORT, downward_callback);  

  simple_udp_register(&data_conn, DATA_PORT, NULL,
                      DATA_PORT, dataRelay);

  simple_udp_register(&data_relay_conn, DATA_RELAY_PORT, NULL,
                      DATA_RELAY_PORT, NULL);

  etimer_set(&periodic_timer, SEND_INTERVAL);
  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));
    etimer_reset(&periodic_timer);
    etimer_set(&send_timer, SEND_TIME);

    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&send_timer));
//    printf("Sending broadcast\n");
//    uip_create_linklocal_allnodes_mcast(&addr);
 //   simple_udp_sendto(&broadcast_connection, "Test", 4, &addr);
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
