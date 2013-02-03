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

#include "SoftUsb_global.h"
#include "generated_mcu.h"
#include "SoftUsb_onewire.h"
#include "SoftUsb_return.h"
#include "SoftUsb_const.h"
#include "SoftUsb_timer.h"

bool g_wdt_auto_reset = true;

bool run_slow = false;
int slow_return;

typedef struct params
{
    byte cmd;uchar bytes[4];
    word word1;
    word word2;
} params_t;

params_t slow_params;

#include "SoftUsb_test.h"

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
    params.word2 = rq->wValue.word; // same as (params.bytes[0];params.bytes[1])

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

        case MAGIC_NUMBER: //42
            return return_int8(MAGIC_NUMBER);
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
            wdt_enable(params.bytes[0]);
            break;

        case 83:
            wdt_disable();
            break;

        case 84:
            g_wdt_auto_reset = params.bytes[0];
            break;

        case 90:
            slow_params = params;
            run_slow = true;
            break;
        case 91:
            return return_int32(g_count);
            break;

        case 101:
        case 102:
        case 103:
        case 104:
        case 105:
        {
            word regaddr = 0;
            byte regsize = 0;
            word regindex = params.word1;
            word regvalue = params.word2;
            byte regcmd = cmd - 100;
            for (unsigned int i = 0; i < REG_COUNT; i++)
            {
                word index = pgm_read_word(&reg_index_list[i]);
                if (index == regindex)
                {
                    regaddr = pgm_read_word(&reg_list[i]);
                    regsize = pgm_read_byte(&sizeof_list[i]);
                    break;
                }
                if (index > regindex)
                    break;
            }
            if (regaddr == 0)
            {
                // register not found
                switch (regcmd)
                {
                case REGISTER_CHECK:
                    return return_int8(REGISTER_MISSING);
                    break;
                default:
                    return 0;
                }
            }

            volatile byte* preg8 = (volatile byte*) regaddr;
            volatile word* preg16 = (volatile word*) regaddr;
            switch (regcmd)
            {
            case REGISTER_WRITE:
                switch (regsize)
                {
                case 1:
                    *preg8 = (byte) regvalue;
                    break;
                case 2:
                    *preg16 = regvalue;
                    break;
                }
                break;
            case REGISTER_READ:
                switch (regsize)
                {
                case 1:
                    return return_int8(*preg8);
                    break;
                case 2:
                    return return_int16(*preg16);
                    break;
                }
                break;
            case REGISTER_CHECK:
                return return_int8(REGISTER_OK);
                break;
            case REGISTER_ADDRESS:
                return return_int16(regaddr);
                break;
            case REGISTER_SIZE:
                return return_int8(regsize);
                break;
            }
        }
            break;

        case 200:
        {
            return slow_return;
            break;
        }

        case 210:
        {
            return return_int8(delay_test(&params));
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
        // disable Timer0
        // millis() and delay()
#if defined( TIMSK0 )
        TIMSK0 &= !(1 << TOIE0);
#elif defined( TIMSK )
        TIMSK &= !(1 << TOIE0);
#endif

        cli();

        //		  wdt_reset();

        //wdt_enable (WDTO_1S);
        wdt_disable();
        /* Even if you don't use the watchdog, turn it off here. On newer devices,
         * the status of the watchdog (on/off, period) is PRESERVED OVER RESET!
         */
        /* RESET status: all port bits are inputs without pull-up.
         * That's the way we need D+ and D-. Therefore we don't need any
         * additional hardware initialization.
         */
        usbInit();

        usbReconnect();

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

        if (run_slow)
        {
            wdt_reset();

            run_slow = false;

            usbPoll();

            uchar i = 10; // ms
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

            case 90:
            {
                bool b_usb_disconnect = slow_params.bytes[0];
                if (b_usb_disconnect)
                    usbDeviceDisconnect();
//                USB_INTR_ENABLE &= ~_BV(USB_INTR_ENABLE_BIT);

                gate_length =slow_params.word1;
                startTCCR2B=slow_params.bytes[1];
                g_count = FreqCount.read1();

//                USB_INTR_ENABLE |= _BV(USB_INTR_ENABLE_BIT);
                if (b_usb_disconnect)
                    usbDeviceConnect();
            }
                break;

            case 211:
                slow_return = return_int8(delay_test(&slow_params));
                break;
            }
            wdt_reset();
        }

        usbPoll();
    }
};

