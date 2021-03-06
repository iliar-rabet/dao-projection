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

static struct simple_udp_connection flow_conn;
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

}
/*---------------------------------------------------------------------------*/

static
PT_THREAD(set_routes(struct httpd_state *s))
{

  PSOCK_BEGIN(&s->sout);
  SEND_STRING(&s->sout, TOP);
  SEND_STRING(&s->sout, "SENDING PDAO\n");
  SEND_STRING(&s->sout, BOTTOM);

  PSOCK_END(&s->sout);

}
/*---------------------------------------------------------------------------*/
static
PT_THREAD(generate_routes(struct httpd_state *s))
{
  static uip_ds6_nbr_t *nbr;

  PSOCK_BEGIN(&s->sout);
  SEND_STRING(&s->sout, TOP);


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

static FILE *fil;
static FILE *fp;

PROCESS(controller, "Controller");
PROCESS_THREAD(controller, ev, data)
{
  PROCESS_BEGIN();

  static struct etimer periodic_timer;
  
  char flow_src_str[30];
  char flow_dst_str[30];
  uip_ipaddr_t flow_dst_addr;
  uip_ipaddr_t flow_src_addr;
      char * line = NULL;
    size_t len = 0;
    ssize_t read;
    
    char via2_str[20];
    char via1_str[20];
    char dst_str[20];

    char track_egress_str[20];
    char track_ingress_str[20];
    uip_ipaddr_t track_egress_addr;
    uip_ipaddr_t track_ingress_addr;

    uip_ipaddr_t  dst_addr;
    uip_ipaddr_t  via1_addr;
    uip_ipaddr_t  via2_addr;
    int index;
    int interm_nodes;


  fil=fopen("flow.txt","r");
  if(fil==NULL)
  {
    printf("FILE not opened\n");
  }

  simple_udp_register(&flow_conn, 5678, NULL,
                      5678, NULL);
    
  etimer_set(&periodic_timer, 300 * CLOCK_SECOND);
  while(fscanf(fil,"%s to %s",flow_src_str,flow_dst_str)!=EOF) {

    printf("flow start: %s %s\n",flow_src_str,flow_dst_str);
    uiplib_ipaddrconv(flow_src_str,&flow_src_addr);
    uiplib_ipaddrconv(flow_dst_str,&flow_dst_addr);
    // LOG_INFO_6ADDR(&flow_dest_addr);
    
    simple_udp_sendto(&flow_conn, flow_dst_str, strlen(flow_dst_str), &flow_src_addr);

    simple_udp_sendto(&flow_conn, flow_dst_str, strlen(flow_dst_str), &flow_src_addr);

    fp=fopen("pdao.json", "r");
    while(fscanf(fp,"%s to %s %d",track_ingress_str,track_egress_str,&interm_nodes)>0){
      printf("%s %s--",track_egress_str,track_ingress_str);
      uiplib_ipaddrconv(track_egress_str,&track_egress_addr);
      uiplib_ipaddrconv(track_ingress_str,&track_ingress_addr);
      // LOG_INFO("interm nodes: %d\n",interm_nodes);
      // LOG_INFO_6ADDR(track_egress_addr);
    

      for(index=0;index<interm_nodes;index++){
        fscanf(fp,"%s via %s in %s",via2_str,via1_str,dst_str);
        // LOG_INFO("%s %s\n",dst_str,track_egress_str);
        if(uip_ipaddr_cmp(&flow_dst_addr,&track_egress_addr)){
          
          uiplib_ipaddrconv(dst_str,&dst_addr);
          uiplib_ipaddrconv(via2_str,&via2_addr);
          uiplib_ipaddrconv(via1_str,&via1_addr);
          // LOG_INFO_6ADDR(&via2_addr);
          // LOG_INFO_6ADDR(&via1_addr);
          // LOG_INFO_6ADDR(&dst_addr);

          rpl_icmp6_pdao_output(&dst_addr,&via1_addr,&via2_addr);
          // rpl_icmp6_pdao_output(&dst_addr,&via1_addr,&via2_addr);
        }
      }
    }
    fclose(fp);

    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));
    etimer_set(&periodic_timer, 30*CLOCK_SECOND);

  }
  fclose(fil);

  PROCESS_END();
}
