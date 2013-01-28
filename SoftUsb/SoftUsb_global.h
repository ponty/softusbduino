#pragma once

#define _STR(s) #s
#define STR(s) _STR(s)



void * operator new(size_t size)
{
    return malloc(size);
}

void operator delete(void * ptr)
{
    free(ptr);
}
