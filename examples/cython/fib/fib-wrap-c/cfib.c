#include "cfib.h"

int cfib(int n)
{
    int a=0, b=1, i=0, tmp=0;
    for(i=0; i<n; i++) {
        tmp = a; a += b; b = tmp;
    }
    return a;
}
