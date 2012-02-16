//#include <avr/io.h>
//#include <avr/wdt.h>
//#include <avr/interrupt.h>  /* for sei() */
//#include <util/delay.h>     /* for _delay_ms() */
//#include <avr/pgmspace.h>
#include "usbdrv.h"
#include "UsbMain.h"


/* ------------------------------------------------------------------------- */
/* ----------------------------- USB interface ----------------------------- */
/* ------------------------------------------------------------------------- */

PROGMEM char usbHidReportDescriptor[22] =
{ /* USB report descriptor */
0x06, 0x00, 0xff, // USAGE_PAGE (Generic Desktop)
		0x09, 0x01, // USAGE (Vendor Usage 1)
		0xa1, 0x01, // COLLECTION (Application)
		0x15, 0x00, //   LOGICAL_MINIMUM (0)
		0x26, 0xff, 0x00, //   LOGICAL_MAXIMUM (255)
		0x75, 0x08, //   REPORT_SIZE (8)
		0x95, 0x01, //   REPORT_COUNT (1)
		0x09, 0x00, //   USAGE (Undefined)
		0xb2, 0x02, 0x01, //   FEATURE (Data,Var,Abs,Buf)
		0xc0 // END_COLLECTION
		};
/* The descriptor above is a dummy only, it silences the drivers. The report
 * it describes consists of one byte of undefined data.
 * We don't transfer our data through HID reports, we use custom requests
 * instead.
 */

/* ------------------------------------------------------------------------- */

//#ifdef __cplusplus
//extern "C"
//{
//#endif


TypeUsbFunctionSetup* pUsbFunctionSetup=0;

usbMsgLen_t usbFunctionSetup(uchar data[8])
{
	if (pUsbFunctionSetup)
		return (*pUsbFunctionSetup)(data);
	return 0;
}

/* ------------------------------------------------------------------------- */

//#ifdef __cplusplus
//} // extern "C"
//#endif

