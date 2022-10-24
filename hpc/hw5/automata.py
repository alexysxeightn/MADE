#!/usr/local/bin/python
from argparse import ArgumentParser
import random
from mpi4py import MPI


def generate_rule_patterns(rule_id):
    rule_patterns = [
        format(i, 'b').zfill(3)
        for i, symb in enumerate(format(rule_id, 'b').zfill(8)[::-1])
        if symb == '1'
    ]
    rule_patterns = [[int(symb) for symb in pattern] for pattern in rule_patterns]
    return rule_patterns


def step(array, rule_patterns):
    new_array = array.copy()
    for i in range(1, len(array) - 1):
        new_array[i] = int(array[i - 1:i + 2] in rule_patterns)
    return new_array


def exchange_ghost_cells(array, comm, rank, world_size, periodic=True):
    if world_size == 1:
        array[-1] = array[1] if periodic else 0
        array[0] = array[-2] if periodic else 0
    else:
        left_ghost_value = array[1] if periodic or 0 < rank < world_size else 0
        right_ghost_value = array[-2] if periodic or -1 < rank < world_size - 1 else 0

        comm.send(right_ghost_value, dest=(rank+1)%world_size, tag=0)
        comm.send(left_ghost_value, dest=(rank-1)%world_size, tag=1)
        
        array[0], array[-1] = comm.recv(tag=0), comm.recv(tag=1)

    return array


def print_cells(array):
    print("".join(["⬛" if x else "⬜" for x in array]), flush=True)


def automata(rule_id, size, num_epochs, periodic, show_progress):
    start_time = MPI.Wtime()
    comm = MPI.COMM_WORLD
    world_size, rank = comm.Get_size(), comm.Get_rank()
    rule_patterns = generate_rule_patterns(rule_id)

    if size % world_size != 0:
        MPI.Finalize()
    
    assert size % world_size == 0, "size % world_size != 0"

    rank_arr_size = size // world_size
    array = [random.randint(0, 1) for _ in range(rank_arr_size + 2)]

    for _ in range(num_epochs):
        array = exchange_ghost_cells(array, comm, rank, world_size, periodic)
        full_array = [array] if world_size == 1 else comm.gather(array, root=0)

        if show_progress and rank == 0:
            print_cells([x for subarray in full_array for x in subarray[1:-1]])

        array = step(array, rule_patterns)

    full_array = [array] if world_size == 1 else comm.gather(array, root=0)
    if rank == 0:
        if show_progress:
            print_cells([elem for subarray in full_array for elem in subarray[1:-1]])
        print(f"Time for world_size = {world_size}: {MPI.Wtime() - start_time:0.4f} seconds")

    MPI.Finalize()


def main():
    parser = ArgumentParser()
    parser.add_argument("--rule-id", type=int, default=110)
    parser.add_argument("--size", type=int, default=32)
    parser.add_argument("--num-epochs", type=int, default=32)
    parser.add_argument("--periodic", action="store_true")
    parser.add_argument("--show-progress", action="store_true")

    arguments = parser.parse_args()

    automata(
        arguments.rule_id,
        arguments.size,
        arguments.num_epochs,
        arguments.periodic,
        arguments.show_progress 
    )


if __name__ == "__main__":
    main()