#pragma once

byte delay_test(params_t* p)
{
    bool b_disable_interrupts = p->bytes[0] & 1;
    bool b_ms = p->bytes[0] & 2;
    bool b_loop = true;//p->bytes[0] & 4;

    static byte index = 0;
    index++;

    if (b_disable_interrupts)
        noInterrupts();

    if (b_ms)
    {
        //delay(p->word1);  // not working
        if (b_loop)
        {
            uint16_t i = p->word1; // ms
            while (--i)
            {
                _delay_ms(1);
            }
        }
        else
        {
            //_delay_ms(p->word1);  // too much code
        }
    }
    else
    {
        delayMicroseconds(p->word1);
    }

    if (b_disable_interrupts)
        interrupts();

    return index;
}
