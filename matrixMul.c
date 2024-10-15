///////////////////////////////
// Matrix multiplication
// using MPI
// Author: Duran Macedo Elliot
// Date: 28-08-24
///////////////////////////////

#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define m 10
#define n 12
#define p 10

int main(int argc, char *argv[])
{
    int id, np, sum;
    int *matrixA, *matrixB, *result, *row, *partial;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &id);
    MPI_Comm_size(MPI_COMM_WORLD, &np);

    if (np != m)
    {
        if (id == 0)
            printf("Number of process must be %d\n", m);

        MPI_Finalize();
        return -1;
    }

    matrixB = (int *)calloc(n * p, sizeof(int));
    row = (int *)calloc(n, sizeof(int));
    partial = (int *)calloc(p, sizeof(int));

    if (id == 0)
    {
        matrixA = (int *)calloc(m * n, sizeof(int));
        result = (int *)calloc(m * p, sizeof(int));

        for (int i = 0; i < m * n; i++)
            matrixA[i] = i + 1;

        for (int i = 0; i < n * p; i++)
            matrixB[i] = i + 1;
    }

    MPI_Scatter(matrixA, n, MPI_INT, row, n, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(matrixB, n * p, MPI_INT, 0, MPI_COMM_WORLD);

    for (int col = 0; col < p; col++)
    {
        sum = 0;

        for (int idx = 0; idx < n; idx++)
            sum += row[idx] * matrixB[col + (p * idx)];

        partial[col] = sum;
    }

    MPI_Gather(partial, p, MPI_INT, result, p, MPI_INT, 0, MPI_COMM_WORLD);

    if (id == 0)
    {
        for (int i = 0; i < m * p; i++)
        {
            if (i % p == 0)
                printf("\n");

            printf("%d ", result[i]);
        }

        printf("\n\n");
        free(matrixA);
        free(result);
    }

    free(row);
    free(partial);
    free(matrixB);

    MPI_Finalize();
    return 0;
}