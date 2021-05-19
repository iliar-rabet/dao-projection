#include "project-conf.h"
#include "contiki.h"
#include "simple-udp.h"
#include "sys/log.h"

#include <stdio.h>
#include <string.h>

#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_INFO

#define DP_PORT	4568

static struct simple_udp_connection udp_conn;

PROCESS(rec_example_process, "UDP REC example process");
AUTOSTART_PROCESSES(&rec_example_process);

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
  printf("received %s\n",data);
}

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(rec_example_process, ev, data)
{
 
  PROCESS_BEGIN();
  /* Initialize UDP connection */
  simple_udp_register(&udp_conn, DP_PORT, NULL,
                      DP_PORT, receiver);

  PROCESS_END();
}
