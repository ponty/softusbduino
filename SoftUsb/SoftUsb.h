#pragma once

#include "UsbMain.h"
#include <avr/version.h>
#include <avr/wdt.h>
#include <avr/interrupt.h>  /* for sei() */
#include <util/delay.h>     /* for _delay_ms() */
#include <avr/pgmspace.h>
#include "generated_version.h"

#if defined(ARDUINO) && ARDUINO >= 100
# include "Arduino.h"
#else
# include "WProgram.h"
# include "pins_arduino.h"
#endif

#include "SoftUsb.h"
#include "generated_mcu.h"

#ifdef OneWire_h
#define HAS_ONE_WIRE  1
#else
#define HAS_ONE_WIRE  0
#endif

#define MAGIC_NUMBER  42

#define _STR(s) #s
#define STR(s) _STR(s)

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
#define REGISTER_MISSING 111
#define REGISTER_OK 222

#define BUFFER_SIZE  20

#define TYPE_INT8   1
#define TYPE_INT16  2
#define TYPE_INT32  3
#define TYPE_STRING 4
#define TYPE_FLOAT  5
#define TYPE_VOID   6
#define TYPE_BYTE_ARRAY  7

#ifndef ONEWIRE_BUS_COUNT
#define ONEWIRE_BUS_COUNT  10
#endif

static uchar dataBuffer[BUFFER_SIZE]; /* buffer must stay valid when usbFunctionSetup returns */
usbMsgLen_t return_string(const char* s)
{
	dataBuffer[0] = TYPE_STRING;
	strcpy((char*) &dataBuffer[1], s);
	return strlen((char*) dataBuffer) + 1;
}

usbMsgLen_t return_byte_array(const byte* arr, int8_t size)
{
	dataBuffer[0] = TYPE_BYTE_ARRAY;
	for (int i = 0; i < size; i++)
	{
		dataBuffer[i + 1] = arr[i];
	}
	return size + 1;
}

usbMsgLen_t return_int8(int8_t x)
{
	dataBuffer[0] = TYPE_INT8;
	dataBuffer[1] = x;
	return 2;
}

usbMsgLen_t return_bool(int8_t x)
{
	return return_int8(x);
}

usbMsgLen_t return_int16(int16_t x)
{
	dataBuffer[0] = TYPE_INT16;
	dataBuffer[1] = x >> (0 * 8);
	dataBuffer[2] = x >> (1 * 8);
	return 3;
}

usbMsgLen_t return_int32(int32_t x)
{
	dataBuffer[0] = TYPE_INT32;
	dataBuffer[1] = x >> (0 * 8);
	dataBuffer[2] = x >> (1 * 8);
	dataBuffer[3] = x >> (2 * 8);
	dataBuffer[4] = x >> (3 * 8);
	return 5;
}

bool g_wdt_auto_reset = true;

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

#define DEFINE(x)    x,
const prog_uint32_t intdef_list[] PROGMEM =
{
#include "generated_intdefs.h"
};
#undef DEFINE

void * operator new(size_t size)
{
	return malloc(size);
}

void operator delete(void * ptr)
{
	free(ptr);
}


#ifdef OneWire_h
OneWire* one_wire_bus_list[ONEWIRE_BUS_COUNT]=
{	NULL};
uint8_t one_wire_address[8];
#endif

bool run_slow = false;
int slow_return;

typedef struct params
{
	byte cmd;
	uchar bytes[4];
	word word1;
} params_t;

params_t slow_params;

void delay_test(params_t* p)
{
	if (p->bytes[0])
		noInterrupts();

	if (p->bytes[1])
		delay(p->word1);
	else
		delayMicroseconds(p->word1);

	if (p->bytes[0])
		interrupts();
}

void usbReconnect()
{
	usbDeviceDisconnect();
	uchar i;
	i = 0;
	while (--i)
	{ /* fake USB disconnect for > 250 ms */
		_delay_ms(1);
	}
	usbDeviceConnect();
}

usbMsgLen_t SoftUsb_UsbFunctionSetup(uchar data[8])
{
	wdt_reset();

	usbRequest_t *rq = (usbRequest_t*) ((void *) data);
	byte cmd = rq->bRequest;

	params_t params;
	params.cmd = rq->bRequest;
	params.bytes[0] = rq->wValue.bytes[0];
	params.bytes[1] = rq->wValue.bytes[1];
	params.bytes[2] = rq->wIndex.bytes[0];
	params.bytes[3] = rq->wIndex.bytes[1];
	params.word1 = rq->wIndex.word; // same as (params.bytes[2];params.bytes[3])

	if ((rq->bmRequestType & USBRQ_TYPE_MASK) == USBRQ_TYPE_VENDOR)
	{
		usbMsgPtr = dataBuffer; /* tell the driver which data to return */
		switch (cmd)
		{
		case 10:
			digitalWrite(params.bytes[0], params.bytes[1]);
			break;

		case 11:
			pinMode(params.bytes[0], params.bytes[1]);
			break;

		case 12:
			analogWrite(params.bytes[0], params.bytes[1]);
			break;

		case 13:
			return return_int8(digitalRead(params.bytes[0]));
			break;

		case 14:
			analogReference(params.bytes[0]);
			break;

		case 22:
			return return_string(__TIME__);
			break;
		case 23:
			return return_string(__DATE__);
			break;

		case 24:
			return return_string(__VERSION__);
			break;

		case 25:
			return return_string(STR(USBDRV_VERSION));
			break;

		case 26:
			return return_string(MCU_DEFINED);
			break;

		case 27:
			return return_int16(analogRead(params.bytes[0]));
			break;

		case 29:
			return return_int8(digitalPinToBitMask(params.bytes[0]));
			break;

		case 30:
			return return_int8(digitalPinToPort(params.bytes[0]));
			break;

		case 31:
			return return_int8(*portModeRegister(params.bytes[0]));
			break;

		case 34:
			return return_int8(USB_CONCAT_EXPANDED(P, USB_CFG_IOPORTNAME));
			break;
		case 36:
			return return_int8(digitalPinToTimer(params.bytes[0]));
			break;
		case 37:
			return return_int8(analogInPinToBit(params.bytes[0]));
			break;
		case 38:
			return return_int8(*portOutputRegister(params.bytes[0]));
			break;
		case 39:
			return return_int8(*portInputRegister(params.bytes[0]));
			break;

		case MAGIC_NUMBER://42
			return return_int8(MAGIC_NUMBER);
			break;

		case 50:
		{
			word w = 0;
			for (unsigned int i = 0; i < sizeof(reg_index_list); i++)
			{
				word index = pgm_read_word(&reg_index_list[i]);
				if (index == params.word1)
				{
					w = pgm_read_word(&reg_list[i]);
					break;
				}
				if (index > params.word1)
					break;
			}
			if (w == 0)
			{
				// register not found
				switch (params.bytes[0])
				{
				case REGISTER_CHECK:
					return return_int8(REGISTER_MISSING);
					break;
				default:
					return 0;
				}
			}

			volatile byte* preg = (volatile byte*) w;
			switch (params.bytes[0])
			{
			case REGISTER_WRITE:
				*preg = params.bytes[1];
				break;
			case REGISTER_READ:
				return return_int8(*preg);
				break;
			case REGISTER_CHECK:
				return return_int8(REGISTER_OK);
				break;
			case REGISTER_ADDRESS:
				return return_int16((int16_t) preg);
				break;
			}
		}
			break;

		case 51:
		{
			uint32_t w = pgm_read_dword(&intdef_list[params.bytes[0]]);
			return return_int32(w);
		}
			break;

#ifdef OneWire_h

		case 62:
			if (one_wire_bus_list[params.bytes[0]])
			{
				delete one_wire_bus_list[params.bytes[0]];
			}
			one_wire_bus_list[params.bytes[0]] = new OneWire(params.bytes[1]);
			break;

		case 64:
			one_wire_bus_list[params.bytes[0]]->reset_search();
			break;

		case 65:
			slow_params = params;
			run_slow = true;
			break;

		case 66:
			slow_params = params;
			run_slow = true;
			break;

		case 67:
			slow_params = params;
			run_slow = true;
			break;

		case 68:
			slow_params = params;
			run_slow = true;
			break;

		case 69:
			one_wire_bus_list[params.bytes[0]]->depower();
			break;

		case 70:
			return return_byte_array(one_wire_address, 8);
			break;

		case 71:
			one_wire_address[0] = params.bytes[0];
			one_wire_address[1] = params.bytes[1];
			one_wire_address[2] = params.bytes[2];
			one_wire_address[3] = params.bytes[3];
			break;

		case 72:
			one_wire_address[4] = params.bytes[0];
			one_wire_address[5] = params.bytes[1];
			one_wire_address[6] = params.bytes[2];
			one_wire_address[7] = params.bytes[3];
			break;

		case 73:
			slow_params = params;
			run_slow = true;
			break;

#endif
		case 80:
			slow_params = params;
			run_slow = true;
			break;

		case 81:
			wdt_reset();
			break;

		case 82:
			wdt_enable( params.bytes[0] );
			break;

		case 83:
			wdt_disable();
			break;

		case 84:
			g_wdt_auto_reset = params.bytes[0];
			break;

		case 200:
		{
			return slow_return;
			break;
		}

		case 210:
		{
			delay_test(&params);
			break;
		}
		case 211:
			slow_params = params;
			run_slow = true;
			break;
		}
	}
	else
	{
		/* class requests USBRQ_HID_GET_REPORT and USBRQ_HID_SET_REPORT are
		 * not implemented since we never call them. The operating system
		 * won't call them either because our descriptor defines no meaning.
		 */
	}

	return 0; /* default for not implemented requests: return no data back to host */
}

class SoftUsb
{
private:

public:
	SoftUsb()
	{
		pUsbFunctionSetup = &SoftUsb_UsbFunctionSetup;
	}

	void begin()
	{
		// disable timer 0 overflow interrupt (used for millis)

		// TODO: make this portable
#if defined( TIMSK0 )
		TIMSK0 &= !(1 << TOIE0);
#elif defined( TIMSK )
		TIMSK &= !(1 << TOIE0);
#endif


		cli();

//		  wdt_reset();
//		  WDTCSR = _BV(WDIF) | _BV(WDIE) | _BV(WDCE) | _BV(WDE) | WDTO_1S;
		  /* The tricky part is that the next line *must* have both,
		   * WDCE and WDE cleared. */
//		  WDTCSR = _BV(WDIF) | _BV(WDIE) | WDTO_1S;
//		  MCUSR = 0;

		wdt_enable( WDTO_1S);
		/* Even if you don't use the watchdog, turn it off here. On newer devices,
		 * the status of the watchdog (on/off, period) is PRESERVED OVER RESET!
		 */
		/* RESET status: all port bits are inputs without pull-up.
		 * That's the way we need D+ and D-. Therefore we don't need any
		 * additional hardware initialization.
		 */
		usbInit();

		usbReconnect();

//		WDTCSR &= ~(1<<WDIE);
//		WDTCSR &= ~(1<<WDE);
//		wdt_disable();
		sei();
	}

	/* This function must be called at regular intervals from the main loop.
	 * Maximum delay between calls is somewhat less than 50ms (USB timeout for
	 * accepting a Setup message). Otherwise the device will not be recognized.
	 */
	void refresh()
	{
		if (g_wdt_auto_reset)
			wdt_reset();
//		WDTCSR &= ~(1<<WDIE);
//		WDTCSR &= ~(1<<WDE);

		if (run_slow)
		{
			run_slow = false;

			usbPoll();

			uchar i = 10;
			while (--i)
			{
				_delay_ms(1);
				usbPoll();
			}

			switch (slow_params.cmd)
			{
#ifdef OneWire_h
			case 65:
			{
				uint8_t ok = one_wire_bus_list[slow_params.bytes[0]]->search(
						one_wire_address);
				slow_return = return_bool(ok);
			}
			case 66:
				slow_return = return_bool(
						one_wire_bus_list[slow_params.bytes[0]]->reset());
				break;
			case 67:
				one_wire_bus_list[slow_params.bytes[0]]->select(
						one_wire_address);
				break;
			case 68:
				one_wire_bus_list[slow_params.bytes[0]]->write(
						slow_params.bytes[1], slow_params.bytes[2]);
				break;

			case 73:
				slow_return = return_int8(
						one_wire_bus_list[slow_params.bytes[0]]->read());
				break;
#endif
			case 80:
				cli();
				usbReconnect();
				sei();
				break;

			case 211:
				delay_test(&slow_params);
				break;
			}
		}

		usbPoll();
	}
};

//ISR(WDT_vect)
//{
//	cli();
//	usbReconnect();
//	sei();
//};
