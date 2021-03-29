// #include "../../arch/dev/cc2420/cc2420.h"
// #include "../../arch/dev/cc2420/cc2420_const.h"
#include "contiki.h"
#include "net/ipv6/uiplib.h"
#include "simple-udp.h"

//#include <stdio.h> /* For printf() */

/*---------------------------------------------------------------------------*/
PROCESS(hello_world_process, "Hello world process");
AUTOSTART_PROCESSES(&hello_world_process);

static struct simple_udp_connection udp_conn;
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(hello_world_process, ev, data)
{
  // static struct etimer timer;
  // char str[100];
  // uip_ipaddr_t dest_ipaddr;

  // PROCESS_BEGIN();
  
  // simple_udp_register(&udp_conn, 4569, NULL,
  //                   4569, NULL);

  // uint count=0;
  // /* Setup a periodic timer that expires after 10 seconds. */
  // etimer_set(&timer, CLOCK_SECOND * 0.1);
  // setreg(CC2420_MANOR,0x0100);

  // while(1) {
  //   // printf("Sending UNMODULATED %u to \n", count);
    
  //   snprintf(str, sizeof(str), "hello %d", count);
  //     uip_create_linklocal_allnodes_mcast(&dest_ipaddr);
  //     simple_udp_sendto(&udp_conn, str, sizeof(str), &dest_ipaddr);  

  //   /* Wait for the periodic timer to expire and then restart the timer. */
  //   PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&timer));
  //   etimer_reset(&timer);
  //   count++;
  // }

  // PROCESS_END();
}
/*---------------------------------------------------------------------------*/
