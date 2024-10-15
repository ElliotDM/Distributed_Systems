///////////////////////////////
// Modified array through 
// processes using MPI
// Author: Duran Macedo Elliot
// Date: 28-08-24
///////////////////////////////

#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define ARRAY_SIZE 5
#define ITERATIONS 2

int main(int argc, char *argv[])
{
    int id, np, name_len, iteration = 0;
    float array[ARRAY_SIZE];
    char host_names[MPI_MAX_PROCESSOR_NAME];
    MPI_Status state;

    MPI_Init(&argc, &argv);
    MPI_Get_processor_name(host_names, &name_len);
    MPI_Comm_rank(MPI_COMM_WORLD, &id);
    MPI_Comm_size(MPI_COMM_WORLD, &np);

    while (iteration < ITERATIONS)
    {
        if (id == 0)
        {
            if (iteration == 0)
            {
                for (int i = 0; i < ARRAY_SIZE; i++)
                    array[i] = i + 1;

                for (int i = 0; i < ARRAY_SIZE; i++)
                    printf("%f ", array[i]);
            }

            MPI_Send(array, ARRAY_SIZE, MPI_FLOAT, 1, 8, MPI_COMM_WORLD);
            MPI_Recv(array, ARRAY_SIZE, MPI_FLOAT, np - 1, 8, MPI_COMM_WORLD, &state);
        }
        else
        {
            MPI_Recv(array, ARRAY_SIZE, MPI_FLOAT, id - 1, 8, MPI_COMM_WORLD, &state);

            for (int i = 0; i < ARRAY_SIZE; i++)
                array[i]++;

            printf("\nData modifed from process %d in host %s\n", id, host_names);

            for (int i = 0; i < ARRAY_SIZE; i++)
                printf("%f ", array[i]);

            if (id == (np - 1))
            {
                MPI_Send(array, ARRAY_SIZE, MPI_FLOAT, 0, 8, MPI_COMM_WORLD);
            }
            else
            {
                MPI_Send(array, ARRAY_SIZE, MPI_FLOAT, id + 1, 8, MPI_COMM_WORLD);
            }
        }

        iteration++;
    }

    if (id == 0)
    {
        if (iteration == ITERATIONS)
        {
            printf("\nResult from process %d in host %s\n", id, host_names);

            for (int i = 0; i < ARRAY_SIZE; i++)
                printf("%f ", array[i]);

            printf("\n");
        }
    }

    MPI_Finalize();
    return 0;
}