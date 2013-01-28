#pragma once

//******************************************************************
//  Timer2 Interrupt Service is invoked by hardware Timer2 every 1ms = 1000 Hz
//  16Mhz / 128 / 125 = 1000 Hz
//  here the gatetime generation for freq. measurement takes place:
//volatile unsigned char f_ready;
//volatile unsigned char f_mlt;
volatile uint16_t f_tics;
volatile uint16_t f_period;
volatile bool f_first;
volatile bool f_ready;

//volatile unsigned int f_comp;
//unsigned long f_freq;

volatile uint16_t f_counter_overflows;

ISR(TIMER2_COMPA_vect)
{
    // multiple 2ms = gate time = 100 ms

    if (f_first)
    {
        TCNT1 = 0; // Counter1 = 0
        if (TIFR1 & (1<<TOV1))
        { // if Timer/Counter 1 overflow flag
            TIFR1 |=(1<<TOV1); // clear Timer/Counter 1 overflow flag
        }
        f_first=false;
    }
    else
    {
        if (f_tics >= f_period) // end of gate time, measurement ready

        {
            // GateCalibration Value, set to zero error with reference frequency counter
            //  delayMicroseconds(FreqCounter::f_comp); // 0.01=1/ 0.1=12 / 1=120 sec
            //delayMicroseconds(f_comp);
            TCCR1B = TCCR1B & ~7; // Gate Off  / Counter T1 stopped
            TIMSK2 &= ~(1<<OCIE2A); // disable Timer2 Interrupt
            //TIMSK0 |=(1<<TOIE0); // enable Timer0 again // millis and delay
            //f_ready=1; // set global flag for end count period

            // calculate now frequeny value
            //f_freq=0x10000 * f_mlt; // mult #overflows by 65636
            //f_freq += TCNT1; // add counter1 value
            //f_mlt=0;
            USB_INTR_ENABLE |= _BV( USB_INTR_ENABLE_BIT );
            f_ready=true;
        }
        else
        {
            f_tics++; // count number of interrupt events
            if (TIFR1 & (1<<TOV1))
            { // if Timer/Counter 1 overflow flag
                f_counter_overflows++;//f_mlt++; // count number of Counter1 overflows
                TIFR1 |=(1<<TOV1); // clear Timer/Counter 1 overflow flag
            }
        }
    }
}
