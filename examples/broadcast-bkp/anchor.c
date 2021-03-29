/*
 * Copyright (c) 2011, Swedish Institute of Computer Science.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * This file is part of the Contiki operating system.
 *
 */
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
#define LOG_LEVEL LOG_LEVEL_DBG

#define UDP_PORT 1234

#define WITH_SERVER_REPLY  1
#define anchor_server_rssi	8765
#define anchor_server_ctrl	5678
#define anchor_MN_DATA 4567
#define anchor_server_DATA 4568
#define anchor_MN_rssi 4569
#define DATA_PORT 4567

#define SEND_INTERVAL		(20 * CLOCK_SECOND)
#define SEND_TIME		(random_rand() % (SEND_INTERVAL))
static struct simple_udp_connection broadcast_connection;
static struct simple_udp_connection udp_conn;
static struct simple_udp_connection data_conn;
uip_ipaddr_t mobile_ip_addr;
static bool best=false;
/*---------------------------------------------------------------------------*/
PROCESS(broadcast_example_process, "UDP broadcast example process");
AUTOSTART_PROCESSES(&broadcast_example_process);
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
  static char src[21];
    uip_ipaddr_t dest_ipaddr;
    static char str[100];
      static char time[4];
      static char p_parent[21];
    
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
    printf("last_rssi %d from %s at %s\n",sicslowpan_get_last_rssi(),src,time);
      //if(sicslowpan_get_last_rssi() < -60) {
      //    printf("Mobile node leaving coverage at %s\n", time);
      //}

  

    if(NETSTACK_ROUTING.node_is_reachable() && NETSTACK_ROUTING.get_root_ipaddr(&dest_ipaddr)) {
          // Flags in message sent: R = RSSI F = From or source T = Time P = current parent of the mobile node
      snprintf(str, sizeof(str), "R %d F %s T %s P %s", sicslowpan_get_last_rssi(), src, time, p_parent);
          printf("str: %s\n", str);
      simple_udp_sendto(&udp_conn, str, strlen(str), &dest_ipaddr);
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
receiverMobileSend(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
    //printf("\n\n%s\n\n", data);
    // rpl_neighbor_print_list("Anchor's table when relaying downward");
    char buf[40];
    // uip_ipaddr_t addr;

    LOG_INFO("Received response\n");// %c%c       ", seq_no[0], seq_no[1]);
		strcpy(buf,replace_str((char *)data,"::",":0:0:0:"));
    uip_ipaddr_t rcvd_ip;
    if(strcmp(buf,"STOP")){
      printf("STOOOOOOOOOOOOOOOOOOOOOOOOOOP\n");
      best=false; 
      // printf("Not Best anymore\n");      
    }
		if(!uiplib_ip6addrconv(buf, &rcvd_ip)) return;
		// Logging received IP address
		LOG_INFO_6ADDR(&rcvd_ip);
    LOG_INFO_6ADDR(rpl_get_global_address());
    if (compare(rpl_get_global_address(),&rcvd_ip)){
      best=true; 
      printf("NOW BEING BEST\n");
    }
    else{
      best=false; 
      printf("Not Best anymore\n");
      // uip_ipaddr_t new_parent;
      // uip_create_linklocal_allnodes_mcast(&new_parent);
      // simple_udp_sendto(&udp_conn, data, sizeof(data), &new_parent);  
    }

    // uip_gethostaddr(&addr);
    // int cmp;
    // cmp=uip_ip4addr_cmp(&rcvd_ip,&addr);
    // if(cmp==0)
    //   best=1;
  // simple_udp_sendto(&broadcast_connection, data, datalen, &mobile_ip_addr);
  
}


static void
dataCallback(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
  if(best==0){
     printf("not best\n");
     return; //anchor only relays the packet to root if it has received the 
  }
  printf("relaying %s\n",(char *)data);
  uip_ipaddr_t dest_ipaddr;
  NETSTACK_ROUTING.get_root_ipaddr(&dest_ipaddr);
  simple_udp_sendto(&data_conn, data, datalen, &dest_ipaddr);
}

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(broadcast_example_process, ev, data)
{
  static struct etimer periodic_timer;
  static struct etimer send_timer;
//  uip_ipaddr_t addr;

  PROCESS_BEGIN();

  simple_udp_register(&broadcast_connection, UDP_PORT,
                      NULL, UDP_PORT,
                      receiver);

  simple_udp_register(&udp_conn, UDP_CLIENT_PORT, NULL,
                      UDP_CLIENT_PORT, receiverMobileSend);                      

simple_udp_register(&data_conn, DATA_PORT, NULL,
                      DATA_PORT, dataCallback);

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
