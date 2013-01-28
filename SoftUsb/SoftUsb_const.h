#pragma once

#define MAGIC_NUMBER  42

#define PA 1
#define PB 2
#define PC 3
#define PD 4
#define PE 5
#define PF 6
#define PG 7
#define PH 8
#define PJ 10
#define PK 11
#define PL 12

#define REGISTER_CHECK 1
#define REGISTER_READ 2
#define REGISTER_WRITE 3
#define REGISTER_ADDRESS 4
#define REGISTER_SIZE 5

#define REGISTER_MISSING 111
#define REGISTER_OK 222


////////////////////////////////////////////
// const lists

#define DEFINE(x) (prog_uint16_t)(&x),
#define MISSING(x)
const prog_uint16_t reg_list[] PROGMEM =
{
#include "generated_registers.h"
};
#undef MISSING
#undef DEFINE

#define DEFINE(x) __COUNTER__,
#define MISSING(x)    (0*__COUNTER__)+
const prog_uint16_t reg_index_list[] PROGMEM =
{
#include "generated_registers.h"
    0
};
#undef MISSING
#undef DEFINE

#define DEFINE(x)    sizeof(x),
#define MISSING(x)
const prog_uint16_t sizeof_list[] PROGMEM =
{
#include "generated_registers.h"
};
#undef MISSING
#undef DEFINE

const int REG_COUNT = sizeof(sizeof_list);

#define DEFINE(x)    x,
const prog_uint32_t intdef_list[] PROGMEM =
{
#include "generated_intdefs.h"
};
#undef DEFINE
