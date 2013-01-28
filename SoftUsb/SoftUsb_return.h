#pragma once

#define BUFFER_SIZE  20

#define TYPE_INT8   1
#define TYPE_INT16  2
#define TYPE_INT32  3
#define TYPE_STRING 4
#define TYPE_FLOAT  5
#define TYPE_VOID   6
#define TYPE_BYTE_ARRAY  7

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
