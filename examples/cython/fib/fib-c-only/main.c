#include "cfib.h"

#define NN 10000000

int v;

int main(int argc, char **argv)
{
    unsigned long i;
    for(i=0; i<NN; i++) {
        cfib(100);
    }
    return 0;
}
