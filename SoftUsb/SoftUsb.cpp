#include <avr/version.h>
#include <avr/wdt.h>
#include <avr/interrupt.h>  /* for sei() */
#include <util/delay.h>     /* for _delay_ms() */
#include <avr/pgmspace.h>
#include "usbdrv.h"
#include "generated_version.h"

#if defined(ARDUINO) && ARDUINO >= 100
# include "Arduino.h"
#else
# include "WProgram.h"
#endif

#include "SoftUsb.h"
#include "UsbMain.h"
#include "generated_mcu.h"
#include "pins_arduino.h"

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

static uchar dataBuffer[BUFFER_SIZE]; /* buffer must stay valid when usbFunctionSetup returns */
usbMsgLen_t return_string(const char* s)
{
	dataBuffer[0] = TYPE_STRING;
	strcpy((char*) &dataBuffer[1], s);
	return strlen((char*) dataBuffer)+1;
}

usbMsgLen_t return_int8(int8_t x)
{
	dataBuffer[0] = TYPE_INT8;
	dataBuffer[1] = x;
	return 2;
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
//#define MISSING(x)   0,
const prog_uint32_t intdef_list[] PROGMEM =
{
#include "generated_intdefs.h"
};
//#undef MISSING
#undef DEFINE

usbMsgLen_t SoftUsb_UsbFunctionSetup(uchar data[8])
{
	//usbMsgLen_t return_value;
	usbRequest_t *rq = (usbRequest_t*) ((void *) data);
	byte cmd = rq->bRequest;
	word wParam = rq->wValue.word;
	byte param1 = rq->wValue.bytes[0];
	byte param2 = rq->wValue.bytes[1];
	byte param3 = rq->wIndex.bytes[0];
	byte param4 = rq->wIndex.bytes[1];

	if ((rq->bmRequestType & USBRQ_TYPE_MASK) == USBRQ_TYPE_VENDOR)
	{
		usbMsgPtr = dataBuffer; /* tell the driver which data to return */
		switch (cmd)
		{
		case 10:
			digitalWrite(param1, param2);
			break;

		case 11:
			pinMode(param1, param2);
			break;

		case 12:
			analogWrite(param1, param2);
			break;

		case 13:
			return return_int8(digitalRead(param1));
			break;

		case 14:
			analogReference(param1);
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
			return return_int16(analogRead(param1));
			break;

		case 29:
			return return_int8(digitalPinToBitMask(param1));
			break;

		case 30:
			return return_int8(digitalPinToPort(param1));
			break;

		case 31:
			return return_int8(*portModeRegister(param1));
			break;

		case 34:
			return return_int8(USB_CONCAT_EXPANDED(P, USB_CFG_IOPORTNAME));
			break;
//		case 35:
//			return return_int8(A0);
//			break;
		case 36:
			return return_int8(digitalPinToTimer(param1));
			break;
		case 37:
			return return_int8(analogInPinToBit(param1));
			break;
		case 38:
			return return_int8(*portOutputRegister(param1));
			break;
		case 39:
			return return_int8(*portInputRegister(param1));
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
				if (index == wParam)
				{
					w = pgm_read_word(&reg_list[i]);
					break;
				}
				if (index > wParam)
					break;
			}
			if (w == 0)
			{
				// register not found
				switch (param3)
				{
				case REGISTER_CHECK:
					return return_int8(REGISTER_MISSING);
					break;
				default:
					return 0;
				}
			}

			volatile byte* preg = (volatile byte*) w;
			switch (param3)
			{
			case REGISTER_WRITE:
				*preg = param4;
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
			uint32_t w = pgm_read_dword(&intdef_list[param1]);
			return return_int32(w);
		}
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


/* ------------------------------------------------------------------------- */

/* ------------------------------------------------------------------------- */
SoftUsb::SoftUsb()
{
	pUsbFunctionSetup=&SoftUsb_UsbFunctionSetup;
}

void SoftUsb::begin()
{
	// disable timer 0 overflow interrupt (used for millis)

	// TODO: make this portable
#if defined( TIMSK0 )
	TIMSK0 &= !(1 << TOIE0);
#elif defined( TIMSK )
	TIMSK &= !(1 << TOIE0);
#endif

	cli();

	wdt_enable( WDTO_1S);
	/* Even if you don't use the watchdog, turn it off here. On newer devices,
	 * the status of the watchdog (on/off, period) is PRESERVED OVER RESET!
	 */
	/* RESET status: all port bits are inputs without pull-up.
	 * That's the way we need D+ and D-. Therefore we don't need any
	 * additional hardware initialization.
	 */
	usbInit();

	usbDeviceDisconnect();
	uchar i;
	i = 0;
	while (--i)
	{ /* fake USB disconnect for > 250 ms */
		_delay_ms(1);
	}
	usbDeviceConnect();

	sei();
}

/* This function must be called at regular intervals from the main loop.
 * Maximum delay between calls is somewhat less than 50ms (USB timeout for
 * accepting a Setup message). Otherwise the device will not be recognized.
 */
void SoftUsb::refresh()
{
	wdt_reset();
	usbPoll();
}
