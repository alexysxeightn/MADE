#include <cblas.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void print_matrix(double *matrix, int N)
{
    size_t dummy_i = 0;

    for (int i = 0; i < N; ++i)
    {
        dummy_i = i * N;

        for (int j = 0; j < N; ++j)
            printf("%.0lf\t", matrix[dummy_i + j]);

        printf("\n");
    }
    printf("\n");
}

void random_adj_matrix(double *matrix, int N)
{
    unsigned int seed = (unsigned) time(NULL);
    size_t dummy_i = 0;
    
    for (int i = 0; i < N; ++i)
       {
        dummy_i = i * N;
        for (int j = 0; j < N; ++j) 
            matrix[dummy_i + j] = (i == j) ? 0 : rand_r(&seed) & 1;
    }
}

double l2_norm(double *vec_1, double *vec_2, int N)
{
    double result = 0;

    #pragma omp parallel shared(vec_1, vec_2, N, result)
    {
        #pragma omp for reduction(+:result)
        for (int i = 0; i < N; ++i)
            result += (vec_1[i] - vec_2[i]) * (vec_1[i] - vec_2[i]);
    }

    return result;
}

void matmul(double *mat_1, double *mat_2, double *result, int N)
{
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, N, N, N,
                1.0, mat_1, N, mat_2, N, 0.0, result, N);
}

void mat_mul_vec(double *matrix, double *vector, double *result, int N)
{
    cblas_dgemv(CblasRowMajor, CblasNoTrans, N, N,
                1.0, matrix, N, vector, 1, 0.0, result, 1);
}

void matrix_power(double *matrix, double *result, int N, int power)
{

    size_t dummy_i = 0;

    for (int i = 0; i < N; ++i)
    {
        dummy_i = i * N;
        for (int j = 0; j < N; ++j)
            result[dummy_i + j] = (i == j) ? 1 : 0;
    }

    double *buffer = (double *) malloc(N * N * sizeof(double));
    double *matrix_pow = (double *) malloc(N * N * sizeof(double));

    memcpy(matrix_pow, matrix, N * N * sizeof(double));

    while (power > 0)
    {
        if (power & 1)
        {
            matmul(matrix_pow, result, buffer, N);
            memcpy(result, buffer, N * N * sizeof(double));
        }

        matmul(matrix_pow, matrix_pow, buffer, N);
        memcpy(matrix_pow, buffer, N * N * sizeof(double));

        power >>= 1;
    }

    free(buffer);
    free(matrix_pow);
}

void naive_ranking(double *matrix, double *rank, int N)
{
    double L = 0;

    #pragma omp parallel shared(rank, L, N)
    {
        #pragma omp for reduction(+:L)
        for (int j = 0; j < N; ++j)
        {
            rank[j] = 0;

            for (int i = 0; i < N; ++i)
                rank[j] += matrix[i * N + j];

            L += rank[j];
        }

        #pragma omp for
        for (int i = 0; i < N; ++i)
            rank[i] /= L;
    }
}

void pagerank(double *matrix, double *rank, int N,
              double eps, double d, int max_iter)
{
    size_t dummy_i = 0;

    double *M_matrix = (double *) malloc(N * N * sizeof(double));

    #pragma omp parallel shared(matrix, M_matrix, N, dummy_i)
    {
        #pragma omp for
        for (int i = 0; i < N; ++i)
        {
            double out_links = 0;
            dummy_i = i * N;

            for (int j = 0; j < N; ++j)
                out_links += matrix[dummy_i + j];

            for (int j = 0; j < N; ++j) 
                M_matrix[j * N + i] = (out_links == 0) ? 1.0 / N : matrix[dummy_i + j] / out_links;
        }
    }

    double *prev_rank = (double *) malloc(N * sizeof(double));

    for (int i = 0; i < N; ++i)
        prev_rank[i] = 1.0 / N;

    for (int i = 0; i < max_iter; ++i)
    {
        mat_mul_vec(M_matrix, prev_rank, rank, N);

        for (int j = 0; j < N; ++j)
            rank[j] = (1 - d) / N + d * rank[j];

        if (l2_norm(prev_rank, rank, N) < eps)
            break;

        memcpy(prev_rank, rank, N * sizeof(double));
    }

    free(M_matrix);
    free(prev_rank);
}

int main()
{
    const int N = 8;
    const int max_power = 4;

    // Случайная матрица смежности
    double *matrix = (double *) malloc(N * N * sizeof(double));
    random_adj_matrix(matrix, N);
    printf("Случайная матрица смежности A:\n");
    print_matrix(matrix, N);

    // Степени матрицы смежности от 2 до max_power
    double *pow_matrix = (double *) malloc(N * N * sizeof(double));
    for (int power = 2; power <= max_power; ++power)
    {
        matrix_power(matrix, pow_matrix, N, power);
        printf("A^%d:\n", power);
        print_matrix(pow_matrix, N);
    }

    // Наивное ранжирование вершин
    double *naive_rank = (double *) malloc(N * sizeof(double));
    naive_ranking(matrix, naive_rank, N);

    // Ранжирование с помощью pagerank
    double *pagerank_result = (double *) malloc(N * sizeof(double));
    double eps = 1e-4, d = 0.85; int max_iter = 1e3;
    pagerank(matrix, pagerank_result, N, eps, d, max_iter);

    // Сравнение методов ранжирования
    printf("Результаты ранжирования:\n");
    printf("i \t naiverank \t pagerank\n");
    for (int i = 0; i < N; ++i)
        printf("%d \t %.5lf \t %.5lf \n", i, naive_rank[i], pagerank_result[i]);

    free(matrix);
    free(pow_matrix);
    free(naive_rank);
    free(pagerank_result);

    return 0;
}