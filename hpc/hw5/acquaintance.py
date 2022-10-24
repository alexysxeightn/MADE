#!/usr/local/bin/python
from mpi4py import MPI
import random

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()

all_ranks = [*range(size)]
processor_name = f"processor_{rank}"

if rank == 0:
    print(f'Я {processor_name}')
    prev_proccesors = [(processor_name, rank)]
    comm.ssend(prev_proccesors, dest=random.choice(all_ranks[1:]))
else:
    prev_proccesors = comm.recv()

    print(
        f'Я {processor_name} и знаком с {[x[0] for x in prev_proccesors]}',
        flush=True
    )

    used_ranks = [rank] + [x[1] for x in prev_proccesors]
    not_used_ranks = [x for x in all_ranks if x not in used_ranks]

    if not_used_ranks:
        prev_proccesors.append((processor_name, rank))
        comm.ssend(prev_proccesors, dest=random.choice(not_used_ranks))

MPI.Finalize()
