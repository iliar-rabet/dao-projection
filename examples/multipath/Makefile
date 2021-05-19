CONTIKI_PROJECT = border-router-udp-server
all: $(CONTIKI_PROJECT)
CONTIKI = ../..

#CI = true

# The BR is either native or embedded, and in the latter case must support SLIP
PLATFORMS_EXCLUDE = nrf52dk z1

# Include RPL BR module
include $(CONTIKI)/Makefile.dir-variables
MODULES += $(CONTIKI_NG_SERVICES_DIR)/rpl-border-router
MODULES += os/services/shell

# Include webserver module
MODULES_REL += webserver
MODULES_REL += udpserver

# Include optional target-specific module
include $(CONTIKI)/Makefile.identify-target
MODULES_REL += $(TARGET)

CFLAGS += -Wno-unused-const-variable

CFLAGS += -Wno-stringop-truncation

LDFLAGS += -pthread  -lpthread -lm
include $(CONTIKI)/Makefile.include
