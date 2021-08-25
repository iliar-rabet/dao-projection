#include "contiki.h"
#include "project-conf.h"
#include "simple-udp.h"
#include "lib/random.h"
#include "net/ipv6/uip.h"
#include "net/ipv6/uip-ds6.h"
#include "net/ipv6/sicslowpan.h"
#include "net/ipv6/uiplib.h"
#include "net/routing/routing.h"
#include "net/routing/rpl-lite/rpl-timers.h"
#include "sys/etimer.h"
#include "sys/log.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>


#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_INFO
#undef UIP_CONF_TCP

#define UP_DAT_MN_PT 4567
#define UP_DAT_AN_PT 4568
#define UP_RSS_MN_PT 4569
#define DN_CTL_BR_PT 5678
#define UP_RSS_AN_PT 8765

static struct simple_udp_connection dn_ctl_br_conn, up_rss_mn_conn, up_rss_an_conn, up_dat_mn_conn, up_dat_an_conn;
static uip_ipaddr_t dest_ipaddr;
static char mobile_ip_addr[21];
static int handoff_flag=0;
/*--------------------------Linked List -- LL -------------------------------*/
struct node {
  char *mob_addr;
  struct node* next;
};

static struct node* LL_head = NULL;

static void
LL_append(struct node** head_ref, const char *new_addr)
{
  struct node *new_node = (struct node*) malloc(sizeof(struct node)), *last = *head_ref;
  new_node->mob_addr = (char *) malloc(21 * sizeof(char));

  strcpy(new_node->mob_addr, (const char *) new_addr);
  new_node->next = NULL;
  if (*head_ref == NULL) {
    *head_ref = new_node;
    return;
  }
  while (last->next != NULL)
    last = last->next;
  last->next = new_node;
  return;
}

static int
LL_del_srch_node(int opt, struct node** head_ref, const char *key)
{
  struct node *temp = *head_ref, *prev = NULL;
  /* opt = 0 for search the node
           1 for delete the node
     ret = 0 if node not in list
           1 if node is  in list
           2   delete is success
  */
  if (temp != NULL && !strcmp(temp->mob_addr, key)) {
    if (opt) {
      *head_ref = temp->next;
      memset(temp->mob_addr, '\0', 21 * sizeof(char));
      free(temp->mob_addr);
      free(temp);
      return 2;
    }
    return 1;
  }
  while (temp != NULL && strcmp(temp->mob_addr, key)) {
    prev = temp;
    temp = temp->next;
  }
  if (temp == NULL)
    return 0;

  if (opt) {
    prev->next = temp->next;
    memset(temp->mob_addr, '\0', 21 * sizeof(char));
    free(temp->mob_addr);
    free(temp);
    return 2;
  }
  return 1;
}
/*--------------------------Callback functions-------------------------------*/
static char str[100];
static void ctimer_callback() {
    
    if(NETSTACK_ROUTING.node_is_reachable() && NETSTACK_ROUTING.get_root_ipaddr(&dest_ipaddr))
    // Flags in message sent: R = RSSI F = From or source T = Time
    simple_udp_sendto(&up_rss_an_conn, str, strlen(str), &dest_ipaddr);

}

static void
rss_callback(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
  char src[21], time[4];
  int i;
  static struct ctimer cong_timer;

  memset(mobile_ip_addr, '\0', 21 * sizeof(char));
  uiplib_ipaddr_snprint(mobile_ip_addr, 21, sender_addr);
  if(LL_del_srch_node(0, &LL_head, (const char *) mobile_ip_addr)) {
    /* Anchor node is already parent of mobile node not sending RSS value
    */
    return;
  }
  
  for(i = 0; i < 3; i++) {
    time[i] = *data;
    data++;
  }
  time[3]='\0';

  uiplib_ipaddr_snprint(src, sizeof(src), sender_addr);
  snprintf(str, sizeof(str), "r %d f %s t %s", sicslowpan_get_last_rssi(), src, time);
  printf("str: %s\n", str);
  

  int cong_wait=random_rand()%5;
  printf("rand %d\n",cong_wait);

  etimer_set(&cong_timer, cong_wait);
  
  ctimer_set(&cong_timer, cong_wait, ctimer_callback, NULL);

  
  return;
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
  printf("Received response: %s\n", data);
  if ((int) *data == 'S') {
    data += 4;
    LL_append(&LL_head, (const char *) data);
    handoff_flag=0;
    printf("NOW BEING BEST\n", data);
  } else if ((int) *data == 'N') {
    data += 4;
    LL_del_srch_node(1, &LL_head, (const char *) data);
  }
  return;
}

static void
data_relay(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
  memset(mobile_ip_addr, '\0', 21 * sizeof(char));
  uiplib_ipaddr_snprint(mobile_ip_addr, 21, sender_addr);

  if(LL_del_srch_node(0, &LL_head, (const char *) mobile_ip_addr)) {
    if(sicslowpan_get_last_rssi()<-91 && handoff_flag==0){
      printf("HANDOFF STARTED\n");
      handoff_flag=1;
    }
    simple_udp_sendto(&up_dat_an_conn, data, strlen(data), &dest_ipaddr);
    printf("relaying\n");
  }
  else{
    printf("NOT relaying\n");
  }
  return;
}
/*---------------------------Contiki Process---------------------------------*/
PROCESS(sdmob_anchor_node_process, "SD-MOB anchor node process");
AUTOSTART_PROCESSES(&sdmob_anchor_node_process);



PROCESS_THREAD(sdmob_anchor_node_process, ev, data)
{

  PROCESS_BEGIN();
  simple_udp_register(&up_rss_an_conn, UP_RSS_AN_PT,
                      NULL, UP_RSS_AN_PT, NULL);

  simple_udp_register(&up_rss_mn_conn, UP_RSS_MN_PT, NULL,
                      UP_RSS_MN_PT, rss_callback);                      
  
  simple_udp_register(&dn_ctl_br_conn, DN_CTL_BR_PT, NULL,
                      DN_CTL_BR_PT, downward_callback);  

  simple_udp_register(&up_dat_mn_conn, UP_DAT_MN_PT, NULL,
                      UP_DAT_MN_PT, data_relay);

  simple_udp_register(&up_dat_an_conn, UP_DAT_AN_PT, NULL,
                      UP_DAT_AN_PT, NULL);
  
  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
