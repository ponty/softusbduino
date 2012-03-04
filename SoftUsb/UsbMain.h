#pragma once

#include "usbdrv.h"

//#ifdef __cplusplus
//extern "C"
//{
//#endif

typedef usbMsgLen_t (TypeUsbFunctionSetup)(uchar data[8]);
extern TypeUsbFunctionSetup* pUsbFunctionSetup;


//#ifdef __cplusplus
//} // extern "C"
//#endif

