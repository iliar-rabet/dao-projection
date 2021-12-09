This repository serves as the implementation for the following papers:

[a link] https://github.com/iliar-rabet/dao-projection/SDMob.pdf
[a link] https://github.com/iliar-rabet/dao-projection/RPL-RP.pdf

To run the SDMob, you will need to install the mobility plugin for Cooja
[a link] https://anrg.usc.edu/contiki/index.php/Mobility_of_Nodes_in_Cooja

In the examples you will find, a bunch of *.csc files. For example, 3tlw.csc runs 3 mobile nodes based on Sky platform (broadcast/broadcast-example.c) moving by TLW mobility pattern - 1 slip radio (slip-radio/slip-radio.c) that connects the cooja environment to the external border router and 25 anchor nodes (anchor/anchor-downward-v0.c).

For the border router you can run the example "sock" in native mode (not in cooja but in linux) by the following command:

sudo ./border-router-udp-server.native fd00::1/64 -a 127.0.0.1

You can also run different versions of the filter using the python script named particle-v1.py using python3. Make sure to configure the script to have the same mobility trace file as given to the cooja mobility plugin.
-----------

To access the RPL-RP which is inspired by a IETF draft titled "DAO projection" that extends RPL (a low-power routing protocol for Internet of Things) [a link] https://datatracker.ietf.org/doc/draft-ietf-roll-dao-projection/. 
This project is based on Contiki-NG an open-source operating system. 

A screenshot of the dashboard (which is also aware of siblings) is demonstrated below:

![screenshot of the dashboard](https://github.com/iliar-rabet/dao-projection/blob/main/dashboard.png)

Knowing the topology we can install the routes as demonstrated in the demo [Video](https://youtu.be/pRlA1fBRYsc) .
