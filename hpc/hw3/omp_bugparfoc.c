#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

int main (int argc, char *argv[])
{
    const size_t N = 100;
    const size_t chunk = 3;

    int tid;
    float a[N], b[N], c[N];

    for (int i = 0; i < N; ++i)
    {
        a[i] = b[i] = (float)i;
    }

#pragma omp parallel for \
    shared(a,b,c,chunk) \
    private(tid) \
    schedule(static,chunk)
    for (int i = 0; i < N; ++i)
    {
        tid = omp_get_thread_num();
        c[i] = a[i] + b[i];
        printf("tid = %d, c[%d] = %f\n", tid, i, c[i]);
    }

    return 0;
}
