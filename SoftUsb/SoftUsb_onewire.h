#pragma once

#ifdef OneWire_h
#define HAS_ONE_WIRE  1
#else
#define HAS_ONE_WIRE  0
#endif

#ifndef ONEWIRE_BUS_COUNT
#define ONEWIRE_BUS_COUNT  10
#endif


#ifdef OneWire_h
OneWire* one_wire_bus_list[ONEWIRE_BUS_COUNT]=
{   NULL};
uint8_t one_wire_address[8];
#endif
