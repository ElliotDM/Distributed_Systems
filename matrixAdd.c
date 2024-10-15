///////////////////////////////
// Matrix addition using MPI
// Author: Duran Macedo Elliot
// Date: 28-08-24
///////////////////////////////

#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define n 12
#define m 10

int main(int argc, char *argv[])
{
    int id, np;
    int *matrix1, *matrix2, *result;
    MPI_Status state;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &id);
    MPI_Comm_size(MPI_COMM_WORLD, &np);

    if (id == 0)
    {
        matrix1 = (int *)calloc(n * m, sizeof(int));
        matrix2 = (int *)calloc(n * m, sizeof(int));
        result = (int *)calloc(n * m, sizeof(int));

        for (int i = 0; i < n * m; i++)
        {
            matrix1[i] = i + 1;
            matrix2[i] = i + 1;
        }

        for (int i = 0; i < np - 1; i++)
        {
            MPI_Send(&matrix1[i * 3 * m], 3 * m, MPI_INT, i + 1, i + 1, MPI_COMM_WORLD);
            MPI_Send(&matrix2[i * 3 * m], 3 * m, MPI_INT, i + 1, i + 1, MPI_COMM_WORLD);
        }

        for (int i = 0; i < np - 1; i++)
            MPI_Recv(&result[i * 3 * m], 3 * m, MPI_INT, i + 1, i + 1, MPI_COMM_WORLD, &state);

        for (int i = 0; i < n * m; i++)
        {
            if (i % 10 == 0)
                printf("\n");

            printf("%d ", result[i]);
        }

        printf("\n\n");
    }
    else
    {
        matrix1 = (int *)calloc(3 * m, sizeof(int));
        matrix2 = (int *)calloc(3 * m, sizeof(int));
        result = (int *)calloc(3 * m, sizeof(int));

        MPI_Recv(&matrix1[0], 3 * m, MPI_INT, 0, id, MPI_COMM_WORLD, &state);
        MPI_Recv(&matrix2[0], 3 * m, MPI_INT, 0, id, MPI_COMM_WORLD, &state);

        for (int i = 0; i < 3 * m; i++)
            result[i] = matrix1[i] + matrix2[i];

        MPI_Send(&result[0], 3 * m, MPI_INT, 0, id, MPI_COMM_WORLD);
    }

    free(matrix1);
    free(matrix2);
    free(result);
    MPI_Finalize();
    return 0;
}