///////////////////////////////
// Dot product using MPI
// Author: Duran Macedo Elliot
// Date: 28-08-24
///////////////////////////////

#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define SIZE 2

int main(int argc, char *argv[])
{
    int id, np, name_len, valA, valB, partial, final;
    int *vectorA, *vectorB, *result;
    char host_names[MPI_MAX_PROCESSOR_NAME];

    MPI_Init(&argc, &argv);
    MPI_Get_processor_name(host_names, &name_len);
    MPI_Comm_rank(MPI_COMM_WORLD, &id);
    MPI_Comm_size(MPI_COMM_WORLD, &np);

    if (id == 0)
    {
        vectorA = (int *)calloc(SIZE, sizeof(int));
        vectorB = (int *)calloc(SIZE, sizeof(int));
        result = (int *)calloc(SIZE, sizeof(int));

        for (int i = 0; i < SIZE; i++)
        {
            vectorA[i] = i + 1;
            vectorB[i] = 2 * (i + 1);
        }

        printf("Vector A\n");

        for (int i = 0; i < SIZE; i++)
            printf("%d ", vectorA[i]);

        printf("\nVector B\n");

        for (int i = 0; i < SIZE; i++)
            printf("%d ", vectorB[i]);
    }

    MPI_Scatter(vectorA, 1, MPI_INT, &valA, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Scatter(vectorB, 1, MPI_INT, &valB, 1, MPI_INT, 0, MPI_COMM_WORLD);

    partial = valA * valB;

    printf("\nOperation performed from process %d in host %s\n", id, host_names);
    printf("(%d) * (%d) = %d\n", valA, valB, partial);

    MPI_Gather(&partial, 1, MPI_INT, result, 1, MPI_INT, 0, MPI_COMM_WORLD);

    if (id == 0)
    {
        for (int i = 0; i < SIZE; i++)
            final += result[i];

        printf("Result = %d\n", final);

        free(vectorA);
        free(vectorB);
        free(result);
    }

    MPI_Finalize();
    return 0;
}