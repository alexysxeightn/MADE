#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void seed_threads(unsigned int * seeds)
{
    int my_thread_id;
    unsigned int seed;
    #pragma omp parallel private(seed, my_thread_id)
    {
        my_thread_id = omp_get_thread_num();
        unsigned int seed = (unsigned) time(NULL);
        seeds[my_thread_id] = (seed & 0xFFFFFFF0) | (my_thread_id + 1);
        printf("Thread %d has seed %u\n", my_thread_id, seeds[my_thread_id]);
    }
}

double calc_pi(size_t num_all_points, unsigned int * seeds)
{
    int tid, num_correct_points = 0;
    
    #pragma omp parallel for private(tid) reduction(+:num_correct_points)
    for (int i = 0; i < num_all_points; ++i)
    {
        tid = omp_get_thread_num();
        double x = ((double)rand_r(&seeds[tid]) / (double)RAND_MAX);
        double y = ((double)rand_r(&seeds[tid]) / (double)RAND_MAX);
        
        if ((x * x + y * y) < 1.0)
            num_correct_points += 1;
    }
    
    return (double)(4.0 * num_correct_points / num_all_points);
}

int main (int argc, char *argv[])
{
    const size_t NUM_ALL_POINTS = 100000000;
    
    const int n_threads = omp_get_num_threads();
    unsigned int seeds[n_threads];
    seed_threads(seeds);
    
    double time = omp_get_wtime();
    double pi = calc_pi(NUM_ALL_POINTS, seeds);
    time = omp_get_wtime() - time;
    
    printf("pi = %f, time = %f seconds\n", pi, time);
    
    return 0;
}
