#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

void ZeroMatrix(double * A, size_t N)
{
    for(size_t i=0; i<N; i++)
    {
        for(size_t j=0; j<N; j++)
        {
            A[i * N + j] = 0.0;
        }
    }
}

void RandomMatrix(double * A, size_t N)
{
    srand(time(NULL));

    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            A[i * N + j] = rand() / RAND_MAX;
        }
    }
}

double CalcMatMulTime_ijk(double * A, double * B, double * C, size_t N)
{
    struct timeval start, end;
    double r_time = 0.0;
    size_t i, j, k;

    ZeroMatrix(&C[0], N);

    gettimeofday(&start, NULL);
    
    for (i = 0; i < N; i++)
        for(j = 0; j < N; j++)
        {
            for(k = 0; k < N; k++)
                C[i * N + j] = C[i * N + j] + A[i * N + k] * B[k * N + j];
        }
    gettimeofday(&end, NULL);
    
    r_time = end.tv_sec - start.tv_sec + ((double) (end.tv_usec - start.tv_usec)) / 1000000;
    
    return r_time;
}

double CalcMatMulTime_jik(double * A, double * B, double * C, size_t N)
{
    struct timeval start, end;
    double r_time = 0.0;
    size_t i, j, k;

    ZeroMatrix(&C[0], N);


    gettimeofday(&start, NULL);
    


    for (j = 0; j < N; j++)
        for(i = 0; i < N; i++)
        {
            for(k = 0; k < N; k++)
                C[i * N + j] = C[i * N + j] + A[i * N + k] * B[k * N + j];
        }
    gettimeofday(&end, NULL);
    
    r_time = end.tv_sec - start.tv_sec + ((double) (end.tv_usec - start.tv_usec)) / 1000000;
    
    return r_time;
}

double CalcMatMulTime_kij(double * A, double * B, double * C, size_t N)
{
    struct timeval start, end;
    double r_time = 0.0;
    size_t i, j, k;

    ZeroMatrix(&C[0], N);

    gettimeofday(&start, NULL);
    
    for (k = 0; k < N; k++)
        for(i = 0; i < N; i++)
        {
            for(j = 0; j < N; j++)
                C[i * N + j] = C[i * N + j] + A[i * N + k] * B[k * N + j];
        }
    gettimeofday(&end, NULL);
    
    r_time = end.tv_sec - start.tv_sec + ((double) (end.tv_usec - start.tv_usec)) / 1000000;
    
    return r_time;
}

double CalcMatMulTime_kij_opt(double * A, double * B, double * C, size_t N)
{
    struct timeval start, end;
    double r_time = 0.0;
    size_t i, j, k;

    size_t dummy = 0;

    ZeroMatrix(&C[0], N);

    gettimeofday(&start, NULL);
    
    for (k = 0; k < N; k++)
        for(i = 0; i < N; i++)
        {
            dummy = i * N;
            for(j = 0; j < N; j++)
                C[dummy + j] = C[dummy + j] + A[dummy + k] * B[k * N + j];
        }
    gettimeofday(&end, NULL);
    
    r_time = end.tv_sec - start.tv_sec + ((double) (end.tv_usec - start.tv_usec)) / 1000000;
    
    return r_time;
}

// add variable 'dummy' for k (not only for i)
double CalcMatMulTime_kij_opt2(double * A, double * B, double * C, size_t N)
{
    struct timeval start, end;
    double r_time = 0.0;
    size_t i, j, k;

    size_t dummy_i = 0;
    size_t dummy_k = 0;

    ZeroMatrix(&C[0], N);

    gettimeofday(&start, NULL);
    
    for (k = 0; k < N; k++)
    	dummy_k = k * N;
        for(i = 0; i < N; i++)
        {
            dummy_i = i * N;
            for(j = 0; j < N; j++)
                C[dummy_i + j] = C[dummy_i + j] + A[dummy_i + k] * B[dummy_k + j];
        }
    gettimeofday(&end, NULL);
    
    r_time = end.tv_sec - start.tv_sec + ((double) (end.tv_usec - start.tv_usec)) / 1000000;
    
    return r_time;
}

int main()
{
    
    int NRuns = 5, N;
    size_t i, j, k;

    int *N_array;
    N_array = (int *) malloc(6 * sizeof(int));
    N_array[0] = 500; N_array[1] = 512;
    N_array[2] = 1000; N_array[3] = 1024;
    N_array[4] = 2000; N_array[5] = 2048;

    double *runtimes;
    double *A, *B, *C;
    
    for (int i = 0; i < 6; i++)
    {
	   N = N_array[i];
	   printf("Size = %d\n", N);
    	A = (double *) malloc(N * N * sizeof(double));
    	B = (double *) malloc(N * N * sizeof(double));
    	C = (double *) malloc(N * N * sizeof(double));
    	runtimes = (double *) malloc(NRuns * sizeof(double));

   	    RandomMatrix(&A[0], N);
    	RandomMatrix(&B[0], N);

    // ijk ordering
        double average_runtime = 0.0;
        for(int n=0; n<NRuns; n++)
        {
            runtimes[n]=CalcMatMulTime_ijk(&A[0], &B[0], &C[0], N);
            average_runtime += runtimes[n]/NRuns;
        }

        printf("average runtime ijk %lf seconds\n", average_runtime);

    // jik ordering
        average_runtime = 0.0;
        for(int n=0; n<NRuns; n++)
        {
            runtimes[n]=CalcMatMulTime_jik(&A[0], &B[0], &C[0], N);
            average_runtime += runtimes[n]/NRuns;
        }

        printf("average runtime jik %lf seconds\n", average_runtime);
        
    // kij ordering
        average_runtime = 0.0;
        for(int n=0; n<NRuns; n++)
        {
            runtimes[n]=CalcMatMulTime_kij(&A[0], &B[0], &C[0], N);
            average_runtime += runtimes[n]/NRuns;
        }
        printf("average runtime kij %lf seconds\n", average_runtime);
        
    // kij ordering naive optimization (useless for -O3)
        average_runtime = 0.0;
        for(int n=0; n<NRuns; n++)
        {
            runtimes[n]=CalcMatMulTime_kij_opt(&A[0], &B[0], &C[0], N);
            average_runtime += runtimes[n]/NRuns;
        }
        printf("average runtime kij opt %lf seconds\n", average_runtime);

    // kij ordering optimization (my solution)
        average_runtime = 0.0;
        for(int n=0; n<NRuns; n++)
        {
            runtimes[n]=CalcMatMulTime_kij_opt2(&A[0], &B[0], &C[0], N);
            average_runtime += runtimes[n]/NRuns;
        }
        printf("average runtime kij opt2 %lf seconds\n", average_runtime);
        printf("---------------------------------\n");


        free(A); 
        free(B);
        free(C);
    }
        return 0;
}

