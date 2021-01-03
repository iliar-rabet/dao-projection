/*
 * Copyright (c) 2017, RISE SICS
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

#include "contiki.h"
#include "net/routing/routing.h"
#include "net/ipv6/uip-ds6-nbr.h"
#include "net/ipv6/uip-ds6-route.h"
#include "net/ipv6/uip-sr.h"
#include "net/routing/rpl-lite/rpl-types.h"
#include "net/routing/rpl-lite/rpl-icmp6.h"

#include "sys/log.h"
#define LOG_MODULE "RPL BR"
#define LOG_LEVEL LOG_LEVEL_INFO



#include <stdio.h>
#include <string.h>

/*---------------------------------------------------------------------------*/
static const char *TOP = "";
static const char *BOTTOM = "";
static char buf[256];
static int blen;
#define ADD(...) do {                                                   \
    blen += snprintf(&buf[blen], sizeof(buf) - blen, __VA_ARGS__);      \
  } while(0)
#define SEND(s) do { \
  SEND_STRING(s, buf); \
  blen = 0; \
} while(0);

/* Use simple webserver with only one page for minimum footprint.
 * Multiple connections can result in interleaved tcp segments since
 * a single static buffer is used for all segments.
 */
#include "httpd-simple.h"

/*---------------------------------------------------------------------------*/
static void
ipaddr_add(const uip_ipaddr_t *addr)
{
  uint16_t a;
  int i, f;
  i=sizeof(uip_ipaddr_t)-2;
  a = (addr->u8[i] << 8) + addr->u8[i + 1];
  ADD("%x",a);
  // for(i = 0, f = 0; i < sizeof(uip_ipaddr_t); i += 2) {
  //   a = (addr->u8[i] << 8) + addr->u8[i + 1];
  //   if(a == 0 && f >= 0) {
  //     if(f++ == 0) {
  //       ADD("::");
  //     }
  //   } else {
  //     if(f > 0) {
  //       f = -1;
  //     } else if(i > 0) {
  //       ADD(":");
  //     }
  //     ADD("%x", a);
  //   }
  // }
}
/*---------------------------------------------------------------------------*/
static
PT_THREAD(set_routes(struct httpd_state *s))
{
  // FILE *fp;
  // char dst[20];
  // char via[20];
  // uip_ipaddr_t * dst_addr = malloc(sizeof(uip_ipaddr_t));
  // printf("Thread started\n");
  // fp=fopen("pdao.json", "r");

  // PSOCK_BEGIN(&s->sout);
  // SEND_STRING(&s->sout, "sending PDAO");

  // fscanf(fp,"%s via %s",dst,via);
  // printf(dst);
  // uiplib_ipaddrconv(dst,dst_addr);
  // printf(via);
  // fclose(fp);
  // LOG_INFO_6ADDR(dst_addr);
  // rpl_icmp6_pdao_output(dst_addr,100);

  // PSOCK_END(&s->sout);
}
/*---------------------------------------------------------------------------*/
static
PT_THREAD(generate_routes(struct httpd_state *s))
{
  static uip_ds6_nbr_t *nbr;

  PSOCK_BEGIN(&s->sout);
  SEND_STRING(&s->sout, TOP);

  // ADD("{\"nodes\": [\n");
  // SEND(&s->sout);
  // for(nbr = uip_ds6_nbr_head();
  //     nbr != NULL;
  //     nbr = uip_ds6_nbr_next(nbr)) {
  //   ADD("    {\"id\":\"");
  //   ipaddr_add(&nbr->ipaddr);
  //   ADD("\",\"group\":1}");
  //   if(uip_ds6_nbr_next(nbr)!=NULL)
  //     ADD(",");
  //   ADD("\n");
  //   SEND(&s->sout);
  // }
  // ADD("  ],\n");
  // SEND(&s->sout);

#if (UIP_MAX_ROUTES != 0)
  {
    static uip_ds6_route_t *r;
  ADD("{\"routes\": [\n");
    SEND(&s->sout);
    for(r = uip_ds6_route_head(); r != NULL; r = uip_ds6_route_next(r)) {
      ADD("    <li>");
      ipaddr_add(&r->ipaddr);
      ADD("/%u (via ", r->length);
      ipaddr_add(uip_ds6_route_nexthop(r));
      ADD(") %lus", (unsigned long)r->state.lifetime);
      ADD("</li>\n");
      SEND(&s->sout);
    }
    ADD("  </ul>\n");
    SEND(&s->sout);
  }
#endif /* UIP_MAX_ROUTES != 0 */

#if (UIP_SR_LINK_NUM != 0)
  if(uip_sr_num_nodes() > 0) {
    static uip_sr_node_t *link;
    ADD("{\"links\": [\n");
    SEND(&s->sout);
    for(link = uip_sr_node_head(); link != NULL; link = uip_sr_node_next(link)) {
      if(link->parent != NULL) {
        uip_ipaddr_t child_ipaddr;
        uip_ipaddr_t parent_ipaddr;

        NETSTACK_ROUTING.get_sr_node_ipaddr(&child_ipaddr, link);
        NETSTACK_ROUTING.get_sr_node_ipaddr(&parent_ipaddr, link->parent);

        ADD("{\"source\":\"");
        ipaddr_add(&child_ipaddr);

        ADD("\",\"target\":\"");
        ipaddr_add(&parent_ipaddr);
        // ADD("\", \"value\":%u", (unsigned int)link->lifetime);
        ADD("\", \"value\":1" );

        ADD("}");
        if(uip_sr_node_next(link)!=NULL)
          ADD(",");
        ADD("\n");
        SEND(&s->sout);
      }
    }
    ADD("  ]\n}");
    SEND(&s->sout);
  }
#endif /* UIP_SR_LINK_NUM != 0 */

  SEND_STRING(&s->sout, BOTTOM);

  PSOCK_END(&s->sout);
}
/*---------------------------------------------------------------------------*/
PROCESS(webserver_nogui_process, "Web server");
PROCESS_THREAD(webserver_nogui_process, ev, data)
{
  PROCESS_BEGIN();

  httpd_init();

  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(ev == tcpip_event);
    httpd_appcall(data);
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
httpd_simple_script_t
httpd_simple_get_script(const char *name)
{
  if(strcmp(name, "s") == 0) {
    return set_routes;
  }
  else
    return generate_routes;
}
/*---------------------------------------------------------------------------*/
PROCESS(controller, "Controller");
PROCESS_THREAD(controller, ev, data)
{
  PROCESS_BEGIN();

  static struct etimer periodic_timer;
  FILE *fp;
  char via2_str[20];
  char via1_str[20];
  char dst_str[20];


  etimer_set(&periodic_timer, CLOCK_SECOND);
  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));

  uip_ipaddr_t * dst_addr = malloc(sizeof(uip_ipaddr_t));
  uip_ipaddr_t * via1_addr = malloc(sizeof(uip_ipaddr_t));
  uip_ipaddr_t * via2_addr = malloc(sizeof(uip_ipaddr_t));
  printf("Thread started\n");
  fp=fopen("pdao.json", "r");
  while(fscanf(fp,"%s via %s in %s",via2_str,via1_str,dst_str)>0){
    
    uiplib_ipaddrconv(dst_str,dst_addr);
    uiplib_ipaddrconv(via2_str,via2_addr);
    uiplib_ipaddrconv(via1_str,via1_addr);
    
    LOG_INFO("SENDING to:");
    LOG_INFO_6ADDR(dst_addr);
    LOG_INFO("\n");
    rpl_icmp6_pdao_output(dst_addr,via1_addr,via2_addr);
  }
  fclose(fp);
  etimer_set(&periodic_timer, 10*CLOCK_SECOND);
  }

  PROCESS_END();
}
